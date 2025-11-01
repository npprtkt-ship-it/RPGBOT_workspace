"""
称号システム - 称号データと解放条件
"""

# ==============================
# 称号データベース（Lv2: 称号解放）
# ==============================

TITLES = {
    # 基本的な称号（死亡回数ベース）
    "death_novice": {
        "id": "death_novice",
        "name": "死の初心者",
        "description": "10回死亡した者に与えられる称号",
        "unlock_condition": {
            "type": "total_deaths",
            "count": 10
        },
        "effect": None,  # Lv2では効果なし、Lv3で実装
        "rarity": "common"
    },

    "death_expert": {
        "id": "death_expert",
        "name": "死の熟練者",
        "description": "50回死亡した者に与えられる称号",
        "unlock_condition": {
            "type": "total_deaths",
            "count": 50
        },
        "effect": None,
        "rarity": "uncommon"
    },

    "death_master": {
        "id": "death_master",
        "name": "死の達人",
        "description": "100回死亡した者に与えられる称号",
        "unlock_condition": {
            "type": "total_deaths",
            "count": 100
        },
        "effect": None,
        "rarity": "rare"
    },

    # 敵別称号
    "slime_victim": {
        "id": "slime_victim",
        "name": "スライムの餌食",
        "description": "スライムに5回殺された者に与えられる不名誉な称号",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "スライム",
            "count": 5
        },
        "effect": None,
        "rarity": "common"
    },

    "slime_friend": {
        "id": "slime_friend",
        "name": "スライムの友",
        "description": "スライムに15回殺された者。もはや友情すら感じる",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "スライム",
            "count": 15
        },
        "effect": None,
        "rarity": "rare"
    },

    "goblin_toy": {
        "id": "goblin_toy",
        "name": "ゴブリンの玩具",
        "description": "ゴブリンに10回殺された者に与えられる称号",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "ゴブリン",
            "count": 10
        },
        "effect": None,
        "rarity": "uncommon"
    },

    "skeleton_curse": {
        "id": "skeleton_curse",
        "name": "骨の呪い",
        "description": "スケルトンに10回殺された者に与えられる称号",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "スケルトン",
            "count": 10
        },
        "effect": None,
        "rarity": "uncommon"
    },

    "vampire_blood": {
        "id": "vampire_blood",
        "name": "吸血鬼の血袋",
        "description": "吸血鬼に10回血を吸われた者に与えられる称号",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "吸血鬼",
            "count": 10
        },
        "effect": None,
        "rarity": "rare"
    },

    # ボス特化称号
    "boss_challenge": {
        "id": "boss_challenge",
        "name": "ボス挑戦者",
        "description": "スライムキングに3回挑んで散った者",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "スライムキング",
            "count": 3
        },
        "effect": None,
        "rarity": "uncommon"
    },

    "golem_wall": {
        "id": "golem_wall",
        "name": "ゴーレムの壁",
        "description": "ゴーレムに5回砕かれた者",
        "unlock_condition": {
            "type": "enemy_deaths",
            "enemy_name": "ゴーレム",
            "count": 5
        },
        "effect": None,
        "rarity": "rare"
    },

    # パターン称号
    "slime_hell": {
        "id": "slime_hell",
        "name": "スライム地獄",
        "description": "3連続でスライムに殺された不運な者",
        "unlock_condition": {
            "type": "death_pattern",
            "pattern": ["スライム", "スライム", "スライム"]
        },
        "effect": None,
        "rarity": "uncommon"
    },

    "boss_pilgrim": {
        "id": "boss_pilgrim",
        "name": "ボス巡礼者",
        "description": "連続でボスに殺された挑戦者",
        "unlock_condition": {
            "type": "death_pattern",
            "pattern": ["スライムキング", "ゴーレム", "闇の騎士"]
        },
        "effect": None,
        "rarity": "epic"
    },

    "undead_cursed": {
        "id": "undead_cursed",
        "name": "不死者の呪い",
        "description": "アンデッド系に連続で殺された者。体が冷たい",
        "unlock_condition": {
            "type": "death_pattern",
            "pattern": ["スケルトン", "ゾンビ", "幽霊"]
        },
        "effect": None,
        "rarity": "rare"
    },

    "equal_death": {
        "id": "equal_death",
        "name": "平等な死",
        "description": "様々な敵に分け隔てなく殺された者",
        "unlock_condition": {
            "type": "death_pattern",
            "pattern": ["スライム", "ゴブリン", "スケルトン", "ゾンビ", "吸血鬼"]
        },
        "effect": None,
        "rarity": "epic"
    },

    # 特殊称号
    "immortal_seeker": {
        "id": "immortal_seeker",
        "name": "不死の探求者",
        "description": "死を恐れず、死から学ぶ者",
        "unlock_condition": {
            "type": "total_deaths",
            "count": 200
        },
        "effect": None,
        "rarity": "legendary"
    },

    "death_memory": {
        "id": "death_memory",
        "name": "死の記憶",
        "description": "全ての死を記憶する者。未来で効果を発揮する",
        "unlock_condition": {
            "type": "total_deaths",
            "count": 30
        },
        "effect": "future_bonus",  # Lv3で実装予定
        "rarity": "epic"
    },

    # 隠し称号（真END用、Lv3実装予定）
    "world_observer": {
        "id": "world_observer",
        "name": "世界の観測者",
        "description": "死を超越し、世界の真実を見た者",
        "unlock_condition": {
            "type": "special",  # 特殊条件（後で実装）
            "requirement": "true_ending_flag"
        },
        "effect": "world_change",
        "rarity": "mythic"
    }
}

# ==============================
# レアリティ設定
# ==============================

RARITY_COLORS = {
    "common": 0x808080,      # グレー
    "uncommon": 0x00ff00,    # 緑
    "rare": 0x0080ff,        # 青
    "epic": 0x8000ff,        # 紫
    "legendary": 0xff8000,   # オレンジ
    "mythic": 0xff0080       # ピンク
}

RARITY_EMOJI = {
    "common": "⚪",
    "uncommon": "🟢",
    "rare": "🔵",
    "epic": "🟣",
    "legendary": "🟠",
    "mythic": "🌸"
}

# ==============================
# ヘルパー関数
# ==============================

def get_title_info(title_id):
    """称号情報を取得"""
    return TITLES.get(title_id, None)

def get_title_rarity_color(title_id):
    """称号のレアリティカラーを取得"""
    title = TITLES.get(title_id)
    if title:
        rarity = title.get("rarity", "common")
        return RARITY_COLORS.get(rarity, 0x808080)
    return 0x808080

def get_title_rarity_emoji(title_id):
    """称号のレアリティ絵文字を取得"""
    title = TITLES.get(title_id)
    if title:
        rarity = title.get("rarity", "common")
        return RARITY_EMOJI.get(rarity, "⚪")
    return "⚪"

def get_all_titles_by_rarity():
    """レアリティ別に称号を取得"""
    sorted_titles = {
        "mythic": [],
        "legendary": [],
        "epic": [],
        "rare": [],
        "uncommon": [],
        "common": []
    }

    for title_id, title_data in TITLES.items():
        rarity = title_data.get("rarity", "common")
        sorted_titles[rarity].append(title_data)

    return sorted_titles