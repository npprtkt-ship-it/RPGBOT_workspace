import random
import copy

ITEMS_DATABASE = {
    "none": {
    },

        # ======
        # 回復薬
        # ======
    
    "HP回復薬（小）": {
        "type": "potion",
        "effect": "HP+30",
        "ability": "HP回復",
        "description": "HPを30回復する薬。",
        "price": 30
    },
    "HP回復薬（中）": {
        "type": "potion",
        "effect": "HP+80",
        "ability": "HP中回復",
        "description": "HPを80回復する高級な薬。",
        "price": 80
    },
    "HP回復薬（大）": {
        "type": "potion",
        "effect": "HP+200",
        "ability": "HP大回復",
        "description": "HPを200回復する貴重な薬。",
        "price": 200
    },
    "MP回復薬（小）": {
        "type": "potion",
        "effect": "MP+15",
        "ability": "MP回復",
        "description": "MPを15回復する薬。",
        "price": 30
    },
    "MP回復薬（中）": {
        "type": "potion",
        "effect": "MP+40",
        "ability": "MP中回復",
        "description": "MPを40回復する高級な薬。",
        "price": 80
    },
    "MP回復薬（大）": {
        "type": "potion",
        "effect": "MP+100",
        "ability": "MP大回復",
        "description": "MPを100回復する貴重な薬。",
        "price": 200
    },
    "エリクサー": {
        "type": "potion",
        "effect": "HPMPMAX",
        "ability": "HP・MP完全回復",
        "description": "HPとMPを完全回復させる幻の秘薬",
    },

        # ====
        # 武器
        # ====
    
    "木の剣": {
        "type": "weapon",
        "attack": 2,
        "ability": "なし",
        "description": "初心者向けの木製の剣。軽くて扱いやすい。",
        "price": 20
    },
    "石の剣": {
        "type": "weapon",
        "attack": 4,
        "ability": "なし",
        "description": "石で作られた剣。木の剣より頑丈。",
        "price": 30
    },
    "鉄の剣": {
        "type": "weapon",
        "attack": 6,
        "ability": "なし",
        "description": "鉄製の剣。切れ味が良い。",
        "price": 50
    },
    "毒針": {
        "type": "weapon",
        "attack": 1,
        "ability": "毒付与(20%の確率で毒付与), 急所突き(2%の確率で即死)",
        "description": "毒が塗られた針。相手を弱らせる。",
        "price": 300
    },
    "黄金の剣": {
        "type": "weapon",
        "attack": 15,
        "ability": "全ステータス+50%, 攻撃時50%で防御無視",
        "description": "黄金に輝く剣。第1ステージ「始まりの洞窟」の激レア武器。",
    },
    "岩石の剣": {
        "type": "weapon",
        "attack": 8,
        "ability": "ダメージ+30%, 攻撃時50%で防御無視",
        "description": "洞窟の主-ストーンスネーク-の鱗に深く突き立てられ長い年月が経ち、刀身が鱗と同化した剣。",
        
    },

        # ====
        # 防具
        # ====
    
    "革の盾": {
        "type": "armor",
        "defense": 1,
        "ability": "なし",
        "description": "革製の盾。何も装備しないよりはいい。",
        "price": 20
    },
    "木の盾": {
        "type": "armor",
        "defense": 2,
        "ability": "なし",
        "description": "木製の盾。簡素だが軽い。",
        "price": 40
    },
    "石の盾": {
        "type": "armor",
        "defense": 4,
        "ability": "なし",
        "description": "石で作られた盾。頑丈。",
        "price": 80
    },
    "鉄の盾": {
        "type": "armor",
        "defense": 7,
        "ability": "なし",
        "description": "鉄製の盾。高い防御力を持つ。",
        "price": 124
    },
    "黄金の盾": {
        "type": "armor",
        "defense": 10,
        "ability": "被攻撃時50%の確率でダメージ無効",
        "description": "黄金に輝く盾。第1ステージ「始まりの洞窟」の激レア防具。",
    },
    "スライムの王冠": {
        "type": "armor",
        "defense": 5,
        "ability": "HP+30",
        "description": "スライムキングが落とした王冠。生命力が強くなる。",
        "price": 80
    }, 
    "呪いの首輪": {
        "type": "armor",
        "defense": -10,
        "ability": "攻撃力+50%（デバフ防具）",
        "description": "装備者の防御を下げるが、攻撃力が大幅に上がる呪われた首輪。",
        "price": 50
    },
    "重い鎖": {
        "type": "armor",
        "defense": -5,
        "ability": "HP+100、移動速度-20%（デバフ防具）",
        "description": "重い鎖。防御は下がるがHPが増加する。",
        "price": 25
    },
    "破滅の兜": {
        "type": "armor",
        "defense": -15,
        "ability": "クリティカル率+30%（デバフ防具）",
        "description": "防御を犠牲にクリティカル率を大幅に上げる危険な兜。",
        "price": 75
    },
    "狂戦士の鎧": {
        "type": "armor",
        "defense": -20,
        "ability": "攻撃力+100%、被ダメージ+50%（デバフ防具）",
        "description": "狂戦士が纏う鎧。攻撃力を劇的に上げるが致命的に脆くなる。",
        "price": 100
    },

        # ====
        # 素材
        # ====
    
    "蜘蛛の糸": {
        "type": "material",
        "ability": "素材",
        "description": "蜘蛛から採れる糸。装備の素材になる。",
        "price": 15
    },
    "黄金の欠片": {
        "type": "material",
        "ability": "素材",
        "description": "世にも珍しい大きな金の欠片。これだけで巨額の富を得られることだろう。",
        "price": 1000
    }

}


ENEMY_ZONES = {
    "0-1000": {
        "enemies": [
            {
                "name": "スライム",
                "hp": 20,
                "atk": 3,
                "def": 2,
                "attribute": "none",
                "weight": 32,
                "exp": 8,
                "drops": [
                    {"item": "none", "weight": 60},
                    {"item": "革の盾", "weight": 15},
                    {"item": "木の盾", "weight": 5},
                    {"item": "石の盾", "weight": 2},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "coins", "amount": [10, 30], "weight": 10}
                ]
            },
            {
                "name": "ゴブリン",
                "hp": 16,
                "atk": 4,
                "def": 2,
                "attribute": "none",
                "weight": 28,
                "exp": 12,
                "drops": [
                    {"item": "none", "weight": 60},
                    {"item": "木の剣", "weight": 15},
                    {"item": "石の剣", "weight": 5},
                    {"item": "鉄の剣", "weight": 2},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "coins", "amount": [15, 30], "weight": 10}
                ]
            },
            {
                "name": "コウモリ",
                "hp": 12,
                "atk": 5,
                "def": 1,
                "attribute": "none",
                "weight": 24,
                "exp": 12,
                "drops": [
                    {"item": "none", "weight": 60},
                    {"item": "木の剣", "weight": 15},
                    {"item": "石の剣", "weight": 5},
                    {"item": "鉄の剣", "weight": 2},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "coins", "amount": [15, 30], "weight": 10}
                ]
            },
            {
                "name": "スパイダー",
                "hp": 25,
                "atk": 5,
                "def": 2,
                "attribute": "none",
                "weight": 15,
                "exp": 20,
                "drops": [
                    {"item": "none", "weight": 40},
                    {"item": "蜘蛛の糸", "weight": 25},
                    {"item": "毒針", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [30, 50], "weight": 20}
                ]
            },
            {
                "name": "ゴールデンスライム",
                "hp": 50,
                "atk": 5,
                "def": 10,
                "attribute": "none",
                "weight": 1,
                "exp": 12,
                "drops": [
                    {"item": "黄金の欠片", "weight": 10},
                    {"item": "黄金の鎧", "weight": 5},
                    {"item": "黄金の剣", "weight": 5},
                    {"item": "coins", "amount": [100, 150], "weight": 30},
                    {"item": "coins", "amount": [150, 200], "weight": 20},
                    {"item": "coins", "amount": [200, 250], "weight": 15},
                    {"item": "coins", "amount": [250, 300], "weight": 10},
                    {"item": "coins", "amount": [300, 500], "weight": 5}
                ]
            }
        ]
    },
    "1001-2000": {
        "enemies": [
            {
                "name": "ゾンビ",
                "hp": 40,
                "atk": 8,
                "def": 4,
                "attribute": "",
                "weight": 32,
                "exp": 20,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "スケルトン",
                "hp": 35,
                "atk": 9,
                "def": 4,
                "attribute": "",
                "weight": 28,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "ミイラ",
                "hp": 28,
                "atk": 8,
                "def": 5,
                "attribute": "",
                "weight": 24,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "ゴーレム",
                "hp": 50,
                "atk": 10,
                "def": 7,
                "attribute": "",
                "weight": 15,
                "exp": 30,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": 1,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "2001-3000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "3001-4000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "4001-5000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "5001-6000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "6001-7000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "7001-8000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "8001-9000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    },
    "9001-10000": {
        "enemies": [
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            },
            {
                "name": "",
                "hp": ,
                "atk": ,
                "def": ,
                "attribute": "",
                "weight": ,
                "exp": ,
                "drops": [
                    {"item": "none", "weight": 60},
                ]
            }
        ]
    }
}


