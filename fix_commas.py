#!/usr/bin/env python3
"""
game.pyのITEMS_DATABASEのカンマを修正するスクリプト
"""
import re

with open('game.py', 'r', encoding='utf-8') as f:
    content = f.read()

# descriptionの後にカンマがなく、その次の行が"price":の場合にカンマを追加
fixed_content = re.sub(
    r'("description": "[^"]*")\n(\s+)("price":)',
    r'\1,\n\2\3',
    content
)

with open('game.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✓ カンマの修正が完了しました")
