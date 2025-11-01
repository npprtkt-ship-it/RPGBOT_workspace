"""
死亡履歴システム - ストーリー分岐・称号解放のロジック
"""

import db
from death_stories import DEATH_STORIES, DEATH_PATTERNS

# ==============================
# ストーリートリガー判定
# ==============================

async def check_death_triggers(user_id):
    """
    死亡後にトリガー可能なストーリーイベントをチェック
    返り値: {"type": "story/title/none", "data": {...}}
    """

    # 1. 特定敵への死亡回数チェック
    story_trigger = await check_enemy_death_count_triggers(user_id)
    if story_trigger:
        return story_trigger

    # 2. 連続死亡パターンチェック
    pattern_trigger = await check_death_pattern_triggers(user_id)
    if pattern_trigger:
        return pattern_trigger

    # 3. 称号解放チェック
    title_trigger = await check_title_triggers(user_id)
    if title_trigger:
        return title_trigger

    return {"type": "none"}


async def check_enemy_death_count_triggers(user_id):
    """特定の敵に○回殺された時のトリガー"""

    for story_id, story_data in DEATH_STORIES.items():
        trigger_type = story_data.get("trigger_type")

        if trigger_type == "enemy_count":
            enemy_name = story_data.get("enemy_name")
            required_count = story_data.get("required_count", 3)

            # 既に表示済みかチェック
            if await db.get_story_flag(user_id, story_id):
                continue

            # 死亡回数チェック
            death_count = await db.get_death_count_by_enemy(user_id, enemy_name)

            if death_count >= required_count:
                # フラグを立てて返す
                await db.set_story_flag(user_id, story_id)
                return {
                    "type": "story",
                    "story_id": story_id,
                    "data": story_data
                }

    return None


async def check_death_pattern_triggers(user_id):
    """連続死亡パターンのトリガー"""

    for pattern_id, pattern_data in DEATH_PATTERNS.items():
        pattern = pattern_data.get("pattern", [])
        story_id = pattern_data.get("story_id")

        # 既に表示済みかチェック
        if await db.get_story_flag(user_id, story_id):
            continue

        # パターンマッチチェック
        if await db.check_death_pattern(user_id, pattern):
            await db.set_story_flag(user_id, story_id)
            return {
                "type": "story",
                "story_id": story_id,
                "data": pattern_data
            }

    return None


async def check_title_triggers(user_id):
    """称号解放トリガー"""
    from titles import TITLES

    for title_id, title_data in TITLES.items():
        # 既に持っているかチェック
        if await db.has_title(user_id, title_id):
            continue

        unlock_condition = title_data.get("unlock_condition", {})
        condition_type = unlock_condition.get("type")

        if condition_type == "enemy_deaths":
            enemy_name = unlock_condition.get("enemy_name")
            required_count = unlock_condition.get("count", 5)
            death_count = await db.get_death_count_by_enemy(user_id, enemy_name)

            if death_count >= required_count:
                # 称号付与
                await db.add_title(user_id, title_id, title_data.get("name"))
                return {
                    "type": "title",
                    "title_id": title_id,
                    "data": title_data
                }

        elif condition_type == "total_deaths":
            required_count = unlock_condition.get("count", 10)
            player = await db.get_player(user_id)
            total_deaths = player.get("total_deaths", 0) if player else 0

            if total_deaths >= required_count:
                await db.add_title(user_id, title_id, title_data.get("name"))
                return {
                    "type": "title",
                    "title_id": title_id,
                    "data": title_data
                }

        elif condition_type == "death_pattern":
            pattern = unlock_condition.get("pattern", [])
            if await db.check_death_pattern(user_id, pattern):
                await db.add_title(user_id, title_id, title_data.get("name"))
                return {
                    "type": "title",
                    "title_id": title_id,
                    "data": title_data
                }

    return None


# ==============================
# 統計取得
# ==============================

async def get_death_summary(user_id):
    """死亡統計サマリーを取得"""
    stats = await db.get_death_stats(user_id)
    player = await db.get_player(user_id)
    total_deaths = player.get("total_deaths", 0) if player else 0

    # トップ5の敵
    top_5 = list(stats.items())[:5]

    return {
        "total_deaths": total_deaths,
        "unique_enemies": len(stats),
        "top_killers": top_5,
        "all_stats": stats
    }


async def get_death_story_progress(user_id):
    """死亡ストーリーの進行状況を取得"""
    total_stories = len(DEATH_STORIES) + len(DEATH_PATTERNS)
    unlocked_count = 0

    for story_id in DEATH_STORIES.keys():
        if await db.get_story_flag(user_id, story_id):
            unlocked_count += 1

    for pattern_data in DEATH_PATTERNS.values():
        story_id = pattern_data.get("story_id")
        if await db.get_story_flag(user_id, story_id):
            unlocked_count += 1

    return {
        "unlocked": unlocked_count,
        "total": total_stories,
        "percentage": (unlocked_count / total_stories * 100) if total_stories > 0 else 0
    }