def get_zone_from_distance(distance):
    if distance <= 1000:
        return "0-1000"
    elif distance <= 2000:
        return "1001-2000"
    elif distance <= 3000:
        return "2001-3000"
    elif distance <= 4000:
        return "3001-4000"
    elif distance <= 5000:
        return "4001-5000"
    elif distance <= 6000:
        return "5001-6000"
    elif distance <= 7000:
        return "6001-7000"
    elif distance <= 8000:
        return "7001-8000"
    elif distance <= 9000:
        return "8001-9000"
    elif distance <= 10000:
        return "9001-10000"
    else:
        return "9001-10000"


def get_random_enemy(distance):
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]

    weights = [enemy["weight"] for enemy in enemies]
    selected_enemy = random.choices(enemies, weights=weights, k=1)[0]

    return {
        "name": selected_enemy["name"],
        "hp": selected_enemy["hp"],
        "atk": selected_enemy["atk"],
        "def": selected_enemy["def"],
        "drops": selected_enemy["drops"],
        "attribute": selected_enemy.get("attribute", "none")
    }


def get_enemy_drop(enemy_name, distance):
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]

    enemy_data = None
    for enemy in enemies:
        if enemy["name"] == enemy_name:
            enemy_data = enemy
            break

    if not enemy_data or not enemy_data.get("drops"):
        return None

    drops = enemy_data["drops"]
    weights = [drop["weight"] for drop in drops]
    selected_drop = random.choices(drops, weights=weights, k=1)[0]

    if selected_drop["item"] == "coins":
        coin_amount = random.randint(selected_drop["amount"][0], selected_drop["amount"][1])
        return {"type": "coins", "amount": coin_amount}
    else:
        return {"type": "item", "name": selected_drop["item"]}


def get_treasure_box_equipment(distance):
    """宝箱から出る装備（武器・防具）のリストを返す"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]
    
    # そのゾーンの敵がドロップする装備を収集
    """レアドロップ品: 毒の短剣、魔法の杖、幽霊の布、竜の鱗、死の鎧、血の剣、暗黒の弓、巨人の鎧、カオスブレード、神の盾、深淵の剣"""
    equipment_list = []
    for enemy in enemies:
        drops = enemy.get("drops", [])
        for drop in drops:
            item_name = drop.get("item")
            if item_name and item_name != "none" and item_name != "coins" and item_name != "毒の短剣" and item_name != "魔法の杖" and item_name != "幽霊の布" and item_name != "竜の鱗" and item_name != "死の鎧" and item_name != "血の剣" and item_name != "暗黒の弓" and item_name != "巨人の鎧" and item_name != "カオスブレード" and item_name != "神の盾" and item_name != "深淵の剣":
                item_info = ITEMS_DATABASE.get(item_name)
                if item_info and item_info.get("type") in ["weapon", "armor"]:
                    if item_name not in equipment_list:
                        equipment_list.append(item_name)
    
    return equipment_list if equipment_list else ["木の剣"]


def get_treasure_box_weapons(distance):
    """宝箱から出る武器のみのリストを返す（階層に応じた武器のみ）"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]
    
    # そのゾーンの敵がドロップする武器のみを収集
    weapon_list = []
    for enemy in enemies:
        drops = enemy.get("drops", [])
        for drop in drops:
            item_name = drop.get("item")
            if item_name and item_name != "none" and item_name != "coins":
                item_info = ITEMS_DATABASE.get(item_name)
                if item_info and item_info.get("type") == "weapon":
                    if item_name not in weapon_list:
                        weapon_list.append(item_name)
    
    return weapon_list if weapon_list else ["木の剣"]


def get_item_info(item_name):
    return ITEMS_DATABASE.get(item_name, None)


