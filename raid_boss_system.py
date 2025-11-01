"""
レイドボスシステム - 500m毎のレイドボス、HP継続戦闘、貢献度システム
"""
import discord
from discord.ui import View, button
import db
import random
import datetime

# レイドボスデータ
RAID_BOSSES = {
    500: {
        "name": "ゴーレム番人",
        "hp": 800,
        "atk": 15,
        "def": 10,
        "drops": ["巨獣の皮", "竜の牙", "HP回復薬（大）", "MP回復薬（大）"],
        "gold_range": [200, 400]
    },
    1000: {
        "name": "闇の守護者",
        "hp": 1500,
        "atk": 20,
        "def": 12,
        "drops": ["闇の宝珠", "暗黒聖剣", "魔法の杖", "HP回復薬（大）"],
        "gold_range": [300, 600]
    },
    1500: {
        "name": "炎獄の番獣",
        "hp": 2200,
        "atk": 25,
        "def": 15,
        "drops": ["地獄犬の牙", "炎獄の剣", "地獄の鎧", "エリクサー"],
        "gold_range": [400, 800]
    },
    2000: {
        "name": "氷結の古竜",
        "hp": 3000,
        "atk": 30,
        "def": 18,
        "drops": ["古竜の心臓", "氷結の杖", "竜の鱗", "エリクサー"],
        "gold_range": [500, 1000]
    },
    2500: {
        "name": "死霊王",
        "hp": 3800,
        "atk": 35,
        "def": 20,
        "drops": ["死霊の杖", "不死王の冠", "闇の聖典", "エリクサー"],
        "gold_range": [600, 1200]
    },
    3000: {
        "name": "深淵の魔神",
        "hp": 4500,
        "atk": 40,
        "def": 22,
        "drops": ["深淵の結晶", "深淵の剣", "虚空の鎧", "エリクサー"],
        "gold_range": [700, 1400]
    },
    3500: {
        "name": "雷神の化身",
        "hp": 5200,
        "atk": 45,
        "def": 25,
        "drops": ["雷神の槍", "神の鉱石", "勇者の鎧", "エリクサー"],
        "gold_range": [800, 1600]
    },
    4000: {
        "name": "混沌の支配者",
        "hp": 6000,
        "atk": 50,
        "def": 28,
        "drops": ["混沌の欠片", "カオスブレード", "混沌の鎧", "エリクサー"],
        "gold_range": [900, 1800]
    },
    4500: {
        "name": "破壊神",
        "hp": 6800,
        "atk": 55,
        "def": 30,
        "drops": ["破壊の核", "破壊の斧", "終焉の盾", "エリクサー"],
        "gold_range": [1000, 2000]
    },
    5000: {
        "name": "竜帝ドラゴノス",
        "hp": 8000,
        "atk": 60,
        "def": 35,
        "drops": ["竜帝の心臓", "竜帝の剣", "竜帝の鎧", "エリクサー"],
        "gold_range": [1200, 2400]
    },
    5500: {
        "name": "幻王イリュージア",
        "hp": 9000,
        "atk": 65,
        "def": 38,
        "drops": ["幻王の魂", "幻影の剣", "幻王の鎧", "エリクサー"],
        "gold_range": [1400, 2800]
    },
    6000: {
        "name": "死帝ネクロード",
        "hp": 10000,
        "atk": 70,
        "def": 40,
        "drops": ["死皇の冠", "死神の剣", "死帝の鎧", "エリクサー"],
        "gold_range": [1600, 3200]
    },
    6500: {
        "name": "海皇ポセイドラ",
        "hp": 11000,
        "atk": 75,
        "def": 42,
        "drops": ["海皇の鱗", "水神の槍", "深海の鎧", "エリクサー"],
        "gold_range": [1800, 3600]
    },
    7000: {
        "name": "三首の魔獣",
        "hp": 12000,
        "atk": 80,
        "def": 45,
        "drops": ["三首の牙", "魔王の双剣", "地獄門の鎧", "エリクサー"],
        "gold_range": [2000, 4000]
    },
    7500: {
        "name": "創世神の使徒",
        "hp": 13000,
        "atk": 85,
        "def": 48,
        "drops": ["神の鉱石", "天の槌", "創世の盾", "エリクサー"],
        "gold_range": [2200, 4400]
    },
    8000: {
        "name": "神殺しの魔剣",
        "hp": 14000,
        "atk": 90,
        "def": 50,
        "drops": ["神殺しの結晶", "滅びの剣", "虚無の剣", "エリクサー"],
        "gold_range": [2400, 4800]
    },
    8500: {
        "name": "堕天使ルシフェル",
        "hp": 15000,
        "atk": 95,
        "def": 52,
        "drops": ["闇の聖典", "暗黒聖剣", "堕天の鎧", "エリクサー"],
        "gold_range": [2600, 5200]
    },
    9000: {
        "name": "四元の守護者",
        "hp": 16000,
        "atk": 100,
        "def": 55,
        "drops": ["元素の核", "四元の剣", "精霊の盾", "エリクサー"],
        "gold_range": [2800, 5600]
    },
    9500: {
        "name": "終焉の化身",
        "hp": 18000,
        "atk": 110,
        "def": 60,
        "drops": ["神殺しの結晶", "獄炎の大剣", "終焉の盾", "エリクサー"],
        "gold_range": [3000, 6000]
    }
}

def get_raid_boss_data(distance):
    """距離に基づいてレイドボスデータを取得"""
    # 500m毎のレイドボス
    raid_distance = (distance // 500) * 500
    if raid_distance == 0 or raid_distance > 9500:
        return None
    return RAID_BOSSES.get(raid_distance)

def get_raid_boss_id(distance):
    """レイドボスIDを生成"""
    raid_distance = (distance // 500) * 500
    return f"raid_{raid_distance}"

def calculate_raid_rewards(total_damage, boss_max_hp):
    """
    貢献度に基づいて報酬の確率を計算
    
    Args:
        total_damage: プレイヤーが与えた総ダメージ
        boss_max_hp: ボスの最大HP
    
    Returns:
        float: ドロップ倍率 (0.5 ~ 2.0)
    """
    contribution_rate = min(total_damage / boss_max_hp, 1.0)
    
    # 貢献度に応じた倍率
    if contribution_rate >= 0.5:  # 50%以上貢献
        return 2.0
    elif contribution_rate >= 0.3:  # 30%以上貢献
        return 1.5
    elif contribution_rate >= 0.1:  # 10%以上貢献
        return 1.2
    elif contribution_rate >= 0.05:  # 5%以上貢献
        return 1.0
    else:
        return 0.5

async def check_raid_boss_respawn(boss_id):
    """
    レイドボスの復活チェック（討伐後24時間）
    
    Returns:
        bool: True if respawned, False if still defeated
    """
    # この関数はdb.pyで実装する必要がある
    pass
