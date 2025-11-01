"""
商人遭遇イベントシステム - 0.5%確率で出現、購入・売却、ステータス確認機能
"""
import discord
from discord.ui import View, button, Select
import random
import game

class MerchantView(View):
    def __init__(self, user_id, player_data):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.player_data = player_data
        
    @button(label="💰 アイテムを購入", style=discord.ButtonStyle.green)
    async def buy_items(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの商人ではありません！", ephemeral=True)
            return
        
        # 購入View表示
        await interaction.response.send_message(
            embed=self.get_merchant_shop_embed(),
            view=MerchantBuyView(self.user_id, self.player_data),
            ephemeral=True
        )
    
    @button(label="💸 アイテムを売却", style=discord.ButtonStyle.primary)
    async def sell_items(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの商人ではありません！", ephemeral=True)
            return
        
        # 売却View表示
        await interaction.response.send_message(
            "インベントリから売却するアイテムを選択してください",
            view=MerchantSellView(self.user_id, self.player_data),
            ephemeral=True
        )
    
    @button(label="📊 ステータス確認", style=discord.ButtonStyle.secondary)
    async def check_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの商人ではありません！", ephemeral=True)
            return
        
        # ステータス表示
        await interaction.response.send_message(
            embed=self.get_player_stats_embed(),
            ephemeral=True
        )
    
    @button(label="👋 立ち去る", style=discord.ButtonStyle.danger)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの商人ではありません！", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="商人との別れ",
            description="商人:「またのご利用を…」\n\nあなたは商人と別れ、冒険を続けた。",
            color=discord.Color.grey()
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    def get_merchant_shop_embed(self):
        """商人の店Embedを生成"""
        embed = discord.Embed(
            title="🏪 旅の商人の店",
            description="商人:「いらっしゃい。良いものを揃えているよ」",
            color=discord.Color.gold()
        )
        return embed
    
    def get_player_stats_embed(self):
        """プレイヤーのステータスEmbedを生成"""
        player = self.player_data
        equipped_weapon = player.get("equipped_weapon", "なし")
        equipped_armor = player.get("equipped_armor", "なし")
        
        weapon_info = game.get_item_info(equipped_weapon) if equipped_weapon != "なし" else {}
        armor_info = game.get_item_info(equipped_armor) if equipped_armor != "なし" else {}
        
        weapon_atk = weapon_info.get("attack", 0)
        armor_def = armor_info.get("defense", 0)
        
        total_atk = player.get("atk", 0) + weapon_atk
        total_def = player.get("def", 0) + armor_def
        
        embed = discord.Embed(
            title="📊 あなたのステータス",
            color=discord.Color.blue()
        )
        embed.add_field(name="💚 HP", value=f"{player.get('hp', 0)}/{player.get('max_hp', 0)}", inline=True)
        embed.add_field(name="💙 MP", value=f"{player.get('mp', 0)}/{player.get('max_mp', 0)}", inline=True)
        embed.add_field(name="💰 ゴールド", value=f"{player.get('gold', 0)}G", inline=True)
        embed.add_field(name="⚔️ 攻撃力", value=f"{total_atk} ({player.get('atk', 0)}+{weapon_atk})", inline=True)
        embed.add_field(name="🛡️ 防御力", value=f"{total_def} ({player.get('def', 0)}+{armor_def})", inline=True)
        embed.add_field(name="📍 距離", value=f"{player.get('distance', 0)}m", inline=True)
        embed.add_field(name="⚔️ 装備武器", value=equipped_weapon, inline=False)
        embed.add_field(name="🛡️ 装備防具", value=equipped_armor, inline=False)
        
        return embed


class MerchantBuyView(View):
    def __init__(self, user_id, player_data):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.player_data = player_data
        self.generate_merchant_items()
        self.add_item_selects()
    
    def generate_merchant_items(self):
        """商人が販売するアイテムをランダム生成"""
        distance = self.player_data.get("distance", 0)
        
        # 距離に応じた価格範囲
        base_price_multiplier = 1.0 + (distance / 5000)
        
        # ランダムで5-8個のアイテムを生成
        self.items_for_sale = []
        
        # 武器2-3個
        weapon_count = random.randint(2, 3)
        all_weapons = [name for name, data in game.ITEMS_DATABASE.items() if data.get("type") == "weapon"]
        for _ in range(weapon_count):
            weapon_name = random.choice(all_weapons)
            weapon_data = game.ITEMS_DATABASE[weapon_name]
            base_price = weapon_data.get("price", 100)
            price = int(base_price * base_price_multiplier * random.uniform(0.8, 1.3))
            self.items_for_sale.append({
                "name": weapon_name,
                "type": "weapon",
                "price": price,
                "attack": weapon_data.get("attack", 0)
            })
        
        # 防具2-3個
        armor_count = random.randint(2, 3)
        all_armors = [name for name, data in game.ITEMS_DATABASE.items() if data.get("type") == "armor"]
        for _ in range(armor_count):
            armor_name = random.choice(all_armors)
            armor_data = game.ITEMS_DATABASE[armor_name]
            base_price = armor_data.get("price", 100)
            price = int(base_price * base_price_multiplier * random.uniform(0.8, 1.3))
            self.items_for_sale.append({
                "name": armor_name,
                "type": "armor",
                "price": price,
                "defense": armor_data.get("defense", 0)
            })
        
        # ポーション1-2個
        potion_count = random.randint(1, 2)
        potions = ["HP回復薬（小）", "HP回復薬（中）", "HP回復薬（大）", "MP回復薬（小）", "MP回復薬（中）", "エリクサー"]
        for _ in range(potion_count):
            potion_name = random.choice(potions)
            potion_data = game.ITEMS_DATABASE[potion_name]
            base_price = potion_data.get("price", 50)
            price = int(base_price * base_price_multiplier * random.uniform(0.9, 1.2))
            self.items_for_sale.append({
                "name": potion_name,
                "type": "potion",
                "price": price
            })
    
    def add_item_selects(self):
        """アイテム選択用のSelectを追加"""
        options = []
        for i, item in enumerate(self.items_for_sale[:25]):  # 最大25個
            label = f"{item['name']} - {item['price']}G"
            description = f"{item['type'].upper()}"
            if "attack" in item:
                description += f" | 攻撃力: {item['attack']}"
            if "defense" in item:
                description += f" | 防御力: {item['defense']}"
            
            emoji_map = {"weapon": "⚔️", "armor": "🛡️", "potion": "🧪"}
            emoji = emoji_map.get(item["type"], "📦")
            
            options.append(discord.SelectOption(
                label=label[:100],
                description=description[:100],
                value=str(i),
                emoji=emoji
            ))
        
        if options:
            select = Select(
                placeholder="購入するアイテムを選択...",
                options=options,
                custom_id="buy_item_select"
            )
            select.callback = self.buy_item_callback
            self.add_item(select)
    
    async def buy_item_callback(self, interaction: discord.Interaction):
        """アイテム購入処理"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの取引ではありません！", ephemeral=True)
            return
        
        selected_idx = int(interaction.data['values'][0])
        item = self.items_for_sale[selected_idx]
        
        # プレイヤーデータ最新化
        player = await game.db.get_player(self.user_id)
        current_gold = player.get("gold", 0)
        
        if current_gold < item["price"]:
            await interaction.response.send_message(
                f"💰 ゴールドが足りません！ （必要: {item['price']}G / 所持: {current_gold}G）",
                ephemeral=True
            )
            return
        
        # 購入処理
        await game.db.add_gold(self.user_id, -item["price"])
        await game.db.add_item_to_inventory(self.user_id, item["name"])
        
        embed = discord.Embed(
            title="✅ 購入完了",
            description=f"**{item['name']}** を {item['price']}G で購入しました！",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class MerchantSellView(View):
    def __init__(self, user_id, player_data):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.player_data = player_data
        self.add_sell_select()
    
    def add_sell_select(self):
        """売却アイテム選択用のSelectを追加"""
        inventory = self.player_data.get("inventory", [])
        if not inventory:
            return
        
        options = []
        for i, item_name in enumerate(inventory[:25]):
            item_data = game.get_item_info(item_name)
            if not item_data:
                continue
            
            base_price = item_data.get("price", 10)
            sell_price = int(base_price * 0.5)  # 売却価格は50%
            
            label = f"{item_name} - {sell_price}G"
            description = f"{item_data.get('type', 'item').upper()}"
            
            emoji_map = {"weapon": "⚔️", "armor": "🛡️", "potion": "🧪", "material": "📦"}
            emoji = emoji_map.get(item_data.get("type"), "📦")
            
            options.append(discord.SelectOption(
                label=label[:100],
                description=description[:100],
                value=item_name,
                emoji=emoji
            ))
        
        if options:
            select = Select(
                placeholder="売却するアイテムを選択...",
                options=options,
                custom_id="sell_item_select"
            )
            select.callback = self.sell_item_callback
            self.add_item(select)
    
    async def sell_item_callback(self, interaction: discord.Interaction):
        """アイテム売却処理"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの取引ではありません！", ephemeral=True)
            return
        
        item_name = interaction.data['values'][0]
        item_data = game.get_item_info(item_name)
        
        if not item_data:
            await interaction.response.send_message("アイテム情報が見つかりません", ephemeral=True)
            return
        
        base_price = item_data.get("price", 10)
        sell_price = int(base_price * 0.5)
        
        # 売却処理
        await game.db.remove_item_from_inventory(self.user_id, item_name)
        await game.db.add_gold(self.user_id, sell_price)
        
        embed = discord.Embed(
            title="✅ 売却完了",
            description=f"**{item_name}** を {sell_price}G で売却しました！",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