def get_enemy_gold_drop(enemy_name, distance):
    """敵撃破時の確定ゴールドドロップ（ランダム範囲）を取得"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]
    
    # 敵データを検索
    for enemy in enemies:
        if enemy["name"] == enemy_name:
            # dropsリストからcoinsの範囲を取得
            drops = enemy.get("drops", [])
            for drop in drops:
                if drop.get("item") == "coins" and "amount" in drop:
                    min_gold = drop["amount"][0]
                    max_gold = drop["amount"][1]
                    return random.randint(min_gold, max_gold)
            # coinsが見つからない場合はデフォルト値
            return random.randint(5, 15)
    
    # 敵が見つからない場合はデフォルト値
    return random.randint(5, 15)


BOSS_DATA = {
    1: {
        "name": "ストーンスネーク",
        "hp": 80,
        "atk": 9,
        "def": 6,
        "attribute": "none",
                "attribute": "none",
        "drops": [
            {"item": "岩石の鱗", "weight": 30},
            {"item": "岩石の剣", "weight": 10},
            {"item": "HP回復薬（小）", "weight": 10},
            {"item": "HP回復薬（中）", "weight": 5},
            {"item": "MP回復薬（小）", "weight": 10},
            {"item": "MP回復薬（中）", "weight": 5},
            {"item": "coins", "amount": [40, 60], "weight": 30}
        ]
    },
    2: {
        "name": "デスロード",
        "hp": 150,
        "atk": 12,
        "def": 5,
        "attribute": "dark",
                "attribute": "dark",
        "drops": [
            {"item": "死神の鎌", "weight": 20},
            {"item": "不死の鎧", "weight": 20},
            {"item": "HP回復薬（中）", "weight": 15},
            {"item": "MP回復薬（中）", "weight": 15},
            {"item": "coins", "amount": [100, 200], "weight": 30}
        ]
    },
    3: {
        "name": "炎獄の魔竜", 
        "hp": 250,
        "atk": 15,
        "def": 6,
        "attribute": "fire",
                "attribute": "fire",
        "drops": [
            {"item": "竜の鱗", "weight": 15},
            {"item": "業火の剣", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 20},
            {"item": "MP回復薬（中）", "weight": 20},
            {"item": "coins", "amount": [150, 250], "weight": 30}
        ]
    },
    4: {
        "name": "影の王",
        "hp": 350,
        "atk": 20,
        "def": 8,
        "attribute": "dark",
                "attribute": "dark",
        "drops": [
            {"item": "影の短剣", "weight": 15},
            {"item": "死の鎧", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 20},
            {"item": "MP回復薬（中）", "weight": 20},
            {"item": "coins", "amount": [200, 300], "weight": 30}
        ]
    },
    5: {
        "name": "雷神",
        "hp": 450,
        "atk": 24,
        "def": 9,
        "attribute": "thunder",
                "attribute": "thunder",
        "drops": [
            {"item": "雷神の槍", "weight": 15},
            {"item": "祝福の盾", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 20},
            {"item": "MP回復薬（中）", "weight": 20},
            {"item": "coins", "amount": [250, 350], "weight": 30}
        ]
    },
    6: {
        "name": "氷の女王",
        "hp": 600,
        "atk": 28,
        "def": 10,
        "attribute": "ice",
                "attribute": "ice",
        "drops": [
            {"item": "氷結の杖", "weight": 15},
            {"item": "氷の鎧", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 15},
            {"item": "HP回復薬（大）", "weight": 5},
            {"item": "MP回復薬（中）", "weight": 15},
            {"item": "MP回復薬（大）", "weight": 5},
            {"item": "coins", "amount": [300, 400], "weight": 30}
        ]
    },
    7: {
        "name": "獄炎の巨人",
        "hp": 700,
        "atk": 32,
        "def": 11,
        "attribute": "fire",
                "attribute": "fire",
        "drops": [
            {"item": "巨人の鎧", "weight": 15},
            {"item": "獄炎の大剣", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 10},
            {"item": "HP回復薬（大）", "weight": 10},
            {"item": "MP回復薬（中）", "weight": 10},
            {"item": "MP回復薬（大）", "weight": 10},
            {"item": "coins", "amount": [350, 450], "weight": 30}
        ]
    },
    8: {
        "name": "深淵の守護者",
        "hp": 800,
        "atk": 35,
        "def": 12,
        "attribute": "dark",
                "attribute": "dark",
        "drops": [
            {"item": "深淵の剣", "weight": 15},
            {"item": "勇者の鎧", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 5},
            {"item": "HP回復薬（大）", "weight": 15},
            {"item": "MP回復薬（中）", "weight": 5},
            {"item": "MP回復薬（大）", "weight": 15},
            {"item": "coins", "amount": [400, 500], "weight": 30}
        ]
    },
    9: {
        "name": "混沌の龍帝",
        "hp": 1000,
        "atk": 40,
        "def": 14,
        "attribute": "fire",
                "attribute": "fire",
        "drops": [
            {"item": "竜帝の剣", "weight": 15},
            {"item": "竜帝の鎧", "weight": 15},
            {"item": "HP回復薬（大）", "weight": 20},
            {"item": "MP回復薬（大）", "weight": 20},
            {"item": "coins", "amount": [450, 550], "weight": 30}
        ]
    },
    10: {
        "name": "終焉の魔王",
        "hp": 1500,
        "atk": 45,
        "def": 16,
        "attribute": "none",
                "attribute": "none",
        "drops": [
            {"item": "魔王の剣", "weight": 20},
            {"item": "魔王の鎧", "weight": 20},
            {"item": "魔王の指輪", "weight": 30},
            {"item": "coins", "amount": [500, 600], "weight": 30}
        ]
    }
}

SECRET_WEAPONS = [
    {"id": 1, "name": "シークレットソード#1", "attack": 40, "ability": "全能力+50%", "rarity": "伝説"},
    {"id": 2, "name": "シークレットソード#2", "attack": 50, "ability": "即死攻撃10%", "rarity": "伝説"},
    {"id": 3, "name": "シークレットソード#3", "attack": 45, "ability": "HP自動回復+10/ターン", "rarity": "伝説"},
    {"id": 4, "name": "シークレットソード#4", "attack": 40, "ability": "攻撃力+100%", "rarity": "神話"},
    {"id": 5, "name": "シークレットソード#5", "attack": 60, "ability": "防御無視攻撃", "rarity": "伝説"},
    {"id": 6, "name": "シークレットソード#6", "attack": 55, "ability": "全ステータス+80%", "rarity": "神話"},
    {"id": 7, "name": "シークレットソード#7", "attack": 65, "ability": "敵防御力無視", "rarity": "伝説"},
    {"id": 8, "name": "シークレットソード#8", "attack": 45, "ability": "クリティカル率100%", "rarity": "神話"},
    {"id": 9, "name": "シークレットソード#9", "attack": 40, "ability": "HP吸収50%", "rarity": "伝説"},
    {"id": 10, "name": "シークレットソード#10", "attack": 70, "ability": "真・無敵", "rarity": "超越"},
]

SPECIAL_EVENT_SHOP = [
    {"name": "魔力の剣", "type": "weapon", "price": 500, "attack": 25, "ability": "魔力+20%"},
    {"name": "聖なる盾", "type": "armor", "price": 450, "attack": 0, "defense": 18, "ability": "HP自動回復+5"},
    {"name": "破壊の斧", "type": "weapon", "price": 600, "attack": 30, "ability": "防御貫通30%"},
    {"name": "呪いの首輪", "type": "armor", "price": 300, "attack": 0, "defense": -10, "ability": "攻撃力+50%"},
    {"name": "狂戦士の鎧", "type": "armor", "price": 700, "attack": 0, "defense": -20, "ability": "攻撃力+100%"},
]

"""現在の素材27種類"""
MATERIAL_PRICES = {
    "蜘蛛の糸": 30,
    "腐った肉": 20,
    "悪魔の角": 40,
    "竜の牙": 50,
    "魔界の結晶": 50,
    "竜王の牙": 60,
    "古竜の心臓": 100,
    "闇の宝珠": 80,
    "地獄犬の牙": 60,
    "吸血鬼の牙": 60,
    "魔導書の欠片": 80,
    "闇の宝石": 80,
    "巨獣の皮": 80,
    "影の欠片": 100,
    "混沌の欠片": 90,
    "不死鳥の羽": 90,
    "破壊の核": 120,
    "深淵の結晶": 100,
    "元素の核": 100,
    "神の鉱石": 120,
    "闇の聖典": 110,
    "海皇の鱗": 120,
    "三首の牙": 130,
    "幻王の魂": 140,
    "竜帝の心臓": 140,
    "神殺しの結晶": 150,
    "死皇の冠": 150,
    "魔王の指輪": 500
}

CRAFTING_RECIPES = {
    "蜘蛛の短剣": {
        "materials": {"蜘蛛の糸": 2},
        "result_type": "weapon",
        "attack": 7,
        "ability": "毒付与（10%の確率で追加ダメージ）",
        "description": "蜘蛛の糸から作られた短剣。強力な毒を持つ。"
    },
    "悪魔の剣": {
        "materials": {"悪魔の角": 2, "闇の宝珠": 1},
        "result_type": "weapon",
        "attack": 15,
        "ability": "闇属性（闇の敵に+60%ダメージ）",
        "description": "悪魔の角から鍛えられた剣。邪悪な力を宿す。"
    },
    "竜牙の剣": {
        "materials": {"竜の牙": 1, "悪魔の角": 2},
        "result_type": "weapon",
        "attack": 11,
        "ability": "竜の力（全ステータス+25%）",
        "description": "竜の牙から作られた伝説の剣。"
    },
    "闇の盾": {
        "materials": {"闇の宝珠": 1, "腐った肉": 3},
        "result_type": "armor",
        "defense": 15,
        "ability": "闇耐性+60%",
        "description": "闇の力が込められた盾。"
    },
    "蜘蛛の鎧": {
        "materials": {"蜘蛛の糸": 3, "悪魔の角": 1},
        "result_type": "armor",
        "defense": 11,
        "ability": "回避率+15%、毒耐性+50%",
        "description": "蜘蛛の糸で織られた鎧。軽くて頑丈。"
    },
    "竜鱗の鎧": {
        "materials": {"古龍の心臓": 1, "竜の牙": 2, "闇の宝珠": 1},
        "result_type": "armor",
        "defense": 13,
        "ability": "全属性耐性+30%、HP自動回復+5/ターン",
        "description": "竜の素材から作られた究極の鎧。"
    },
    "腐肉の兜": {
        "materials": {"腐った肉": 4},
        "result_type": "armor",
        "defense": 8,
        "ability": "毒無効、アンデッド特効+40%",
        "description": "腐った肉で作られた兜。アンデッドに強い。"
    }
}

def get_boss(stage):
    boss_template = BOSS_DATA.get(stage)
    if boss_template:
        # ディープコピーで新しいボスデータを返す
        return copy.deepcopy(boss_template)
    return None
    

def should_spawn_boss(distance):
    if distance < 980:
        return False
    remainder = distance % 1000
    # 980-1020の範囲（1000の±20）でボス発生
    return remainder <= 20 or remainder >= 980

def get_boss_stage(distance):
    """ボス戦の正しいステージ番号を取得（範囲ベース）"""
    return round(distance / 1000)

def is_special_event_distance(distance):
    if distance < 480:
        return False
    remainder = distance % 500
    # 480-520の範囲（500の±20）で特殊イベント発生
    in_event_range = remainder <= 20 or remainder >= 480
    # ただしボス範囲は除外
    in_boss_range = should_spawn_boss(distance)
    return in_event_range and not in_boss_range

def get_special_event_stage(distance):
    """特殊イベントの正しいステージ番号を取得（範囲ベース）"""
    return round(distance / 500)

def get_random_secret_weapon():
    if random.random() < 0.001:
        return random.choice(SECRET_WEAPONS)
    return None

def parse_ability_bonuses(ability_text):
    """ability文字列から数値ボーナスを解析"""
    import re
    bonuses = {
        'hp_bonus': 0,
        'attack_percent': 0,
        'defense_percent': 0,
        'damage_reduction': 0,
        'hp_regen': 0,
        'lifesteal_percent': 0
    }

    if not ability_text or ability_text == "なし" or ability_text == "素材":
        return bonuses

    hp_match = re.search(r'HP\+(\d+)', ability_text)
    if hp_match:
        bonuses['hp_bonus'] = int(hp_match.group(1))

    atk_match = re.search(r'攻撃力\+(\d+)%', ability_text)
    if atk_match:
        bonuses['attack_percent'] = int(atk_match.group(1))

    def_match = re.search(r'防御力\+(\d+)%', ability_text)
    if def_match:
        bonuses['defense_percent'] = int(def_match.group(1))

    dmg_red_match = re.search(r'(?:全ダメージ|被ダメージ)-(\d+)%', ability_text)
    if dmg_red_match:
        bonuses['damage_reduction'] = int(dmg_red_match.group(1))

    regen_match = re.search(r'HP(?:自動)?回復\+(\d+)', ability_text)
    if regen_match:
        bonuses['hp_regen'] = int(regen_match.group(1))

    lifesteal_match = re.search(r'HP吸収(?:.*?)?(\d+)%', ability_text)
    if lifesteal_match:
        bonuses['lifesteal_percent'] = int(lifesteal_match.group(1))

    return bonuses

async def calculate_equipment_bonus(user_id):
    """装備中のアイテムから攻撃力・防御力ボーナスと特殊効果を計算"""
    import db
    equipped = await db.get_equipped_items(user_id)

    attack_bonus = 0
    defense_bonus = 0
    total_bonuses = {
        'hp_bonus': 0,
        'attack_percent': 0,
        'defense_percent': 0,
        'damage_reduction': 0,
        'hp_regen': 0,
        'lifesteal_percent': 0
    }

    weapon_ability = ""
    armor_ability = ""

    if equipped.get('weapon'):
        weapon_info = get_item_info(equipped['weapon'])
        if weapon_info:
            attack_bonus = weapon_info.get('attack', 0)
            weapon_ability = weapon_info.get('ability', '')
            weapon_bonuses = parse_ability_bonuses(weapon_ability)
            for key in total_bonuses:
                total_bonuses[key] += weapon_bonuses[key]

    if equipped.get('armor'):
        armor_info = get_item_info(equipped['armor'])
        if armor_info:
            defense_bonus = armor_info.get('defense', 0)
            armor_ability = armor_info.get('ability', '')
            armor_bonuses = parse_ability_bonuses(armor_ability)
            for key in total_bonuses:
                total_bonuses[key] += armor_bonuses[key]

    return {
        'attack_bonus': attack_bonus,
        'defense_bonus': defense_bonus,
        'weapon_ability': weapon_ability,
        'armor_ability': armor_ability,
        **total_bonuses
    }


STORY_TRIGGERS = [
    {"distance": 100, "story_id": "voice_1", "exact_match": False},
    {"distance": 777, "story_id": "lucky_777", "exact_match": True},
    {"distance": 250, "story_id": "story_250", "exact_match": False},
    {"distance": 750, "story_id": "story_750", "exact_match": False},
    {"distance": 1250, "story_id": "story_1250", "exact_match": False},
    {"distance": 1750, "story_id": "story_1750", "exact_match": False},
    {"distance": 2250, "story_id": "story_2250", "exact_match": False},
    {"distance": 2750, "story_id": "story_2750", "exact_match": False},
    {"distance": 3250, "story_id": "story_3250", "exact_match": False},
    {"distance": 3750, "story_id": "story_3750", "exact_match": False},
    {"distance": 4250, "story_id": "story_4250", "exact_match": False},
    {"distance": 4750, "story_id": "story_4750", "exact_match": False},
    {"distance": 5250, "story_id": "story_5250", "exact_match": False},
    {"distance": 5750, "story_id": "story_5750", "exact_match": False},
    {"distance": 6250, "story_id": "story_6250", "exact_match": False},
    {"distance": 6750, "story_id": "story_6750", "exact_match": False},
    {"distance": 7250, "story_id": "story_7250", "exact_match": False},
    {"distance": 7750, "story_id": "story_7750", "exact_match": False},
    {"distance": 8250, "story_id": "story_8250", "exact_match": False},
    {"distance": 8750, "story_id": "story_8750", "exact_match": False},
    {"distance": 9250, "story_id": "story_9250", "exact_match": False},
    {"distance": 9750, "story_id": "story_9750", "exact_match": False},
]


def get_enemy_type(enemy_name):
    """敵の名前からタイプを判定"""
    enemy_name_lower = enemy_name.lower()

    # アンデッド系
    undead_keywords = ["ゴースト", "スケルトン", "ゾンビ", "リッチ", "デスナイト", "デスロード", "デスエンペラー", "不死", "死神"]
    for keyword in undead_keywords:
        if keyword in enemy_name:
            return "undead"

    # ドラゴン系
    dragon_keywords = ["ドラゴン", "竜", "龍", "ワイバーン"]
    for keyword in dragon_keywords:
        if keyword in enemy_name:
            return "dragon"

    # 闇属性
    dark_keywords = ["ダーク", "闇", "シャドウ", "影", "黒騎士"]
    for keyword in dark_keywords:
        if keyword in enemy_name:
            return "dark"

    return "normal"


def apply_ability_effects(damage, ability_text, attacker_hp, target_type="normal"):
    """
    ability効果を適用してダメージと追加効果を計算

    Args:
        damage: 基本ダメージ
        ability_text: ability説明文
        attacker_hp: 攻撃者のHP（HP吸収用）
        target_type: 対象タイプ（"normal", "undead", "dragon"など）

    Returns:
        dict: {
            "damage": 最終ダメージ,
            "lifesteal": HP吸収量,
            "burn": 燃焼ダメージ（追加効果）,
            "poison": 毒ダメージ（追加効果）,
            "instant_kill": 即死判定,
            "effect_text": 効果説明テキスト
        }
    """
    import re

    result = {
        "damage": damage,
        "lifesteal": 0,
        "burn": 0,
        "poison": 0,
        "instant_kill": False,
        "effect_text": ""
    }

    if not ability_text or ability_text == "なし" or ability_text == "素材":
        return result

    # 炎ダメージ（追加で炎ダメージ+X）
    fire_match = re.search(r'炎ダメージ\+(\d+)', ability_text)
    if fire_match:
        fire_damage = int(fire_match.group(1))
        result["damage"] += fire_damage
        result["effect_text"] += f"🔥炎+{fire_damage} "

    # 燃焼状態（攻撃時X%で敵を燃焼）
    burn_match = re.search(r'攻撃時(\d+)%で(?:敵を)?燃焼.*?ダメージ(\d+)', ability_text)
    if burn_match:
        burn_chance = int(burn_match.group(1))
        burn_damage = int(burn_match.group(2))
        if random.randint(1, 100) <= burn_chance:
            result["burn"] = burn_damage
            result["effect_text"] += f"🔥燃焼付与! "

    # 毒付与
    poison_match = re.search(r'毒付与.*?(\d+)%', ability_text)
    if poison_match:
        poison_chance = int(poison_match.group(1))
        if random.randint(1, 100) <= poison_chance:
            result["poison"] = 10
            result["effect_text"] += f"☠️毒付与! "

    # HP吸収
    lifesteal_match = re.search(r'HP吸収.*?(\d+)%', ability_text)
    if lifesteal_match:
        lifesteal_percent = int(lifesteal_match.group(1))
        result["lifesteal"] = int(damage * lifesteal_percent / 100)
        result["effect_text"] += f"💉HP吸収{result['lifesteal']} "

    # 即死効果
    instant_kill_match = re.search(r'攻撃時(\d+)%で即死', ability_text)
    if instant_kill_match:
        kill_chance = int(instant_kill_match.group(1))
        if random.randint(1, 100) <= kill_chance:
            result["instant_kill"] = True
            result["effect_text"] += f"💀即死発動! "

    # アンデッド特効
    if target_type == "undead" and "アンデッド特効" in ability_text:
        undead_match = re.search(r'アンデッド.*?\+(\d+)%', ability_text)
        if undead_match:
            bonus_percent = int(undead_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"⚰️特効+{bonus_damage} "

    # ドラゴン特効
    if target_type == "dragon" and "ドラゴン特効" in ability_text:
        dragon_match = re.search(r'ドラゴン.*?\+(\d+)%', ability_text)
        if dragon_match:
            bonus_percent = int(dragon_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"🐉特効+{bonus_damage} "

    # 闇属性特効
    if target_type == "dark" and "闇" in ability_text:
        dark_match = re.search(r'闇.*?\+(\d+)%', ability_text)
        if dark_match:
            bonus_percent = int(dark_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"🌑特効+{bonus_damage} "

    # クリティカル率アップ
    if "クリティカル率" in ability_text:
        crit_match = re.search(r'クリティカル率\+(\d+)%', ability_text)
        if crit_match:
            crit_chance = int(crit_match.group(1))
            if random.randint(1, 100) <= crit_chance:
                crit_damage = int(damage * 0.5)
                result["damage"] += crit_damage
                result["effect_text"] += f"💥クリティカル+{crit_damage} "

    # クリティカル時ダメージ3倍
    if "クリティカル時ダメージ3倍" in ability_text:
        if random.randint(1, 100) <= 20:
            triple_damage = int(damage * 2)
            result["damage"] += triple_damage
            result["effect_text"] += f"💥💥クリティカル3倍+{triple_damage} "

    # 凍結効果（攻撃時X%で敵を凍結）
    freeze_match = re.search(r'攻撃時(\d+)%で(?:敵を)?凍結', ability_text)
    if freeze_match:
        freeze_chance = int(freeze_match.group(1))
        if random.randint(1, 100) <= freeze_chance:
            result["freeze"] = True
            result["effect_text"] += "❄️凍結! "

    # 麻痺効果（攻撃時X%で敵を麻痺）
    paralyze_match = re.search(r'攻撃時(\d+)%で(?:敵を)?麻痺', ability_text)
    if paralyze_match:
        paralyze_chance = int(paralyze_match.group(1))
        if random.randint(1, 100) <= paralyze_chance:
            result["paralyze"] = True
            result["effect_text"] += "⚡麻痺! "

    # 分身攻撃（2回攻撃）
    if "分身攻撃" in ability_text and "2回攻撃" in ability_text:
        result["double_attack"] = True
        result["damage"] = int(damage * 2)
        result["effect_text"] += f"👥分身攻撃×2! "

    # 3回攻撃
    if "3回攻撃" in ability_text:
        result["triple_attack"] = True
        result["damage"] = int(damage * 3)
        result["effect_text"] += f"👥👥3連撃! "

    # 防御力無視
    if "防御無視" in ability_text or "防御力無視" in ability_text:
        if "攻撃時" in ability_text:
            ignore_match = re.search(r'攻撃時(\d+)%で敵の防御力無視', ability_text)
            if ignore_match:
                ignore_chance = int(ignore_match.group(1))
                if random.randint(1, 100) <= ignore_chance:
                    result["defense_ignore"] = True
                    result["effect_text"] += "🔓防御無視! "
        else:
            result["defense_ignore"] = True
            result["effect_text"] += "🔓防御無視! "

    # MP吸収
    mp_drain_match = re.search(r'(?:攻撃時)?敵のMP-(\d+)', ability_text)
    if mp_drain_match:
        mp_drain = int(mp_drain_match.group(1))
        result["mp_drain"] = mp_drain
        result["effect_text"] += f"🔵MP吸収{mp_drain} "

    # MP吸収（パーセント版）
    mp_absorb_match = re.search(r'MP吸収(\d+)%', ability_text)
    if mp_absorb_match:
        mp_percent = int(mp_absorb_match.group(1))
        result["mp_absorb_percent"] = mp_percent
        result["effect_text"] += f"🔵MP吸収{mp_percent}% "

    # アンデッド召喚
    if "アンデッド召喚" in ability_text:
        summon_match = re.search(r'攻撃時(\d+)%でアンデッド召喚.*?HP(\d+)回復', ability_text)
        if summon_match:
            summon_chance = int(summon_match.group(1))
            heal_amount = int(summon_match.group(2))
            if random.randint(1, 100) <= summon_chance:
                result["summon_heal"] = heal_amount
                result["effect_text"] += f"💀召喚HP+{heal_amount} "

    # 竜の咆哮（敵怯み）
    if "竜の咆哮" in ability_text:
        if random.randint(1, 100) <= 30:
            result["enemy_flinch"] = True
            result["effect_text"] += "🐉咆哮(怯み)! "

    # 呪い（攻撃時にHP-1、ダメージ+50%）
    if "呪い" in ability_text and "攻撃時にHP-" in ability_text:
        curse_match = re.search(r'HP-(\d+).*?ダメージ\+(\d+)%', ability_text)
        if curse_match:
            hp_loss = int(curse_match.group(1))
            dmg_bonus = int(curse_match.group(2))
            bonus_damage = int(damage * dmg_bonus / 100)
            result["damage"] += bonus_damage
            result["self_damage"] = hp_loss
            result["effect_text"] += f"😈呪い+{bonus_damage}(自傷-{hp_loss}) "

    # ランダム効果（燃焼・毒・防御無視・分身攻撃のいずれか）
    if "ランダム効果" in ability_text or "毎攻撃ランダム追加効果" in ability_text:
        random_effect = random.choice(["burn", "poison", "defense_ignore", "double_attack"])
        if random_effect == "burn":
            result["burn"] = 15
            result["effect_text"] += "🔥ランダム:燃焼! "
        elif random_effect == "poison":
            result["poison"] = 15
            result["effect_text"] += "☠️ランダム:毒! "
        elif random_effect == "defense_ignore":
            result["defense_ignore"] = True
            result["effect_text"] += "🔓防御無視! "
        elif random_effect == "double_attack":
            if random.randint(1, 100) <= 40:
                result["double_attack"] = True
                result["damage"] = int(damage * 2)
                result["effect_text"] += f"👥分身攻撃×2! "

    # ボス特効
    if "ボスに特効" in ability_text or "ボス特効" in ability_text:
        boss_match = re.search(r'ボス(?:に)?特効\+(\d+)%', ability_text)
        if boss_match and target_type == "boss":
            bonus_percent = int(boss_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"👑ボス特効+{bonus_damage} "

    # 全ステータス+X%
    if "全ステータス" in ability_text:
        stats_match = re.search(r'全ステータス\+(\d+)%', ability_text)
        if stats_match:
            stats_bonus = int(stats_match.group(1))
            bonus_damage = int(damage * stats_bonus / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"✨全ステ+{stats_bonus}% "

    # 攻撃力+X%（デバフ防具）
    if "攻撃力+" in ability_text and "%" in ability_text:
        atk_match = re.search(r'攻撃力\+(\d+)%', ability_text)
        if atk_match:
            atk_bonus = int(atk_match.group(1))
            bonus_damage = int(damage * atk_bonus / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"⚔️攻撃+{atk_bonus}% "

    # 初期化されていないフィールドを追加
    if "freeze" not in result:
        result["freeze"] = False
    if "double_attack" not in result:
        result["double_attack"] = False
    if "triple_attack" not in result:
        result["triple_attack"] = False
    if "defense_ignore" not in result:
        result["defense_ignore"] = False
    if "mp_drain" not in result:
        result["mp_drain"] = 0
    if "mp_absorb_percent" not in result:
        result["mp_absorb_percent"] = 0
    if "max_hp_damage" not in result:
        result["max_hp_damage"] = 0
    if "summon_heal" not in result:
        result["summon_heal"] = 0
    if "enemy_flinch" not in result:
        result["enemy_flinch"] = False
    if "self_damage" not in result:
        result["self_damage"] = 0
    if "paralyze" not in result:
        result["paralyze"] = False

    return result


def apply_armor_effects(incoming_damage, armor_ability, defender_hp, max_hp, attacker_damage=0, attack_attribute="none"):
    """
    防具のアビリティ効果を適用

    Args:
        incoming_damage: 受けるダメージ
        armor_ability: 防具のアビリティ文字列
        defender_hp: 防御者の現在HP
        max_hp: 防御者の最大HP
        attacker_damage: 攻撃者が与えたダメージ（反撃用）
        attack_attribute: 攻撃の属性 (none, fire, ice, thunder, dark, water, etc.)

    Returns:
        dict: {
            "damage": 最終ダメージ,
            "evaded": 回避したか,
            "counter_damage": 反撃ダメージ,
            "reflect_damage": 反射ダメージ,
            "hp_regen": HP回復量,
            "revived": 蘇生したか,
            "effect_text": 効果説明テキスト
        }
    """
    import re

    result = {
        "damage": incoming_damage,
        "evaded": False,
        "counter_damage": 0,
        "reflect_damage": 0,
        "hp_regen": 0,
        "revived": False,
        "effect_text": ""
    }

    if not armor_ability or armor_ability == "なし" or armor_ability == "素材":
        return result

    # 回避率
    evasion_match = re.search(r'回避率\+(\d+)%', armor_ability)
    if evasion_match:
        evasion_chance = int(evasion_match.group(1))
        if random.randint(1, 100) <= evasion_chance:
            result["evaded"] = True
            result["damage"] = 0
            result["effect_text"] += "💨回避! "
            return result

    # 幻影分身（被攻撃時X%で回避）
    phantom_match = re.search(r'被攻撃時(\d+)%で(?:完全)?回避', armor_ability)
    if phantom_match:
        phantom_chance = int(phantom_match.group(1))
        if random.randint(1, 100) <= phantom_chance:
            result["evaded"] = True
            result["damage"] = 0
            result["effect_text"] += "👻幻影回避! "
            return result

    # ダメージ軽減系
    if "全ダメージ" in armor_ability or "被ダメージ" in armor_ability:
        dmg_red_match = re.search(r'(?:全ダメージ|被ダメージ)-(\d+)%', armor_ability)
        if dmg_red_match:
            reduction = int(dmg_red_match.group(1))
            reduced_amount = int(incoming_damage * reduction / 100)
            result["damage"] -= reduced_amount
            result["effect_text"] += f"🛡️軽減-{reduced_amount} "

    # 物理ダメージ軽減
    if "物理ダメージ" in armor_ability:
        phys_match = re.search(r'物理ダメージ(?:軽減)?-(\d+)%', armor_ability)
        if phys_match:
            reduction = int(phys_match.group(1))
            reduced_amount = int(incoming_damage * reduction / 100)
            result["damage"] -= reduced_amount
            result["effect_text"] += f"🛡️物理軽減-{reduced_amount} "

    # 属性耐性（攻撃属性に応じて適用）
    if attack_attribute == "fire":
        if "炎耐性" in armor_ability or "炎無効" in armor_ability:
            if "無効" in armor_ability:
                result["damage"] = 0
                result["effect_text"] += "🔥炎無効! "
            else:
                fire_res_match = re.search(r'炎耐性\+(\d+)%', armor_ability)
                if fire_res_match:
                    resistance = int(fire_res_match.group(1))
                    reduced = int(incoming_damage * resistance / 100)
                    result["damage"] -= reduced
                    result["effect_text"] += f"🔥炎耐性-{reduced} "

    if attack_attribute == "dark":
        if "闇耐性" in armor_ability:
            dark_res_match = re.search(r'闇耐性\+(\d+)%', armor_ability)
            if dark_res_match:
                resistance = int(dark_res_match.group(1))
                reduced = int(incoming_damage * resistance / 100)
                result["damage"] -= reduced
                result["effect_text"] += f"🌑闇耐性-{reduced} "

    if attack_attribute in ["ice", "water"]:
        if "水・氷耐性" in armor_ability or "水耐性" in armor_ability or "氷耐性" in armor_ability:
            water_match = re.search(r'(?:水・氷耐性|水耐性|氷耐性)(\d+)%', armor_ability)
            if water_match:
                resistance = int(water_match.group(1))
                reduced = int(incoming_damage * resistance / 100)
                result["damage"] -= reduced
                result["effect_text"] += f"❄️水氷耐性-{reduced} "

    # 全属性耐性は常に適用（属性攻撃のみ）
    if attack_attribute != "none" and "全属性耐性" in armor_ability:
        all_res_match = re.search(r'全属性耐性\+(\d+)%', armor_ability)
        if all_res_match:
            resistance = int(all_res_match.group(1))
            reduced = int(incoming_damage * resistance / 100)
            result["damage"] -= reduced
            result["effect_text"] += f"✨全耐性-{reduced} "

    # ダメージ下限を0に
    result["damage"] = max(0, result["damage"])

    # 反撃（被ダメージのX%を返す）
    if "反撃" in armor_ability:
        counter_match = re.search(r'被ダメージの(\d+)%を返す', armor_ability)
        if counter_match:
            counter_percent = int(counter_match.group(1))
            result["counter_damage"] = int(incoming_damage * counter_percent / 100)
            result["effect_text"] += f"⚔️反撃{result['counter_damage']} "

    # 被攻撃時反撃ダメージ
    if "被攻撃時" in armor_ability and "反撃ダメージ" in armor_ability:
        reflect_match = re.search(r'反撃ダメージ(\d+)', armor_ability)
        if reflect_match:
            base_reflect = int(reflect_match.group(1))
            reflect_chance_match = re.search(r'被攻撃時(\d+)%', armor_ability)
            if reflect_chance_match:
                reflect_chance = int(reflect_chance_match.group(1))
                if random.randint(1, 100) <= reflect_chance:
                    result["reflect_damage"] = base_reflect
                    result["effect_text"] += f"⚡反撃{base_reflect} "

    # 反射ダメージ
    if "反射ダメージ" in armor_ability:
        reflect_dmg_match = re.search(r'反射ダメージ(\d+)', armor_ability)
        if reflect_dmg_match:
            result["reflect_damage"] = int(reflect_dmg_match.group(1))
            result["effect_text"] += f"⚡反射{result['reflect_damage']} "

    # HP自動回復
    hp_regen_match = re.search(r'HP(?:自動)?回復\+(\d+)', armor_ability)
    if hp_regen_match:
        result["hp_regen"] = int(hp_regen_match.group(1))
        result["effect_text"] += f"💚回復+{result['hp_regen']} "

    # 瀕死時HP回復
    if "瀕死時" in armor_ability and defender_hp <= max_hp * 0.3:
        critical_heal_match = re.search(r'瀕死時HP\+(\d+)', armor_ability)
        if critical_heal_match:
            critical_heal = int(critical_heal_match.group(1))
            result["hp_regen"] += critical_heal
            result["effect_text"] += f"💚瀕死回復+{critical_heal} "

    # HP30%以下で防御力1.5倍（神の加護）
    if "神の加護" in armor_ability and defender_hp <= max_hp * 0.3:
        if "防御力1.5倍" in armor_ability:
            halved = int(result["damage"] / 1.5)
            result["damage"] = halved
            result["effect_text"] += "✨神の加護(防御1.5倍)! "

    # 精霊加護（致死ダメージ時1回生存）
    if "精霊加護" in armor_ability and result["damage"] >= defender_hp:
        if "致死ダメージ時50%で生存" in armor_ability:
            if random.randint(1, 100) < 50:
                result["damage"] = defender_hp - 1
                result["revived"] = True
                result["effect_text"] += "🌟精霊加護(生存)! "

    # 竜鱗の守護（致死ダメージ無効1回）
    if "竜鱗の守護" in armor_ability and result["damage"] >= defender_hp:
        if "致死ダメージ50%で無効" in armor_ability:
            if random.randint(1, 100) < 50:
                result["damage"] = 0
                result["evaded"] = True
                result["effect_text"] += "🐉竜鱗の守護! "

    return result


async def check_story_trigger(previous_distance, current_distance, user_id):
    """
    ストーリートリガーをチェック

    Args:
        previous_distance: 移動前の距離
        current_distance: 移動後の距離
        user_id: ユーザーID

    Returns:
        トリガーされたストーリーID、またはNone
    """
    import db
    from story import STORY_DATA

    player = await db.get_player(user_id)
    if not player:
        return None

    loop_count = player.get("loop_count", 0)

    for trigger in STORY_TRIGGERS:
        trigger_distance = trigger["distance"]
        story_id = trigger["story_id"]
        exact_match = trigger.get("exact_match", False)

        triggered = False
        if exact_match:
            triggered = (current_distance == trigger_distance)
        else:
            triggered = (previous_distance < trigger_distance <= current_distance)

        if triggered:
            story = STORY_DATA.get(story_id)
            if not story:
                continue

            loop_requirement = story.get("loop_requirement")

            if loop_requirement is None:
                return story_id
            elif loop_requirement == 0 and loop_count == 0:
                if not await db.get_story_flag(user_id, story_id):
                    return story_id
            elif loop_requirement > 0 and loop_count >= loop_requirement:
                if not await db.get_story_flag(user_id, story_id):
                    return story_id

    return None

# スキルデータベース
SKILLS_DATABASE = {
    "体当たり": {
        "id": "体当たり",
        "name": "体当たり",
        "type": "attack",
        "mp_cost": 3,
        "power": 1.2,
        "description": "基本的な体当たり攻撃。威力1.2倍。",
        "unlock_distance": 0
    },
    "小火球": {
        "id": "小火球",
        "name": "小火球",
        "type": "attack",
        "mp_cost": 6,
        "power": 1.5,
        "description": "小さな火球を放つ。威力1.5倍。",
        "unlock_distance": 1000
    },
    "軽傷治癒": {
        "id": "軽傷治癒",
        "name": "軽傷治癒",
        "type": "heal",
        "mp_cost": 10,
        "heal_amount": 20,
        "description": "軽い傷を癒す。HP20回復。",
        "unlock_distance": 2000
    },
    "強攻撃": {
        "id": "強攻撃",
        "name": "強攻撃",
        "type": "attack",
        "mp_cost": 10,
        "power": 1.8,
        "description": "強力な一撃。威力1.8倍。",
        "unlock_distance": 3000
    },
    "ファイアボール": {
        "id": "ファイアボール",
        "name": "ファイアボール",
        "type": "attack",
        "mp_cost": 14,
        "power": 2.2,
        "description": "炎の球を放つ。威力2.2倍。",
        "unlock_distance": 4000
    },
    "猛攻撃": {
        "id": "猛攻撃",
        "name": "猛攻撃",
        "type": "attack",
        "mp_cost": 18,
        "power": 2.5,
        "description": "猛烈な攻撃。威力2.5倍。",
        "unlock_distance": 5000
    },
    "中治癒": {
        "id": "中治癒",
        "name": "中治癒",
        "type": "heal",
        "mp_cost": 20,
        "heal_amount": 50,
        "description": "傷を治す。HP50回復。",
        "unlock_distance": 6000
    },
    "爆炎": {
        "id": "爆炎",
        "name": "爆炎",
        "type": "attack",
        "mp_cost": 24,
        "power": 3.0,
        "description": "爆発する炎。威力3.0倍。",
        "unlock_distance": 7000
    },
    "完全治癒": {
        "id": "完全治癒",
        "name": "完全治癒",
        "type": "heal",
        "mp_cost": 30,
        "heal_amount": 100,
        "description": "完全に傷を癒す。HP100回復。",
        "unlock_distance": 8000
    },
    "神速の一閃": {
        "id": "神速の一閃",
        "name": "神速の一閃",
        "type": "attack",
        "mp_cost": 30,
        "power": 3.5,
        "description": "神速の斬撃。威力3.5倍。",
        "unlock_distance": 9000
    },
    "究極魔法": {
        "id": "究極魔法",
        "name": "究極魔法",
        "type": "attack",
        "mp_cost": 35,
        "power": 4.0,
        "description": "究極の魔法攻撃。威力4.0倍。",
        "unlock_distance": 10000
    }
}

def get_skill_info(skill_id):
    """スキル情報を取得"""
    return SKILLS_DATABASE.get(skill_id, None)

def get_exp_from_enemy(enemy_name, distance):
    """敵からのEXP獲得量を取得"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]

    for enemy in enemies:
        if enemy["name"] == enemy_name:
            return enemy.get("exp", 10)

    return 10

