#!/usr/bin/env python3
"""
game.pyのITEMS_DATABASEに価格("price"キー)を自動追加するスクリプト
"""
import re

def calculate_price(item_name, item_data):
    """アイテムの価格を計算"""
    item_type = item_data.get('type', '')
    
    # Potions
    if item_type == 'potion':
        effect = item_data.get('effect', '')
        if 'HPMPMAX' in effect or 'エリクサー' in item_name:
            return 500
        elif '大' in item_name:
            return 200
        elif '中' in item_name:
            return 80
        elif '小' in item_name:
            return 30
        return 50
    
    # Weapons
    elif item_type == 'weapon':
        attack = item_data.get('attack', 0)
        defense = item_data.get('defense', 0)  # 一部武器はdefense持ち
        stat = max(attack, defense)
        
        base_price = stat * 15
        if stat <= 5:
            return max(10, base_price + 20)
        elif stat <= 10:
            return base_price + 50
        elif stat <= 15:
            return base_price + 80
        elif stat <= 20:
            return base_price + 120
        elif stat <= 25:
            return base_price + 150
        elif stat <= 30:
            return base_price + 200
        else:
            return base_price + 300
    
    # Armor
    elif item_type == 'armor':
        defense = item_data.get('defense', 0)
        # デバフ防具は価格が低い
        if defense < 0:
            return max(10, abs(defense) * 5)
        
        base_price = defense * 12
        if defense <= 5:
            return max(10, base_price + 20)
        elif defense <= 10:
            return base_price + 40
        elif defense <= 15:
            return base_price + 70
        elif defense <= 20:
            return base_price + 100
        elif defense <= 25:
            return base_price + 130
        elif defense <= 30:
            return base_price + 180
        else:
            return base_price + 250
    
    # Materials
    elif item_type == 'material':
        material_prices = {
            '蜘蛛の糸': 15, '腐った肉': 10, '悪魔の角': 50, '竜の牙': 100,
            '闇の宝珠': 80, '魔界の結晶': 150, '古竜の心臓': 300, '竜王の牙': 200,
            '地獄犬の牙': 120, '吸血鬼の牙': 100, '魔導書の欠片': 90, '闇の宝石': 180,
            '巨獣の皮': 70, '影の欠片': 110, '混沌の欠片': 250, '不死鳥の羽': 220,
            '破壊の核': 280, '深淵の結晶': 200, '元素の核': 300, '神の鉱石': 350,
            '闇の聖典': 320, '海皇の鱗': 280, '三首の牙': 240, '幻王の魂': 400,
            '竜帝の心臓': 500, '神殺しの結晶': 600,
        }
        return material_prices.get(item_name, 50)
    
    return 10

# game.pyを読み込み
with open('game.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 新しいコンテンツを作成
new_lines = []
in_item_dict = False
item_indent = ""
brace_count = 0
dict_depth = 0

for i, line in enumerate(lines):
    # ITEMS_DATABASE の開始を検出
    if 'ITEMS_DATABASE = {' in line:
        new_lines.append(line)
        dict_depth = 1
        continue
    
    # 辞書の深さを追跡
    if dict_depth > 0:
        brace_count += line.count('{') - line.count('}')
        dict_depth = max(1, 1 + brace_count)
        
        # アイテム名の行（"アイテム名": { の形式）
        if '": {' in line and dict_depth == 2:
            in_item_dict = True
            item_indent = re.match(r'^(\s*)', line).group(1)
            new_lines.append(line)
            continue
        
        # アイテム辞書の終了（},）
        if in_item_dict and '},' in line:
            # priceキーがまだない場合は追加
            # 直前の行をチェック
            if new_lines and '"price"' not in ''.join(new_lines[-5:]):
                # アイテム名を取得
                for prev_line in reversed(new_lines[-20:]):
                    if '": {' in prev_line:
                        item_name_match = re.search(r'"([^"]+)":\s*{', prev_line)
                        if item_name_match:
                            item_name = item_name_match.group(1)
                            # アイテムデータを簡易解析
                            item_data = {}
                            for check_line in new_lines[-20:]:
                                if '"type":' in check_line:
                                    type_match = re.search(r'"type":\s*"([^"]+)"', check_line)
                                    if type_match:
                                        item_data['type'] = type_match.group(1)
                                if '"attack":' in check_line:
                                    attack_match = re.search(r'"attack":\s*(\d+)', check_line)
                                    if attack_match:
                                        item_data['attack'] = int(attack_match.group(1))
                                if '"defense":' in check_line:
                                    defense_match = re.search(r'"defense":\s*(-?\d+)', check_line)
                                    if defense_match:
                                        item_data['defense'] = int(defense_match.group(1))
                                if '"effect":' in check_line:
                                    effect_match = re.search(r'"effect":\s*"([^"]+)"', check_line)
                                    if effect_match:
                                        item_data['effect'] = effect_match.group(1)
                            
                            # 価格を計算
                            price = calculate_price(item_name, item_data)
                            # priceキーを追加（descriptionの後）
                            new_lines.append(f'{item_indent}    "price": {price}\n')
                            break
            
            new_lines.append(line)
            in_item_dict = False
            continue
        
        # ITEMS_DATABASEの終了
        if dict_depth == 1 and line.strip() == '}':
            new_lines.append(line)
            dict_depth = 0
            continue
    
    new_lines.append(line)

# ファイルに書き込み
with open('game.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✓ 価格の追加が完了しました")
