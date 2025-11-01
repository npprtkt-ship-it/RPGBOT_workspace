import logging  # ← 最初
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger("rpgbot")
logger.setLevel(logging.DEBUG)

logging.getLogger("discord").setLevel(logging.INFO)
logging.getLogger("discord.http").setLevel(logging.WARNING)

print("✅ ロギング設定完了")

import discord
from discord.ext import commands
import random
import asyncio
import os
from dotenv import load_dotenv
from aiohttp import web
import db
from db import get_player
import views
from views import (
    NameRequestView, 
    ResetConfirmView, 
    TreasureView, 
    BattleView,
    FinalBossBattleView,
    BossBattleView,
    SpecialEventView,
    TrapChestView
)
import game
from story import StoryView
import death_system
from titles import get_title_rarity_emoji, RARITY_COLORS

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

user_processing = {}
user_locks = {}

def get_user_lock(user_id: int) -> asyncio.Lock:
    """ユーザー別ロックを取得（なければ作成）"""
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]

from functools import wraps
def check_ban():
    """BAN確認デコレーター"""
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx: commands.Context, *args, **kwargs):
            user_id = str(ctx.author.id)

            # BAN確認
            if await db.is_player_banned(user_id):
                embed = discord.Embed(
                    title="❌ BOT利用禁止",
                    description="あなたはBOT利用禁止処分を受けています。\n\n運営チームにお問い合わせください。",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            return await func(ctx, *args, **kwargs)
        return wrapper
    return decorator

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


#スタート×チュートリアル開始
@bot.command(name="start")
@check_ban()
async def start(ctx: commands.Context):
    user = ctx.author
    user_id = str(user.id)

    # 処理中チェック
    if user_processing.get(user.id):
        await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
        return

    user_processing[user.id] = True
    try:
        # DBからプレイヤー取得
        player = await get_player(user_id)
        if player and player.get("name"):
            await ctx.send("⚠️ あなたはすでにゲームを開始しています！", delete_after=10)
            user_processing[user.id] = False
            return

        # プレイヤーデータが存在しない場合は作成
        if not player:
            await db.create_player(user.id)

        # カテゴリ検索 or 作成
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="RPG")
        if not category:
            category = await guild.create_category("RPG")

        # 【重要】ユーザーIDベースで既存チャンネルをチェック
        # トピックにユーザーIDを保存して検索
        existing_channel = None
        for ch in category.channels:
            if ch.topic and str(user.id) in ch.topic:
                existing_channel = ch
                break
        
        if existing_channel:
            await ctx.send(f"⚠️ すでにチャンネルが存在します: {existing_channel.mention}", delete_after=10)
            user_processing[user.id] = False
            return

        # チャンネル名を作成（表示名を使うが、IDで管理）
        channel_name = f"{user.name}-冒険"

        # パーミッション設定
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # 【重要】トピックにユーザーIDを保存
        channel = await guild.create_text_channel(
            channel_name, 
            category=category, 
            overwrites=overwrites,
            topic=f"UserID:{user.id}"  # ← ここでユーザーIDを保存
        )

        await ctx.send(f"✅ 冒険チャンネルを作成しました！ {channel.mention}", delete_after=10)

        # チャンネルにウェルカムメッセージ
        await channel.send(
            f"{user.mention} さん！ようこそ 🎉\nここはあなた専用の冒険チャンネルです。"
        )

        # 名前入力モーダルを表示
        embed = discord.Embed(
            title="📝 名前を入力しよう！",
            description="これからの冒険で使うキャラクター名を決めてね！",
            color=discord.Color.blue()
        )
        view = NameRequestView(user.id, channel)
        await channel.send(embed=embed, view=view)

        # 通知チャンネルへメッセージ送信
        try:
            notify_channel = bot.get_channel(1424712515396305007)
            if notify_channel:
                await notify_channel.send(
                    f"🎮 {user.mention} が新しい冒険を開始しました！"
                )
        except Exception as e:
            print(f"通知送信エラー: {e}")
    except Exception as e:
        print(f"!startコマンドエラー: {e}")
        await ctx.send(f"⚠️ エラーが発生しました: {e}", delete_after=10)
    finally:
        user_processing[user.id] = False