def categorize_drops_by_zone(zones, items_db):
    """
    ENEMY_ZONESのドロップアイテムを、アイテムタイプ別に分類し、階層ごとに集計する。
    """
    drops_by_zone_and_type = {}

    for zone_key, zone_data in zones.items():
        "ゾーンごとに結果を初期化"
        drops_by_zone_and_type[zone_key] = {
            "weapon": set(),
            "armor": set(),
            "potion": set(),
            "material": set(),
            "other": set() # noneやcoinsなど、タイプがないものを格納
        }

        "ENEMIESがリストであることを前提"
        for enemy in zone_data.get("enemies", []): 
            "dropsがリストであることを前提"
            for drop in enemy.get("drops", []):
                item_name = drop.get("item")

                "'none' または 'coins' のような特殊ドロップはスキップまたは'other'に追加"
                if item_name == "none" or item_name == "coins":
                    if item_name == "coins":
                        # 'none'は無視、'coins'は'other'に記録
                        drops_by_zone_and_type[zone_key]["other"].add(item_name)
                    continue

                "ITEMS_DATABASEからアイテムタイプを取得"
                item_info = items_db.get(item_name)

                if item_info:
                    item_type = item_info.get("type")
                    if item_type in drops_by_zone_and_type[zone_key]:
                        "該当するタイプセットにアイテム名を追加"
                        drops_by_zone_and_type[zone_key][item_type].add(item_name)
                    else:
                        "定義されていないタイプは 'other' に追加"
                        drops_by_zone_and_type[zone_key]["other"].add(item_name)
                else:
                    "ITEMS_DATABASEに見つからない場合は 'other' に追加"
                    drops_by_zone_and_type[zone_key]["other"].add(item_name)

        "setをリストに変換して、ソートする"
        for item_type in drops_by_zone_and_type[zone_key]:
            drops_by_zone_and_type[zone_key][item_type] = sorted(list(drops_by_zone_and_type[zone_key][item_type]))

    return drops_by_zone_and_type

