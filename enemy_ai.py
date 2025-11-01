"""
敵AI行動システム - 敵の行動パターンとスキル
"""
import random

# 敵のスキルデータベース
ENEMY_SKILLS = {
    "体当たり": {
        "type": "attack",
        "damage_multiplier": 1.2,
        "mp_cost": 0,
        "description": "通常攻撃の1.2倍のダメージ"
    },
    "強撃": {
        "type": "attack",
        "damage_multiplier": 1.5,
        "mp_cost": 0,
        "description": "強力な一撃"
    },
    "連続攻撃": {
        "type": "attack",
        "hit_count": 2,
        "damage_multiplier": 0.7,
        "mp_cost": 0,
        "description": "2回連続で攻撃"
    },
    "毒針": {
        "type": "status",
        "damage_multiplier": 0.8,
        "status": "poison",
        "status_duration": 3,
        "status_damage": 5,
        "mp_cost": 0,
        "description": "毒を与える攻撃"
    },
    "暗黒の刃": {
        "type": "attack",
        "damage_multiplier": 1.8,
        "mp_cost": 0,
        "description": "強力な闇属性攻撃"
    },
    "炎の息": {
        "type": "attack",
        "damage_multiplier": 1.6,
        "attribute": "fire",
        "mp_cost": 0,
        "description": "炎属性の範囲攻撃"
    },
    "即死の鎌": {
        "type": "instant_death",
        "success_rate": 0.15,
        "damage_multiplier": 2.0,
        "mp_cost": 0,
        "description": "低確率で即死（失敗時は大ダメージ）"
    },
    "吸血": {
        "type": "drain",
        "damage_multiplier": 1.3,
        "hp_drain_rate": 0.5,
        "mp_cost": 0,
        "description": "与えたダメージの50%を吸収"
    },
    "魔力暴走": {
        "type": "attack",
        "damage_multiplier": 2.5,
        "self_damage_rate": 0.2,
        "mp_cost": 0,
        "description": "強力だが自身もダメージを受ける"
    }
}

# 敵の行動パターン
def get_enemy_action(enemy_name, enemy_hp, enemy_max_hp, turn_count):
    """
    敵の行動を決定する
    
    Args:
        enemy_name: 敵の名前
        enemy_hp: 敵の現在HP
        enemy_max_hp: 敵の最大HP
        turn_count: 現在のターン数
    
    Returns:
        dict: {"action": "attack"/"skill"/"defend"/"flee"/"nothing", "skill_name": スキル名(skillの場合)}
    """
    hp_rate = enemy_hp / enemy_max_hp if enemy_max_hp > 0 else 0
    
    # 敵ごとの行動パターン
    enemy_behaviors = {
        # 初期エリア (0-1000m)
        "スライム": {
            "skills": ["体当たり"],
            "skill_rate": 0.3,
            "defend_rate": 0.1,
            "flee_rate": 0.05 if hp_rate < 0.3 else 0,
        },
        "ゴブリン": {
            "skills": ["強撃", "連続攻撃"],
            "skill_rate": 0.4,
            "defend_rate": 0.15,
            "flee_rate": 0.1 if hp_rate < 0.2 else 0,
        },
        "蜘蛛": {
            "skills": ["毒針", "連続攻撃"],
            "skill_rate": 0.5,
            "defend_rate": 0.1,
            "flee_rate": 0,
        },
        
        # 1001-2000m
        "スケルトン": {
            "skills": ["暗黒の刃", "強撃"],
            "skill_rate": 0.5,
            "defend_rate": 0.2,
            "flee_rate": 0,
        },
        "ゾンビ": {
            "skills": ["体当たり", "吸血"],
            "skill_rate": 0.4,
            "defend_rate": 0.1,
            "flee_rate": 0,
        },
        "ゴースト": {
            "skills": ["暗黒の刃", "吸血"],
            "skill_rate": 0.6,
            "defend_rate": 0.05,
            "flee_rate": 0.15 if hp_rate < 0.4 else 0,
        },
        
        # 2001-3000m
        "デーモン": {
            "skills": ["炎の息", "強撃", "連続攻撃"],
            "skill_rate": 0.6,
            "defend_rate": 0.2,
            "flee_rate": 0,
        },
        "ダークナイト": {
            "skills": ["暗黒の刃", "強撃"],
            "skill_rate": 0.5,
            "defend_rate": 0.3,
            "flee_rate": 0,
        },
        "ドラゴン": {
            "skills": ["炎の息", "連続攻撃", "強撃"],
            "skill_rate": 0.7,
            "defend_rate": 0.1,
            "flee_rate": 0,
        },
        
        # その他の敵もデフォルト行動
        "default": {
            "skills": ["体当たり", "強撃"],
            "skill_rate": 0.4,
            "defend_rate": 0.15,
            "flee_rate": 0.05 if hp_rate < 0.3 else 0,
        }
    }
    
    # 敵の行動設定を取得（なければデフォルト）
    behavior = enemy_behaviors.get(enemy_name, enemy_behaviors["default"])
    
    # 行動を確率で決定
    rand = random.random()
    
    # 逃走判定
    if rand < behavior["flee_rate"]:
        return {"action": "flee"}
    
    # 防御判定
    if rand < behavior["flee_rate"] + behavior["defend_rate"]:
        return {"action": "defend"}
    
    # スキル使用判定
    if rand < behavior["flee_rate"] + behavior["defend_rate"] + behavior["skill_rate"]:
        # ランダムでスキルを選択
        skill_name = random.choice(behavior["skills"])
        return {"action": "skill", "skill_name": skill_name}
    
    # 通常攻撃
    return {"action": "attack"}


def calculate_enemy_skill_damage(skill_name, enemy_atk, player_def):
    """
    敵のスキルダメージを計算
    
    Args:
        skill_name: スキル名
        enemy_atk: 敵の攻撃力
        player_def: プレイヤーの防御力
    
    Returns:
        dict: {
            "damage": ダメージ量,
            "type": スキルタイプ,
            "extra_effects": 追加効果の辞書
        }
    """
    skill = ENEMY_SKILLS.get(skill_name)
    if not skill:
        return {"damage": max(1, enemy_atk - player_def), "type": "attack", "extra_effects": {}}
    
    damage_multiplier = skill.get("damage_multiplier", 1.0)
    base_damage = max(1, int((enemy_atk * damage_multiplier) - player_def))
    
    result = {
        "damage": base_damage,
        "type": skill.get("type", "attack"),
        "extra_effects": {},
        "description": skill.get("description", "")
    }
    
    # 連続攻撃
    if "hit_count" in skill:
        result["extra_effects"]["hit_count"] = skill["hit_count"]
        result["damage"] = int(base_damage * skill["hit_count"])
    
    # 状態異常
    if skill.get("type") == "status":
        result["extra_effects"]["status"] = skill.get("status")
        result["extra_effects"]["status_duration"] = skill.get("status_duration", 0)
        result["extra_effects"]["status_damage"] = skill.get("status_damage", 0)
    
    # HP吸収
    if skill.get("type") == "drain":
        result["extra_effects"]["hp_drain_rate"] = skill.get("hp_drain_rate", 0)
    
    # 即死スキル
    if skill.get("type") == "instant_death":
        result["extra_effects"]["instant_death_rate"] = skill.get("success_rate", 0)
    
    # 自傷ダメージ
    if "self_damage_rate" in skill:
        result["extra_effects"]["self_damage_rate"] = skill.get("self_damage_rate", 0)
    
    return result