@bot.command(name="reset")
@check_ban()
async def reset(ctx: commands.Context):
    """2段階確認付きでプレイヤーデータと専用チャンネルを削除する"""
    user = ctx.author
    user_id = str(user.id)

    # 処理中チェック
    if user_processing.get(user.id):
        await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
        return

    player = await get_player(user_id)

    if not player:
        await ctx.send(embed=discord.Embed(title="未登録", description="あなたはまだゲームを開始していません。`!start` を使ってゲームを開始してください。", color=discord.Color.orange()))
        return

    embed = discord.Embed(
        title="データを削除しますか？",
        description="リセットするとプレイヤーデータは完全に削除されます。よろしいですか？\n\n※確認は2段階です。",
        color=discord.Color.red()
    )
    view = ResetConfirmView(user.id, None)
    await ctx.send(embed=embed, view=view)


#move
@bot.command(name="move")
@check_ban()
async def move(ctx: commands.Context):
    user = ctx.author

    # 処理中チェック
    if user_processing.get(user.id):
        await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
        return

    user_processing[user.id] = True
    view_delegated = False

    try:
        # プレイヤーデータチェック
        player = await get_player(user.id)
        if not player:
            await ctx.send("!start で冒険を始めてみてね。")
            return

        # クリア状態チェック
        if await db.is_game_cleared(user.id):
            embed = discord.Embed(
                title="🏆 ダンジョン制覇済み！",
                description="ダンジョンをクリアしました！\n\n次の冒険を始めるには `!reset` でデータをリセットしてください。\n\n使用可能なコマンド:\n• `!reset` - データをリセット\n• `!inventory` - インベントリ確認\n• `!status` - ステータス確認",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
            return

        # intro_2: 1回目の死亡後、最初のmove時に表示
        loop_count = await db.get_loop_count(user.id)
        intro_2_flag = await db.get_story_flag(user.id, "intro_2")

        # デバッグログ（本番環境では削除可能）
        print(f"[DEBUG] intro_2チェック - User: {user.id}, loop_count: {loop_count}, intro_2_flag: {intro_2_flag}")

        if loop_count == 1 and not intro_2_flag:
            print(f"[DEBUG] intro_2を表示します - User: {user.id}")
            embed = discord.Embed(
                title="📖 既視感",
                description="不思議な声が聞こえる…\n誰なんだ？この声の正体は……",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            await asyncio.sleep(2)

            view = StoryView(user.id, "intro_2", user_processing)
            await view.send_story(ctx)
            view_delegated = True
            return

        # 移動距離（5〜15m）
        distance = random.randint(5, 15)
        previous_distance = await db.get_previous_distance(user.id)
        total_distance = await db.add_player_distance(user.id, distance)

        current_floor = total_distance // 100 + 1
        current_stage = total_distance // 1000 + 1

        # 移動演出
        exploring_msg = await ctx.send(
            f"🚶‍♂️ ダンジョンを進んでいる…\n周囲は暗く静かだ……\n\n現在：第{current_floor}階層 / ステージ{current_stage}"
        )

        await asyncio.sleep(2.5)

        # ==========================
        # イベント分岐（通過判定方式）
        # ==========================

        # 通過したイベント距離を判定する関数
        def passed_through(event_distance):
            """前回の距離から今回の距離の間にevent_distanceを通過したか"""
            return previous_distance < event_distance <= total_distance

        # 優先度1: ボス戦（1000m毎）- 最優先
        boss_distances = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        for boss_distance in boss_distances:
            if passed_through(boss_distance):
                boss_stage = boss_distance // 1000

                # ボス未撃破の場合のみ処理
                if not await db.is_boss_defeated(user.id, boss_stage):
                    # boss_preストーリーチェック（未表示の場合のみ表示）
                    story_id = f"boss_pre_{boss_stage}"
                    if not await db.get_story_flag(user.id, story_id):
                        # ラスボス判定（10000m）
                        if boss_stage == 10:
                            embed = discord.Embed(
                                title="📖 運命の時",
                                description="強大な気配を感じる…なにが来るんだ？",
                                color=discord.Color.purple()
                            )
                        else:
                            embed = discord.Embed(
                                title="📖 試練の予兆",
                                description="強大な存在の気配を感じる…気を引き締めて……",
                                color=discord.Color.purple()
                            )

                        await exploring_msg.edit(content=None, embed=embed)
                        await asyncio.sleep(2)

                        # ストーリー完了後にボス戦を開始するコールバックを設定
                        view = StoryView(user.id, story_id, user_processing, 
                                        callback_data={
                                            'type': 'boss_battle',
                                            'boss_stage': boss_stage,
                                            'ctx': ctx
                                        })
                        await view.send_story(ctx)
                        view_delegated = True
                        return

                    # ストーリー表示済みの場合、ボス戦に進む
                    boss = game.get_boss(boss_stage)
                    if boss:
                        player_data = {
                            "hp": player.get("hp", 50),
                            "mp": player.get("mp", 20),
                            "attack": player.get("atk", 5),
                            "defense": player.get("def", 2),
                            "inventory": player.get("inventory", []),
                            "distance": total_distance,
                            "user_id": user.id
                        }

                        # ラスボス判定（10000m）
                        if boss_stage == 10:
                            embed = discord.Embed(
                                title="⚔️ ラスボス出現！",
                                description=f"**{boss['name']}** が最後の戦いに臨む！\n\nこれが最終決戦だ…！",
                                color=discord.Color.dark_gold()
                            )
                            await exploring_msg.edit(content=None, embed=embed)
                            await asyncio.sleep(3)

                            view = await FinalBossBattleView.create(ctx, player_data, boss, user_processing, boss_stage)
                            await view.send_initial_embed()
                            view_delegated = True
                            return
                        else:
                            embed = discord.Embed(
                                title="⚠️ ボス出現！",
                                description=f"**{boss['name']}** が目の前に立ちはだかる！",
                                color=discord.Color.dark_red()
                            )
                            await exploring_msg.edit(content=None, embed=embed)
                            await asyncio.sleep(2)

                            view = await BossBattleView.create(ctx, player_data, boss, user_processing, boss_stage)
                            await view.send_initial_embed()
                            view_delegated = True
                            return

        # 優先度2: 特殊イベント（500m毎、1000m除く）
        special_distances = [500, 1500, 2500, 3500, 4500, 5500, 6500, 7500, 8500, 9500]
        for special_distance in special_distances:
            if passed_through(special_distance):
                view = SpecialEventView(user.id, user_processing, special_distance)
                embed = discord.Embed(
                    title="✨ 特殊な雰囲気の場所だ……",
                    description="何が起こるのだろうか？",
                    color=discord.Color.purple()
                )
                embed.set_footer(text=f"📏 現在の距離: {special_distance}m")
                await exploring_msg.edit(content=None, embed=embed, view=view)
                view_delegated = True
                return

        # 優先度3: 距離ベースストーリー（250m, 750m, 1250m, etc.）
        story_distances = [250, 750, 1250, 1750, 2250, 2750, 3250, 3750, 4250, 4750, 5250, 5750, 6250, 6750, 7250, 7750, 8250, 8750, 9250, 9750]
        for story_distance in story_distances:
            if passed_through(story_distance):
                # 周回数に応じたストーリーIDを生成
                story_id = f"story_{story_distance}"
                if loop_count >= 2:
                    loop_story_id = f"story_{story_distance}_loop{loop_count}"
                    # 周回専用ストーリーが存在するかチェック
                    if not await db.get_story_flag(user.id, loop_story_id):
                        story_id = loop_story_id

                if not await db.get_story_flag(user.id, story_id):
                    embed = discord.Embed(
                        title="📖 探索中に何かを見つけた",
                        description="不思議な出来事が起こる予感…",
                        color=discord.Color.purple()
                    )
                    await exploring_msg.edit(content=None, embed=embed)
                    await asyncio.sleep(2)

                    view = StoryView(user.id, story_id, user_processing)
                    await view.send_story(ctx)
                    view_delegated = True
                    return

        # 優先度4: 超低確率で選択肢分岐ストーリー（3%）
        choice_story_roll = random.random() * 100
        if choice_story_roll < 0.1:
            # 選択肢ストーリーのリスト
            choice_story_ids = [
                "choice_mysterious_door",
                "choice_strange_merchant",
                "choice_fork_road",
                "choice_mysterious_well",
                "choice_sleeping_dragon",
                "choice_cursed_treasure",
                "choice_time_traveler",
                "choice_fairy_spring"
            ]

            # 未体験の選択肢ストーリーをフィルタリング
            available_stories = []
            for sid in choice_story_ids:
                if not await db.get_story_flag(user.id, sid):
                    available_stories.append(sid)

            # 未体験のストーリーがある場合、ランダムに選択
            if available_stories:
                selected_story_id = random.choice(available_stories)

                embed = discord.Embed(
                    title="✨ イベント発生！",
                    description="運命の分岐点が現れた…",
                    color=discord.Color.gold()
                )
                await exploring_msg.edit(content=None, embed=embed)
                await asyncio.sleep(2)

                view = StoryView(user.id, selected_story_id, user_processing)
                await view.send_story(ctx)
                view_delegated = True
                return

        # 優先度5: 通常イベント抽選（60%何もなし/30%敵/9%宝箱/1%トラップ宝箱）
        event_roll = random.random() * 100

        # 1% トラップ宝箱
        if event_roll < 1:
            embed = discord.Embed(
                title="⚠️ 宝箱を見つけた！",
                description="何か罠が仕掛けられているような気がする…\nどうする？",
                color=discord.Color.gold()
            )
            embed.set_footer(text=f"📏 現在の距離: {total_distance}m")
            view = TrapChestView(user.id, user_processing, player)
            await exploring_msg.edit(content=None, embed=embed, view=view)
            view_delegated = True
            return

        # 9% 宝箱（1～10%）
        elif event_roll < 10:
            embed = discord.Embed(
                title="⚠️ 宝箱を見つけた！",
                description="何か罠が仕掛けられているような気がする…\nどうする？",
                color=discord.Color.gold()
            )
            embed.set_footer(text=f"📏 現在の距離: {total_distance}m")
            view = TreasureView(user.id, user_processing)
            await exploring_msg.edit(content=None, embed=embed, view=view)
            view_delegated = True
            return
        # 30% 敵との遭遇（10～40%）
        elif event_roll < 40:
            # game.pyから距離に応じた敵を取得
            enemy = game.get_random_enemy(total_distance)

            player_data = {
                "hp": player.get("hp", 50),
                "mp": player.get("mp", 20),
                "attack": player.get("atk", 5),
                "defense": player.get("def", 2),
                "inventory": player.get("inventory", []),
                "distance": total_distance,
                "user_id": user.id
            }

            # 戦闘Embed呼び出し
            await exploring_msg.edit(content="⚔️ 敵が現れた！ 戦闘開始！")
            view = await BattleView.create(ctx, player_data, enemy, user_processing)
            await view.send_initial_embed()
            view_delegated = True
            return

        # 3. 何もなし
        embed = discord.Embed(
            title="📜 探索結果",
            description=f"→ {distance}m進んだ！\n何も見つからなかったようだ。",
            color=discord.Color.dark_grey()
        )
        embed.set_footer(text=f"📏 現在の距離: {total_distance}m")
        await exploring_msg.edit(content=None, embed=embed)
    finally:
        # Viewに委譲していない場合のみクリア（View自身がクリアする責任を持つ）
        if not view_delegated:
            user_processing[user.id] = False


# インベントリ
@bot.command()
@check_ban()
async def inventory(ctx):
    # 処理中チェック
    if user_processing.get(ctx.author.id):
        await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
        return

    player = await db.get_player(ctx.author.id)
    if not player:
        await ctx.send("!start で冒険を始めてね。")
        return

    view = views.InventorySelectView(player)
    await ctx.send("🎒 インベントリ", view=view)

# ステータス&装備
@bot.command()
@check_ban()
async def status(ctx):
    try:
        # 他処理中チェック
        if 'user_processing' in globals() and user_processing.get(ctx.author.id):
            await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
            return

        # プレイヤー情報取得
        player = None
        if 'db' in globals():
            player = await db.get_player(ctx.author.id)

        if not player:
            await ctx.send("!start で冒険を始めてね。")
            return

        # 装備情報取得
        equipped = {"weapon": "なし", "armor": "なし"}
        if 'db' in globals():
            temp = await db.get_equipped_items(ctx.author.id)
            if isinstance(temp, dict):
                equipped["weapon"] = str(temp.get("weapon") or "なし")
                equipped["armor"] = str(temp.get("armor") or "なし")

        # 装備ボーナスを計算
        import game
        equipment_bonus = await game.calculate_equipment_bonus(ctx.author.id)
        base_attack = player.get("atk", 5)
        base_defense = player.get("def", 2)
        total_attack = base_attack + equipment_bonus.get("attack_bonus", 0)
        total_defense = base_defense + equipment_bonus.get("defense_bonus", 0)

        # Embed作成
        embed = discord.Embed(title="📊 ステータス", color=discord.Color.blue())
        embed.add_field(name="名前", value=str(player.get("name", "未設定")), inline=True)
        embed.add_field(name="レベル", value=str(player.get("level", 1)), inline=True)
        embed.add_field(name="距離", value=f"{player.get('distance', 0)}m", inline=True)
        embed.add_field(name="HP", value=f"{player.get('hp', 50)}/{player.get('max_hp', 50)}", inline=True)
        embed.add_field(name="MP", value=f"{player.get('mp', 20)}/{player.get('max_mp', 20)}", inline=True)
        embed.add_field(name="EXP", value=f"{player.get('exp', 0)}/{db.get_required_exp(player.get('level', 1))}", inline=True)
        embed.add_field(name="攻撃力", value=f"{total_attack} ({base_attack}+{equipment_bonus.get('attack_bonus', 0)})", inline=True)
        embed.add_field(name="防御力", value=f"{total_defense} ({base_defense}+{equipment_bonus.get('defense_bonus', 0)})", inline=True)
        embed.add_field(name="所持金", value=f'{player.get("gold", 0)}G', inline=True)
        embed.add_field(name="装備武器", value=equipped["weapon"], inline=True)
        embed.add_field(name="装備防具", value=equipped["armor"], inline=True)

        # 装備変更UIを追加
        player_with_id = player.copy()
        player_with_id["user_id"] = ctx.author.id
        equip_view = views.EquipmentSelectView(player_with_id)

        await ctx.send(embed=embed, view=equip_view)

    except Exception as e:
        # エラー時はBotが落ちずに報告
        await ctx.send(f"⚠️ ステータス取得中にエラーが発生しました: {e}")
        print(f"statusコマンドエラー: {e}")

# アップグレード
@bot.command()
@check_ban()
async def upgrade(ctx):
    if user_processing.get(ctx.author.id):
        await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
        return

    player = await db.get_player(ctx.author.id)
    if not player:
        await ctx.send("!start で冒険を始めてね。")
        return

    # クリア状態チェック
    if await db.is_game_cleared(ctx.author.id):
        embed = discord.Embed(
            title="⚠️ ダンジョン踏破済",
            description="あなたはダンジョンをクリアしています！\n`!reset` で'データをリセットして再度冒険を初めてください。\n\n※周回システムは実装予定です。アップデートにご期待ください！",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return

    points = player.get("upgrade_points", 0)
    upgrades = await db.get_upgrade_levels(ctx.author.id)
    
    # 動的コストを取得
    cost_hp = await db.get_upgrade_cost(1, ctx.author.id)
    cost_mp = await db.get_upgrade_cost(2, ctx.author.id)
    cost_coin = await db.get_upgrade_cost(3, ctx.author.id)
    cost_atk = await db.get_upgrade_cost(4, ctx.author.id)
    cost_def = await db.get_upgrade_cost(5, ctx.author.id)

    embed = discord.Embed(title="⬆️ アップグレード", description=f"所持ポイント: **{points}**", color=0xFFD700)
    embed.add_field(
        name=f"1️⃣ HP最大値アップ ({cost_hp}ポイント)",
        value=f"現在Lv.{upgrades['max_hp']} → 最大HP +5",
        inline=False
    )
    embed.add_field(
        name=f"2️⃣ MP最大値アップ ({cost_mp}ポイント)",
        value=f"現在Lv.{upgrades['max_mp']} → 最大MP +5",
        inline=False
    )
    embed.add_field(
        name=f"3️⃣ コイン取得量アップ ({cost_coin}ポイント)",
        value=f"現在Lv.{upgrades['coin_gain']} → コイン +10%",
        inline=False
    )
    embed.add_field(
        name=f"4️⃣ 攻撃力初期値アップ ({cost_atk}ポイント)",
        value=f"現在Lv.{upgrades['atk']} → ATK +1",
        inline=False
    )
    embed.add_field(
        name=f"5️⃣ 防御力初期値アップ ({cost_def}ポイント)",
        value=f"現在Lv.{upgrades['def_upgrade']} → DEF +1",
        inline=False
    )
    embed.set_footer(text="!buy_upgrade <番号> でアップグレード購入")

    await ctx.send(embed=embed)

# アップグレード購入
@bot.command()
@check_ban()
async def buy_upgrade(ctx, upgrade_type: int):
    if user_processing.get(ctx.author.id):
        await ctx.send("⚠️ 別の処理が実行中です。完了するまでお待ちください。", delete_after=5)
        return

    player = await db.get_player(ctx.author.id)
    if not player:
        await ctx.send("!start で冒険を始めてね。")
        return

    # クリア状態チェック
    if await db.is_game_cleared(ctx.author.id):
        embed = discord.Embed(
            title="⚠️ ダンジョン踏破済",
            description="あなたはダンジョンをクリアしています！\n`!reset` で'データをリセットして再度冒険を初めてください。\n\n※周回システムは実装予定です。アップデートにご期待ください！",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return

    if upgrade_type not in [1, 2, 3, 4, 5]:
        await ctx.send("無効なアップグレード番号です。1〜5から選んでください。")
        return

    # 動的コストを取得
    cost = await db.get_upgrade_cost(upgrade_type, ctx.author.id)
    points = player.get("upgrade_points", 0)

    if points < cost:
        await ctx.send(f"ポイントが足りません！必要: {cost}ポイント、所持: {points}ポイント")
        return

    if upgrade_type == 1:
        await db.upgrade_initial_hp(ctx.author.id)
        await db.spend_upgrade_points(ctx.author.id, cost)
        await ctx.send("✅ HP最大値をアップグレードしました！ 最大HP +5")
    elif upgrade_type == 2:
        await db.upgrade_initial_mp(ctx.author.id)
        await db.spend_upgrade_points(ctx.author.id, cost)
        await ctx.send("✅ MP最大値をアップグレードしました！ 最大MP +5")
    elif upgrade_type == 3:
        await db.upgrade_coin_gain(ctx.author.id)
        await db.spend_upgrade_points(ctx.author.id, cost)
        await ctx.send("✅ コイン取得量をアップグレードしました！ コイン取得 +10%")
    elif upgrade_type == 4:
        await db.upgrade_atk(ctx.author.id)
        await db.spend_upgrade_points(ctx.author.id, cost)
        await ctx.send("✅ 攻撃力初期値をアップグレードしました！ ATK +1")
    elif upgrade_type == 5:
        await db.upgrade_def(ctx.author.id)
        await db.spend_upgrade_points(ctx.author.id, cost)
        await ctx.send("✅ 防御力初期値をアップグレードしました！ DEF +1")

# デバッグコマンドの読み込み（削除可能）
try:
    import debug_commands
    debug_commands.setup(bot, user_processing)
    print("✅ デバッグコマンドを読み込みました")
except ImportError:
    print("ℹ️ デバッグコマンドは利用できません（debug_commands.py が見つかりません）")
except Exception as e:
    print(f"⚠️ デバッグコマンドの読み込みエラー: {e}")

import asyncio
from aiohttp import web

async def health_check(request):
    return web.Response(text="OK", status=200)

async def run_health_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    print("✅ ヘルスチェックサーバーを起動しました (ポート 8000)")

async def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ エラー: DISCORD_BOT_TOKEN 環境変数が設定されていません")
        exit(1)

    # Health server を起動してから Bot を起動
    await run_health_server()

    print("🤖 Discord BOTを起動します...")
    async with bot:
        await bot.start(token)


@bot.command(name="servers")
async def show_servers(ctx: commands.Context):
    """BOTが参加しているサーバー一覧を表示(開発者用・ページネーション付き)"""

    # 開発者のみ実行可能にする
    DEVELOPER_ID = "1301416493401243694"  # あなたのDiscord ID

    if str(ctx.author.id) != DEVELOPER_ID:
        await ctx.send("❌ このコマンドは開発者のみ実行できます")
        return

    guilds_list = list(bot.guilds)
    total_servers = len(guilds_list)

    if total_servers == 0:
        await ctx.send("📭 BOTはどのサーバーにも参加していません")
        return

    # ページネーション用のView
    class ServerListView(discord.ui.View):
        def __init__(self, guilds, user_id):
            super().__init__(timeout=180)  # 3分でタイムアウト
            self.guilds = guilds
            self.user_id = user_id
            self.current_page = 0
            self.max_page = (len(guilds) - 1) // 10

            # 最初のページでは前のページボタンを無効化
            self.update_buttons()

        def update_buttons(self):
            """ボタンの有効/無効を更新"""
            self.children[0].disabled = (self.current_page == 0)  # 前へボタン
            self.children[1].disabled = (self.current_page >= self.max_page)  # 次へボタン

        def create_embed(self):
            """現在のページのEmbedを作成"""
            start_idx = self.current_page * 10
            end_idx = min(start_idx + 10, len(self.guilds))

            embed = discord.Embed(
                title="🌐 BOTが参加しているサーバー",
                description=f"合計: **{len(self.guilds)}** サーバー",
                color=discord.Color.blue()
            )

            for guild in self.guilds[start_idx:end_idx]:
                embed.add_field(
                    name=f"📍 {guild.name}",
                    value=f"ID: `{guild.id}`\nメンバー: {guild.member_count}人",
                    inline=False
                )

            embed.set_footer(text=f"ページ {self.current_page + 1} / {self.max_page + 1}")
            return embed

        @discord.ui.button(label="◀ 前へ", style=discord.ButtonStyle.primary)
        async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # 実行者チェック
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ このボタンは実行者のみ操作できます", ephemeral=True)
                return

            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

        @discord.ui.button(label="次へ ▶", style=discord.ButtonStyle.primary)
        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # 実行者チェック
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ このボタンは実行者のみ操作できます", ephemeral=True)
                return

            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)

        @discord.ui.button(label="❌ 閉じる", style=discord.ButtonStyle.danger)
        async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # 実行者チェック
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ このボタンは実行者のみ操作できます", ephemeral=True)
                return

            await interaction.message.delete()

    # Viewとメッセージを送信
    view = ServerListView(guilds_list, str(ctx.author.id))
    await ctx.send(embed=view.create_embed(), view=view)


@bot.command(name="death_stats")
@check_ban()
async def death_stats(ctx: commands.Context):
    """死亡統計を表示"""
    user = ctx.author
    player = await get_player(user.id)

    if not player:
        await ctx.send("!start で冒険を始めてみてね。")
        return

    import death_system

    summary = await death_system.get_death_summary(user.id)
    total_deaths = summary.get("total_deaths", 0)
    top_killers = summary.get("top_killers", [])

    if total_deaths == 0:
        embed = discord.Embed(
            title="💀 死亡統計",
            description="まだ一度も死亡していません。\n\n慎重な冒険者ですね！",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return

    # トップ5の敵を表示
    killer_list = ""
    for i, (enemy_name, count) in enumerate(top_killers[:5], 1):
        killer_list += f"{i}. **{enemy_name}** - {count}回\n"

    if not killer_list:
        killer_list = "データがありません"

    embed = discord.Embed(
        title=f"💀 {player.get('name', 'あなた')}の死亡統計",
        description=f"総死亡回数: **{total_deaths}回**\n\n## よく殺された敵 TOP5\n{killer_list}",
        color=discord.Color.red()
    )

    # ストーリー進行状況
    story_progress = await death_system.get_death_story_progress(user.id)
    embed.add_field(
        name="📖 死亡ストーリー進行",
        value=f"{story_progress['unlocked']}/{story_progress['total']} ({story_progress['percentage']:.1f}%)",
        inline=True
    )

    embed.set_footer(text="!death_history で詳細な履歴を確認できます")

    await ctx.send(embed=embed)

@bot.command(name="death_history")
@check_ban()
async def death_history(ctx: commands.Context, limit: int = 10):
    """最近の死亡履歴を表示"""
    user = ctx.author
    player = await get_player(user.id)

    if not player:
        await ctx.send("!start で冒険を始めてみてね。")
        return

    if limit < 1 or limit > 50:
        await ctx.send("⚠️ 表示件数は1〜50の範囲で指定してください。")
        return

    recent_deaths = await db.get_recent_deaths(user.id, limit)

    if not recent_deaths:
        embed = discord.Embed(
            title="💀 死亡履歴",
            description="まだ一度も死亡していません。",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return

    # 履歴をフォーマット
    history_text = ""
    for i, death in enumerate(recent_deaths, 1):
        enemy_name = death.get("enemy_name", "不明")
        distance = death.get("distance", 0)
        floor = death.get("floor", 0)
        enemy_type_icon = "👑" if death.get("enemy_type") == "boss" else "⚔️"

        history_text += f"{i}. {enemy_type_icon} **{enemy_name}** ({distance}m / {floor}階層)\n"

    embed = discord.Embed(
        title=f"💀 最近の死亡履歴 (直近{len(recent_deaths)}件)",
        description=history_text,
        color=discord.Color.dark_red()
    )

    embed.set_footer(text="!death_stats で統計を確認できます")

    await ctx.send(embed=embed)

@bot.command(name="titles")
@check_ban()
async def titles(ctx: commands.Context):
    """所持している称号を表示"""
    user = ctx.author
    player = await get_player(user.id)

    if not player:
        await ctx.send("!start で冒険を始めてみてね。")
        return

    from titles import get_title_rarity_emoji, RARITY_COLORS

    player_titles = await db.get_player_titles(user.id)
    active_title = await db.get_active_title(user.id)

    if not player_titles:
        embed = discord.Embed(
            title="🏆 称号一覧",
            description="まだ称号を獲得していません。\n\n特定の条件を満たすと称号が解放されます。",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return

    # レアリティ別に分類
    from titles import TITLES
    rarity_order = ["mythic", "legendary", "epic", "rare", "uncommon", "common"]

    title_text = ""
    for rarity in rarity_order:
        rarity_titles = [t for t in player_titles if TITLES.get(t['title_id'], {}).get('rarity') == rarity]

        if rarity_titles:
            rarity_name = {
                "mythic": "神話",
                "legendary": "伝説",
                "epic": "叙事詩",
                "rare": "レア",
                "uncommon": "アンコモン",
                "common": "コモン"
            }.get(rarity, rarity)

            for title in rarity_titles:
                emoji = get_title_rarity_emoji(title['title_id'])
                title_name = title['title_name']
                is_active = "【装備中】" if title_name == active_title else ""
                title_text += f"{emoji} **{title_name}** {is_active}\n"

    embed = discord.Embed(
        title=f"🏆 {player.get('name', 'あなた')}の称号一覧 ({len(player_titles)}個)",
        description=title_text or "称号がありません",
        color=discord.Color.gold()
    )

    embed.set_footer(text="!equip_title <称号名> で称号を装備できます")

    await ctx.send(embed=embed)

@bot.command(name="equip_title")
@check_ban()
async def equip_title(ctx: commands.Context, *, title_name: str = None):
    """称号を装備する"""
    user = ctx.author
    player = await get_player(user.id)

    if not player:
        await ctx.send("!start で冒険を始めてみてね。")
        return

    if not title_name:
        await ctx.send("⚠️ 使い方: `!equip_title <称号名>`")
        return

    # 称号を持っているか確認
    player_titles = await db.get_player_titles(user.id)
    matching_title = None

    for title in player_titles:
        if title['title_name'].lower() == title_name.lower():
            matching_title = title
            break

    if not matching_title:
        await ctx.send(f"⚠️ 称号 `{title_name}` を所持していません。\n\n`!titles` で所持称号を確認できます。")
        return

    # 称号を装備
    success = await db.set_active_title(user.id, matching_title['title_id'])

    if success:
        from titles import get_title_rarity_emoji
        embed = discord.Embed(
            title="✅ 称号を装備しました",
            description=f"{get_title_rarity_emoji(matching_title['title_id'])} **{matching_title['title_name']}** を装備中",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("⚠️ 称号の装備に失敗しました。")


@bot.command(name="unequip_title")
@check_ban()
async def unequip_title(ctx: commands.Context):
    """称号を外す"""
    user = ctx.author
    player = await get_player(user.id)

    if not player:
        await ctx.send("!start で冒険を始めてみてね。")
        return

    await db.unequip_title(user.id)

    embed = discord.Embed(
        title="✅ 称号を外しました",
        description="現在、称号を装備していません。",
        color=discord.Color.grey()
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    asyncio.run(main())