"階層ごとにタイプ別ドロップアイテムを格納する新しい変数"
"ENEMY_ZONESとITEMS_DATABASEが定義された後に実行されます。"
DROPS_BY_ZONE_AND_TYPE = categorize_drops_by_zone(ENEMY_ZONES, ITEMS_DATABASE)

"0-1000mのエリアでドロップする武器のリストを取得"
weapon_drops_1 = DROPS_BY_ZONE_AND_TYPE["0-1000"]["weapon"]
"['木の剣', '石の剣', '毒の短剣', '鉄の剣']"

"0-1000mのエリアでドロップする防具のリストを取得"
armor_drops_1 = DROPS_BY_ZONE_AND_TYPE["0-1000"]["armor"]
"['木の盾', '石の盾', '鉄の盾']"

"1001-2000mのエリアでドロップする武器のリストを取得"
weapon_drops_2 = DROPS_BY_ZONE_AND_TYPE["1001-2000"]["weapon"]
"['骨の剣', '呪いの剣', '魔法の杖']"

"1001-2000mのエリアでドロップする防具のリストを取得"
armor_drops_2 = DROPS_BY_ZONE_AND_TYPE["1001-2000"]["armor"]
"['骨の盾', '死者の兜', '不死の鎧','幽霊の布']"

"2001-3000mのエリアでドロップする武器のリストを取得"
weapon_drops_3 = DROPS_BY_ZONE_AND_TYPE["2001-3000"]["weapon"]
"['炎の大剣', 'ドラゴンソード', '黒騎士の剣']"

"2001-3000mのエリアでドロップする防具のリストを取得"
armor_drops_3 = DROPS_BY_ZONE_AND_TYPE["2001-3000"]["armor"]
"['地獄の鎧', '龍の鱗', '黒騎士の盾','黒騎士の鎧']"

"3001-4000mのエリアでドロップする武器のリストを取得"
weapon_drops_4 = DROPS_BY_ZONE_AND_TYPE["3001-4000"]["weapon"]
"['炎獄の剣', '死神の鎌']"

"3001-4000mのエリアでドロップする防具のリストを取得"
armor_drops_4 = DROPS_BY_ZONE_AND_TYPE["3001-4000"]["armor"]
"['魔王の盾', '龍鱗の鎧', '冥界の盾','死の鎧']"

"4001-5000mのエリアでドロップする武器のリストを取得"
weapon_drops_5 = DROPS_BY_ZONE_AND_TYPE["4001-5000"]["weapon"]
"['業火の剣', '血の剣', '死霊の杖']"

"4001-5000mのエリアでドロップする防具のリストを取得"
armor_drops_5 = DROPS_BY_ZONE_AND_TYPE["4001-5000"]["armor"]
"['炎の鎧', '夜の外套', '不死王の兜']"

"5001-6000mのエリアでドロップする武器のリストを取得"
weapon_drops_6 = DROPS_BY_ZONE_AND_TYPE["5001-6000"]["weapon"]
"['影の短剣', '暗黒の弓', '破壊の斧', '虚無の剣']"

"5001-6000mのエリアでドロップする防具のリストを取得"
armor_drops_6 = DROPS_BY_ZONE_AND_TYPE["5001-6000"]["armor"]
"['巨人の鎧', '幻影の鎧']"

"6001-7000mのエリアでドロップする武器のリストを取得"
weapon_drops_7 = DROPS_BY_ZONE_AND_TYPE["6001-7000"]["weapon"]
"['カオスブレード', '炎の剣', '滅びの剣']"

"6001-7000mのエリアでドロップする防具のリストを取得"
armor_drops_7 = DROPS_BY_ZONE_AND_TYPE["6001-7000"]["armor"]
"['混沌の鎧', '再生の鎧', '終焉の盾']"

"7001-8000mのエリアでドロップする武器のリストを取得"
weapon_drops_8 = DROPS_BY_ZONE_AND_TYPE["7001-8000"]["weapon"]
"['深淵の剣', '四元の剣', '天の槌']"

"7001-8000mのエリアでドロップする防具のリストを取得"
armor_drops_8 = DROPS_BY_ZONE_AND_TYPE["7001-8000"]["armor"]
"['虚空の鎧', '精霊の盾', '神の盾']"

"8001-9000mのエリアでドロップする武器のリストを取得"
weapon_drops_9 = DROPS_BY_ZONE_AND_TYPE["8001-9000"]["weapon"]
"['暗黒聖剣', '水神の槍', '獄炎の剣']"

"8001-9000mのエリアでドロップする防具のリストを取得"
armor_drops_9 = DROPS_BY_ZONE_AND_TYPE["8001-9000"]["armor"]
"['堕天の鎧', '深海の鎧', '地獄門の鎧']"

"9001-10000mのエリアでドロップする武器のリストを取得"
weapon_drops_10 = DROPS_BY_ZONE_AND_TYPE["9001-10000"]["weapon"]
"['幻影剣', '竜帝剣', '混沌神剣', '死神大鎌']"

"9001-10000mのエリアでドロップする防具のリストを取得"
armor_drops_10 = DROPS_BY_ZONE_AND_TYPE["9001-10000"]["armor"]
"['幻王の鎧', '竜帝の鎧', '創世の盾', '死帝の鎧']"
