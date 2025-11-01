import discord
import db
import random
import asyncio
import game
from db import get_player, update_player, delete_player
import death_system
from titles import get_title_rarity_emoji, get_title_rarity_color
# -------------------------
# 名前入力View
# -------------------------
class NameRequestView(discord.ui.View):
    def __init__(self, user_id: int, channel: discord.TextChannel):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.channel = channel

    @discord.ui.button(label="名前を入力する", style=discord.ButtonStyle.primary)
    async def request_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("⚠️ あなたはこのチュートリアルを開始できません！", ephemeral=True)
            return
        # 名前入力モーダルを開く
        await interaction.response.send_modal(NameModal(self.user_id, self.channel))

# -------------------------
# 名前入力Modal
# -------------------------
class NameModal(discord.ui.Modal):
    def __init__(self, user_id: int, channel: discord.TextChannel):
        super().__init__(title="キャラクター名を入力")
        self.user_id = user_id
        self.channel = channel

        self.name_input = discord.ui.TextInput(
            label="あなたの名前は？",
            placeholder="例: 勇者タロウ",
            max_length=20
        )
        self.add_item(self.name_input)

    async def on_submit(self, interaction: discord.Interaction):
        player_name = self.name_input.value.strip()

        # DB更新（名前登録）
        await update_player(self.user_id, name=player_name)

        # 名前反映メッセージ
        await self.channel.send(
            embed=discord.Embed(
                title="🎉 ようこそ！",
                description=f"{player_name} さん、冒険の準備が整いました！",
                color=discord.Color.gold()
            )
        )

        # 倉庫チェック：アイテムがあれば取り出し選択を表示
        storage_items = await db.get_storage_items(self.user_id, include_taken=False)

        if storage_items:
            embed = discord.Embed(
                title="📦 倉庫にアイテムがあります！",
                description="前回の冒険で持ち帰ったアイテムが倉庫にあります。\n1つ取り出して冒険に持っていけます。",
                color=discord.Color.blue()
            )

            # プルダウンで選択肢を作成
            storage_view = StorageSelectView(self.user_id, self.channel, storage_items)
            await self.channel.send(embed=embed, view=storage_view)
        else:
            # 倉庫が空の場合は通常通りチュートリアル開始
            await self.channel.send(
                embed=discord.Embed(
                    title="第1節 ~冒険の始まり~",
                    description="あなたはこのダンジョンに迷い込んだ者。\n目を覚ますと、見知らぬ洞窟の中だった。\n体にはなにも身につけていない。そしてどこかで誰かの声がする――。\n\n『ようこそ、挑戦者よ。ここは終わりなき迷宮。』\n\n『最初の一歩を踏み出す準備はできているか？』",
                    color=discord.Color.purple()
                )
            )

            # チュートリアル開始
            tutorial_view = TutorialView(self.user_id)
            await self.channel.send(embed=tutorial_view.pages[0], view=tutorial_view)


# -------------------------
# 倉庫アイテム選択View
# -------------------------
class StorageSelectView(discord.ui.View):
    def __init__(self, user_id: int, channel: discord.TextChannel, storage_items: list):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.channel = channel
        self.storage_items = storage_items

        # プルダウンメニューを作成
        options = []
        for item_data in storage_items[:25]:  # 最大25個
            item_name = item_data.get("item_name", "不明なアイテム")
            item_type = item_data.get("item_type", "material")
            storage_id = item_data.get("id")

            # 絵文字を選択
            emoji_map = {
                "weapon": "⚔️",
                "armor": "🛡️",
                "potion": "🧪",
                "material": "📦"
            }
            emoji = emoji_map.get(item_type, "📦")

            # アイテム情報取得
            item_info = game.get_item_info(item_name)
            description = item_info.get("description", "")[:50] if item_info else ""

            options.append(discord.SelectOption(
                label=item_name,
                description=f"{item_type.upper()} - {description}",
                value=str(storage_id),
                emoji=emoji
            ))

        # "取り出さない"オプションも追加
        options.append(discord.SelectOption(
            label="取り出さない",
            description="倉庫からアイテムを取り出さずに冒険を開始",
            value="skip",
            emoji="❌"
        ))

        select = discord.ui.Select(
            placeholder="倉庫から取り出すアイテムを選択...",
            options=options,
            custom_id="storage_retrieve_select"
        )
        select.callback = self.retrieve_item
        self.add_item(select)

    async def retrieve_item(self, interaction: discord.Interaction):
        """選択されたアイテムを倉庫から取り出してインベントリに追加"""
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたの選択ではありません！", ephemeral=True)

        selected_value = interaction.data['values'][0]

        if selected_value == "skip":
            # 取り出さない場合
            embed = discord.Embed(
                title="📦 倉庫をスキップ 第1節 ~冒険の始まり~",
                description="倉庫からアイテムを取り出さずに冒険を開始します。\n\nあなたはこのダンジョンを踏破しに来た者。\n目を覚ますと、見知らぬ洞窟の中だった。\nなにも身につけていない。そしてどこかで誰かの声がする――。\n\n『ようこそ、挑戦者よ。ここは終わりなき迷宮。』\n\n『最初の一歩を踏み出す準備はできているか？』",
                color=discord.Color.grey()
            )
            await interaction.response.edit_message(embed=embed, view=None)

            # チュートリアル開始
            tutorial_view = TutorialView(self.user_id)
            await self.channel.send(embed=tutorial_view.pages[0], view=tutorial_view)
            return

        # アイテムを取り出す
        storage_id = int(selected_value)
        item_data = await db.get_storage_item_by_id(storage_id)

        if not item_data:
            await interaction.response.send_message("⚠️ アイテムが見つかりません。", ephemeral=True)
            return

        item_name = item_data.get("item_name")

        # 倉庫から取り出し（is_taken = True に設定）
        success = await db.take_from_storage(self.user_id, storage_id)

        if success:
            # インベントリに追加
            await db.add_item_to_inventory(self.user_id, item_name)

            embed = discord.Embed(
                title="✅ アイテムを取り出しました 第1節 ~冒険の始まり~",
                description=f"**{item_name}** を倉庫から取り出し、インベントリに追加しました！\n\nあなたはこのダンジョンを踏破しに来た者。\n目を覚ますと、見知らぬ洞窟の中だった。\n手には何故かアイテム、そしてどこかで誰かの声がする――。\n\n『ようこそ、挑戦者よ。ここは終わりなき迷宮。』\n\n『最初の一歩を踏み出す準備はできているか？』",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(embed=embed, view=None)

            # チュートリアル開始
            tutorial_view = TutorialView(self.user_id)
            await self.channel.send(embed=tutorial_view.pages[0], view=tutorial_view)
        else:
            await interaction.response.send_message("⚠️ アイテムの取り出しに失敗しました。", ephemeral=True)

# -------------------------
# 世界線説明View
# -------------------------
class TutorialView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.page = 0
        self.pages = [
            discord.Embed(
                title="なぜ……ここに？(1/5)",
                description="ここは『イニシエダンジョン』──100階層まで続く階層を持つのが特徴の謎のダンジョンだ。\n人工的に作られたかのように100m区切りで1階層となっているようだ……",
                color=discord.Color.purple()
            ),
            discord.Embed(
                title="なぜ……ここに？ (2/5)",
                description="多くの冒険者が挑み、帰らぬ者も数知れない…なぜこんな場所にいるんだ？",
                color=discord.Color.purple()
            ),
            discord.Embed(
                title="⚔ 基本操作 (3/5)",
                description="・`!move` で進む\n・敵に遭遇すると戦闘が始まる\n・勝利すると装備やお金が手に入る\n\nその他コマンドはサポートサーバーをご確認ください",
                color=discord.Color.green()
            ),
            discord.Embed(
                title="📘 冒険チャンネル (4/5)",
                description="ここはあなた専用の冒険チャンネルです。他のプレイヤーは謎の力によって立ち入れません。",
                color=discord.Color.blue()
            ),
            discord.Embed(
                title="✅ チュートリアル完了 (5/5)",
                description="考えてても仕方がない\n準備は整った！ まずは `!move` で進んでみよう！",
                color=discord.Color.gold()
            )
        ]

    async def update_page(self, interaction: discord.Interaction):
        embed = self.pages[self.page]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="⬅ BACK", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
        await self.update_page(interaction)

    @discord.ui.button(label="NEXT ➡", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < len(self.pages) - 1:
            self.page += 1
            await self.update_page(interaction)
        else:
            await interaction.response.edit_message(
                embed=discord.Embed(
                    title="🎉 チュートリアル終了！",
                    description="君の冒険がいよいよ始まる！ `!move` で歩みを進めよう。",
                    color=discord.Color.green()
                ),
                view=None
            )
            # チュートリアル完了（名前が設定されていることで完了とみなす）
            pass

#!resetコマンド時
# -------------------------
# Reset 用 View（1段階目）
# -------------------------
class ResetConfirmView(discord.ui.View):
    def __init__(self, author_id: int, cached_channel_id: int | None = None):
        super().__init__(timeout=120)  # 2分でキャンセル
        self.author_id = author_id
        # ボタン押された時に使うため、呼び出し元で channel_id を渡しておくと安全
        self.cached_channel_id = cached_channel_id

    @discord.ui.button(label="削除する", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 誰でも押せない。実行者以外は弾く
        if interaction.user.id != self.author_id:
            return await interaction.response.send_message("これはあなた専用の確認です。", ephemeral=True)

        # 1回目確認OK → 別 View に差し替え（2段階目）
        embed = discord.Embed(
            title="本当に削除しますか？（最終確認）",
            description="ここで該当データとチャンネルを完全に削除します。取り消しは不可能です。 \nよければ「本当に削除する」を押してください。",
            color=discord.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=ResetFinalConfirmView(self.author_id, self.cached_channel_id))

    @discord.ui.button(label="いいえ（キャンセル）", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            return await interaction.response.send_message("これはあなた専用の確認です。", ephemeral=True)
        embed = discord.Embed(title="キャンセルされました", description="データの削除は実行されませんでした。引き続き[イニシエダンジョン]をお楽しみください――", color=discord.Color.dark_gray())
        await interaction.response.edit_message(embed=embed, view=None)

# -------------------------
# Reset 用 View（2段階目：最終確認）
# -------------------------
class ResetFinalConfirmView(discord.ui.View):
    def __init__(self, author_id: int, cached_channel_id: int | None = None):
        super().__init__(timeout=120)
        self.author_id = author_id
        self.cached_channel_id = cached_channel_id

    @discord.ui.button(label="本当に削除する", style=discord.ButtonStyle.danger)
    async def final_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            return await interaction.response.send_message("これはあなた専用の確認です。", ephemeral=True)

        user_id_str = str(self.author_id)
        # DBから削除
        await delete_player(user_id_str)

        # チャンネル削除処理
        guild = interaction.guild
        user = interaction.user
        channel_name = f"{user.name}-冒険"

        # RPGカテゴリ内の該当チャンネルを検索
        category = discord.utils.get(guild.categories, name="RPG")
        if category:
            channel = discord.utils.get(category.channels, name=channel_name.lower())
            if channel:
                try:
                    await channel.delete()
                    channel_deleted = True
                except:
                    channel_deleted = False
            else:
                channel_deleted = False
        else:
            channel_deleted = False

        # 完了メッセージ
        if channel_deleted:
            description = "プレイヤーデータとチャンネルを削除しました。"
        else:
            description = "プレイヤーデータを削除しました。チャンネルが見つからなかったか、削除に失敗しました。\n\n管理者をお呼びください。"

        embed = discord.Embed(
            title="削除完了", 
            description=description, 
            color=discord.Color.green()
        )

        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="いいえ（戻る）", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            return await interaction.response.send_message("これはあなた専用の確認です。", ephemeral=True)
        embed = discord.Embed(title="キャンセルされました。引き続き[イニシエダンジョン]をお楽しみください――", color=discord.Color.dark_gray())
        await interaction.response.edit_message(embed=embed, view=None)



from discord.ui import View, button

class TreasureView(View):
    def __init__(self, user_id: int, user_processing: dict):
        super().__init__(timeout=30)
        self.user_id = user_id
        self.user_processing = user_processing
        self.message = None

    # ==============================
    # 「開ける」ボタン
    # ==============================
    @button(label="開ける", style=discord.ButtonStyle.green)
    async def open_treasure(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これは君の宝箱じゃない！", ephemeral=True)
            return

        # メッセージを保存
        if not self.message:
            self.message = interaction.message

        await interaction.response.defer()

        # 通常宝箱は必ず報酬
        await self.handle_reward(interaction)

        # ボタン無効化
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        # 処理完了フラグをクリア
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    # ==============================
    # 「開けない」ボタン
    # ==============================
    @button(label="開けない", style=discord.ButtonStyle.red)
    async def ignore_treasure(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これは君の宝箱じゃない！", ephemeral=True)
            return

        # メッセージを保存
        if not self.message:
            self.message = interaction.message

        embed = discord.Embed(
            title="💨 宝箱を無視した",
            description="慎重な判断だ……何も起こらなかった。",
            color=discord.Color.dark_grey()
        )
        await interaction.response.edit_message(embed=embed, view=None)

        # 処理完了フラグをクリア
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    # ==============================
    # 宝箱報酬処理
    # ==============================
    async def handle_reward(self, interaction: discord.Interaction):
        player = await get_player(interaction.user.id)
        if not player:
            embed = discord.Embed(
                title="⚠️ エラー",
                description="プレイヤーデータが見つかりません。`!start` でゲームを開始してください。",
                color=discord.Color.red()
            )
            msg = self.message or interaction.message
            await msg.edit(embed=embed, view=None)
            return

        embed = None
        secret_weapon_hit = False

        # シークレット武器の超低確率抽選（0.1% = 1/1000）
        if random.random() < 0.001:
            available_weapons = await db.get_available_secret_weapons()

            if available_weapons:
                secret_weapon = random.choice(available_weapons)

                await db.add_secret_weapon(interaction.user.id, secret_weapon['id'])
                await db.add_item_to_inventory(interaction.user.id, secret_weapon['name'])
                await db.increment_global_weapon_count(secret_weapon['id'])

                embed = discord.Embed(
                    title="……なんだこれは――。",
                    description=f"**{secret_weapon['name']}** と書いてある……シークレット武器というものらしい。\n\n{secret_weapon['ability']}\n⚔️ 攻撃力: {secret_weapon['attack']}\nとてつもなく強力な力が備わっている。注意しよう",
                    color=discord.Color.purple()
                )

                secret_weapon_hit = True

                try:
                    bot = interaction.client
                    log_channel = bot.get_channel(1424712515396305007)
                    if log_channel:
                        await log_channel.send(
                            f" **{interaction.user.mention} がシークレット武器を発見！**\n"
                            f"**{secret_weapon['name']}** を手に入れた！\n"
                            f"レアリティ: {secret_weapon['rarity']}\n"
                            f"サーバー: {interaction.guild.name}"
                        )
                except Exception as e:
                    print(f"グローバルログ通知エラー: {e}")
        
        # シークレット武器が出た場合はそのEmbedを表示
        if secret_weapon_hit and embed:
            msg = self.message or interaction.message
            await interaction.followup.send(embed=embed)
        else:
            # 通常の宝箱報酬を処理
            await self.open_treasure_box(interaction, player, secret_weapon_hit)

    async def open_treasure_box(self, interaction, player, secret_weapon_hit):
        if not secret_weapon_hit:
            reward_type = random.choices(
                ["coins", "weapon"],
                weights=[70, 30],
                k=1
            )[0]

            if reward_type == "coins":
                amount = random.randint(30, 60)
                await db.add_gold(interaction.user.id, amount)

                embed = discord.Embed(
                    title="💰 宝箱の中身",
                    description=f"{amount}ゴールドを手に入れた！",
                    color=discord.Color.gold()
                )

            else:
                distance = player.get("distance", 0)
                available_equipment = game.get_treasure_box_equipment(distance)
                weapon_name = random.choice(available_equipment) if available_equipment else "木の剣"
                await db.add_item_to_inventory(interaction.user.id, weapon_name)
                item_info = game.get_item_info(weapon_name)

                embed = discord.Embed(
                    title="🗡️ 宝箱の中身",
                    description=f"**{weapon_name}** を手に入れた！\n\n{item_info.get('description', '')}",
                    color=discord.Color.green()
                )

            msg = self.message or interaction.message
            await msg.edit(embed=embed, view=None)


    # ==============================
    # トラップ発動処理
    # ==============================
    async def handle_trap(self, interaction: discord.Interaction, trap_type: str):
        player = await get_player(interaction.user.id)
        if not player:
            embed = discord.Embed(
                title="⚠️ エラー",
                description="プレイヤーデータが見つかりません。`!start` でゲームを開始してください。",
                color=discord.Color.red()
            )
            msg = self.message or interaction.message
            await msg.edit(embed=embed, view=None)
            return

        msg = self.message or interaction.message

        # --- HP20%ダメージ ---
        if trap_type == "damage":
            damage = int(player.get("hp", 50) * 0.2)
            new_hp = max(0, player.get("hp", 50) - damage)
            await update_player(interaction.user.id, hp=new_hp)

            embed = discord.Embed(
                title="💥 トラップ発動！",
                description=f"爆発が起きた！\n{damage}のダメージを受けた！\nこのダンジョンにはトラップチェストがある。気をつけよう――。\n\n残りHP: {new_hp}",
                color=discord.Color.red()
            )
            await msg.edit(embed=embed, view=None)


        # --- 奇襲（戦闘突入） ---
        elif trap_type == "ambush":
            embed = discord.Embed(
                title="😈 奇襲発生！",
                description="突如、敵が現れた！戦闘に備えて――",
                color=discord.Color.dark_red()
            )
            await msg.edit(embed=embed, view=None)

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

# ==============================
# トラップ宝箱View
# ==============================
class TrapChestView(View):
    def __init__(self, user_id: int, user_processing: dict, player: dict):
        super().__init__(timeout=30)
        self.user_id = user_id
        self.user_processing = user_processing
        self.player = player

    @button(label="開ける", style=discord.ButtonStyle.danger)
    async def open_trap_chest(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これは君の宝箱じゃない！", ephemeral=True)
            return

        await interaction.response.defer()

        # トラップ必ず発動
        trap_types = ["damage", "remove_weapon", "ambush"]
        trap_type = random.choice(trap_types)

        await self.handle_trap(interaction, trap_type)

        # ボタン無効化
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)

        # 処理完了フラグをクリア
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    @button(label="開けない", style=discord.ButtonStyle.secondary)
    async def ignore_trap_chest(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これは君の宝箱じゃない！", ephemeral=True)
            return

        embed = discord.Embed(
            title="🚶 立ち去った",
            description="見るからに怪しい宝箱を開けずに立ち去った。\n賢明な判断だ…",
            color=discord.Color.dark_grey()
        )
        await interaction.response.edit_message(embed=embed, view=None)

        # 処理完了フラグをクリア
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    async def handle_trap(self, interaction: discord.Interaction, trap_type: str):
        player = await get_player(interaction.user.id)
        if not player:
            embed = discord.Embed(
                title="⚠️ エラー",
                description="プレイヤーデータが見つかりません。",
                color=discord.Color.red()
            )
            await interaction.message.edit(embed=embed, view=None)
            return

        if trap_type == "damage":
            damage = random.randint(10, 20)
            new_hp = max(1, player.get("hp", 50) - damage)
            await update_player(interaction.user.id, hp=new_hp)

            embed = discord.Embed(
                title="💥 トラップ発動！",
                description=f"毒ガスが噴出した！\n{damage}のダメージを受けた！\n残りHP: {new_hp}",
                color=discord.Color.red()
            )
            await interaction.message.edit(embed=embed, view=None)

        elif trap_type == "ambush":
            embed = discord.Embed(
                title="😈 奇襲発生！",
                description="突如、敵が現れた！戦闘に備えて――",
                color=discord.Color.dark_red()
            )
            await interaction.message.edit(embed=embed, view=None)

            await asyncio.sleep(2)

            distance = player.get("distance", 0)
            enemy = game.get_random_enemy(distance)

            player_data = {
                "hp": player.get("hp", 50),
                "attack": player.get("attack", 5),
                "defense": player.get("defense", 2),
                "inventory": player.get("inventory", []),
                "distance": distance,
                "user_id": interaction.user.id
            }

            try:
                class FakeContext:
                    def __init__(self, interaction):
                        self.interaction = interaction
                        self.author = interaction.user
                        self.channel = interaction.channel

                    async def send(self, *args, **kwargs):
                        return await self.channel.send(*args, **kwargs)

                fake_ctx = FakeContext(interaction)
                view = await BattleView.create(fake_ctx, player_data, enemy, self.user_processing)
                await view.send_initial_embed()
            except Exception as e:
                print(f"[Error] BattleView transition failed: {e}")

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

# ==============================
# 500m特殊イベントView
# ==============================
class SpecialEventView(View):
    def __init__(self, user_id: int, user_processing: dict, distance: int):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.user_processing = user_processing
        self.distance = distance

    @button(label="🔨 鍛冶屋", style=discord.ButtonStyle.primary)
    async def blacksmith_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのイベントではありません！", ephemeral=True)
            return

        await interaction.response.defer()

        player = await get_player(interaction.user.id)
        if not player:
            embed = discord.Embed(
                title="⚠️ エラー",
                description="プレイヤーデータが見つかりません。",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=embed, view=None)
            return

        inventory = player.get("inventory", [])
        materials = {}
        for item in inventory:
            if item in game.MATERIAL_PRICES:
                materials[item] = materials.get(item, 0) + 1

        if not materials:
            embed = discord.Embed(
                title="🔨 鍛冶屋",
                description="「おっと、素材が何もないようだな。素材を集めてきてくれ」\n\n他の選択肢を選んでください。",
                color=discord.Color.orange()
            )
            for child in self.children:
                if child.label == "🔨 鍛冶屋":
                    child.disabled = True
            await interaction.edit_original_response(embed=embed, view=self)
            return

        from views import BlacksmithView
        view = BlacksmithView(self.user_id, self.user_processing, materials)
        await interaction.edit_original_response(content=None, embed=view.get_embed(), view=view)

    @button(label="💰 素材商人", style=discord.ButtonStyle.success)
    async def material_merchant_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのイベントではありません！", ephemeral=True)
            return

        await interaction.response.defer()

        player = await get_player(interaction.user.id)
        if not player:
            embed = discord.Embed(
                title="⚠️ エラー",
                description="プレイヤーデータが見つかりません。",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=embed, view=None)
            return

        inventory = player.get("inventory", [])
        materials = {}
        for item in inventory:
            if item in game.MATERIAL_PRICES:
                materials[item] = materials.get(item, 0) + 1

        if not materials:
            embed = discord.Embed(
                title="💰 素材商人",
                description="「素材が何もないのか？もったいない…」\n\n他の選択肢を選んでください。",
                color=discord.Color.orange()
            )
            for child in self.children:
                if child.label == "💰 素材商人":
                    child.disabled = True
            await interaction.edit_original_response(embed=embed, view=self)
            return

        from views import MaterialMerchantView
        view = MaterialMerchantView(self.user_id, self.user_processing, materials)
        await interaction.edit_original_response(content=None, embed=view.get_embed(), view=view)

    @button(label="👹 特殊な敵", style=discord.ButtonStyle.danger)
    async def special_enemy(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのイベントではありません！", ephemeral=True)
            return

        await interaction.response.defer()

        player = await get_player(interaction.user.id)
        if not player:
            return

        special_enemies = [
            {"name": "財宝の守護者", "hp": 200, "atk": 20, "def": 10, "gold_drop": (200, 500)},
            {"name": "レアモンスター", "hp": 150, "atk": 25, "def": 8, "gold_drop": (300, 600)}
        ]
        enemy = random.choice(special_enemies)

        embed = discord.Embed(
            title="👹 特殊な敵が現れた！",
            description=f"**{enemy['name']}** が立ちはだかる！\n通常の敵より強力だが、報酬も豪華だ！",
            color=discord.Color.dark_red()
        )
        await interaction.message.edit(embed=embed, view=None)

        await asyncio.sleep(2)

        player_data = {
            "hp": player.get("hp", 50),
            "attack": player.get("attack", 5),
            "defense": player.get("defense", 2),
            "inventory": player.get("inventory", []),
            "distance": self.distance,
            "user_id": interaction.user.id
        }

        class FakeContext:
            def __init__(self, interaction):
                self.interaction = interaction
                self.author = interaction.user
                self.channel = interaction.channel

            async def send(self, *args, **kwargs):
                return await self.channel.send(*args, **kwargs)

        fake_ctx = FakeContext(interaction)
        view = await BattleView.create(fake_ctx, player_data, enemy, self.user_processing)
        await view.send_initial_embed()

    @button(label="📖 ストーリー", style=discord.ButtonStyle.secondary)
    async def story_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたのイベントではありません！", ephemeral=True)
            return

        await interaction.response.defer()

        stories = [
            {
                "title": "古の碑文",
                "description": "壁に刻まれた文字を発見した。\n\n「深淵を覗く者は、深淵にも覗かれている」\n\n…不吉な予感がする。注意して進もう。",
                "reward": "wisdom_bonus"
            },
            {
                "title": "謎の声",
                "description": "???「よう。お前も勇敢だな。とっとと逃げた方がいいぜ。逃げられない？どうにか頑張ってくれ」\n\n誰かの声が聞こえた気がした。\n誰なんだこの無責任すぎるやつは……",
                "reward": "courage_bonus"
            },
            {
                "title": "休息の泉",
                "description": "不思議な泉を発見した。\n水を飲むと体力が回復した！\n\n現在のHP[100]",
                "reward": "hp_restore"
            }
        ]

        story = random.choice(stories)

        embed = discord.Embed(
            title=f"📖 {story['title']}",
            description=story['description'],
            color=discord.Color.purple()
        )

        if story['reward'] == "hp_restore":
            player = await get_player(interaction.user.id)
            if player:
                max_hp = player.get("max_hp", 50)
                await update_player(interaction.user.id, hp=max_hp)
                embed.add_field(name="✨ 効果", value="HPが全回復した！", inline=False)

        await interaction.edit_original_response(embed=embed, view=None)

        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False


# ==============================
# ラスボスクリア時のアイテム持ち帰りView
# ==============================
from collections import Counter

class FinalBossClearView(discord.ui.View):
    def __init__(self, user_id: int, ctx, user_processing: dict, boss_stage: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.ctx = ctx
        self.user_processing = user_processing
        self.boss_stage = boss_stage

    @classmethod
    async def create(cls, user_id: int, ctx, user_processing: dict, boss_stage: int):
        """Async factory method to create and initialize FinalBossClearView"""
        instance = cls(user_id, ctx, user_processing, boss_stage)
        await instance._async_init()
        return instance

    async def _async_init(self):
        """Async initialization logic"""
        # クリア処理を実行
        clear_result = await db.handle_boss_clear(self.user_id)

        # インベントリからアイテム選択プルダウンを作成
        player = await db.get_player(self.user_id)
        inventory = player.get("inventory", []) if player else []

        if inventory:
            # アイテムをカウント（集約）
            item_counts = Counter(inventory)
            
            # アイテムを選択肢に変換（最大25個）
            options = []
            for i, (item_name, count) in enumerate(list(item_counts.items())[:25]):
                item_info = game.get_item_info(item_name)
                item_type = item_info.get("type", "material") if item_info else "material"

                # 絵文字を選択
                emoji_map = {
                    "weapon": "⚔️",
                    "armor": "🛡️",
                    "potion": "🧪",
                    "material": "📦"
                }
                emoji = emoji_map.get(item_type, "📦")

                # ラベルに個数表示
                label = f"{item_name} ×{count}" if count > 1 else item_name
                desc = f"{item_type.upper()} - {item_info.get('description', '')[:50]}" if item_info else item_type.upper()

                options.append(discord.SelectOption(
                    label=label,
                    description=desc,
                    value=f"{i}_{item_name}",  # インデックスを付けて重複回避
                    emoji=emoji
                ))

            # プルダウンを作成
            select = discord.ui.Select(
                placeholder="倉庫に持ち帰るアイテムを1つ選択...",
                options=options,
                custom_id="storage_select"
            )
            select.callback = self.store_item
            self.add_item(select)

    async def store_item(self, interaction: discord.Interaction):
        """選択されたアイテムを倉庫に保管"""
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたの選択ではありません！", ephemeral=True)

        selected_value = interaction.data['values'][0]
        
        # valueから型とアイテム名を分離
        parts = selected_value.split("_", 1)
        if len(parts) < 2:
            return await interaction.response.send_message("不正な選択です。", ephemeral=True)
        
        idx, selected_item = parts

        # アイテム情報取得
        item_info = game.get_item_info(selected_item)
        item_type = item_info.get("type", "material") if item_info else "material"

        # 倉庫に保存
        success = await db.add_to_storage(interaction.user.id, selected_item, item_type)

        if success:
            embed = discord.Embed(
                title="📦 アイテムを倉庫に保管しました",
                description=f"**{selected_item}** を倉庫に保管しました。\n次回 `!start` 時に倉庫から取り出せます。\n\n**!reset** でデータをリセットして新しい冒険を始めましょう！",
                color=discord.Color.green()
            )
            embed.add_field(
                name="⚠️ 重要",
                value="このダンジョンは踏破済です。`!reset` を実行するまで `!move` などのコマンドは使用できません。",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="⚠️ エラー",
                description="倉庫への保管に失敗しました。サポートサーバーにお問い合わせください。\n**!resetを行わないでください**",
                color=discord.Color.red()
            )

        await interaction.response.edit_message(embed=embed, view=None)

        # 通知チャンネルへ送信
        try:
            notification_channel = self.ctx.bot.get_channel(1424712515396305007)
            if notification_channel:
                notify_embed = discord.Embed(
                    title="🎉 ラスボス討伐成功！",
                    description=f"**{interaction.user.name}** がラスボスを討伐し、**{selected_item}** を倉庫に保管した！",
                    color=discord.Color.gold()
                )
                await notification_channel.send(embed=notify_embed)
        except Exception as e:
            print(f"通知チャンネルへの送信エラー: {e}")

        # boss_postストーリー表示
        story_id = f"boss_post_{self.boss_stage}"
        if not await db.get_story_flag(interaction.user.id, story_id):
            await asyncio.sleep(2)
            from story import StoryView
            view = StoryView(interaction.user.id, story_id, self.user_processing)
            await view.send_story(self.ctx)
            return

        if self.ctx.author.id in self.user_processing:
            self.user_processing[self.ctx.author.id] = False

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.ctx.author.id in self.user_processing:
            self.user_processing[self.ctx.author.id] = False

# ==============================
# ラスボス戦View
# ==============================
class FinalBossBattleView(View):
    def __init__(self, ctx, player, boss, user_processing: dict, boss_stage: int):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player = player
        self.boss = boss
        self.message = None
        self.user_processing = user_processing
        self.boss_stage = boss_stage

    @classmethod
    async def create(cls, ctx, player, boss, user_processing: dict, boss_stage: int):
        """Async factory method to create and initialize FinalBossBattleView"""
        instance = cls(ctx, player, boss, user_processing, boss_stage)
        await instance._async_init()
        return instance

    async def _async_init(self):
        """Async initialization logic"""
        if "user_id" in self.player:
            fresh_player = await db.get_player(self.player["user_id"])
            if fresh_player:
                self.player.update({
                    "hp": fresh_player.get("hp", self.player.get("hp", 50)),
                    "max_hp": fresh_player.get("max_hp", self.player.get("max_hp", 50)),
                    "mp": fresh_player.get("mp", self.player.get("mp", 20)),
                    "max_mp": fresh_player.get("max_mp", self.player.get("max_mp", 20)),
                    "attack": fresh_player.get("atk", self.player.get("attack", 5)),
                    "defense": fresh_player.get("def", self.player.get("defense", 2))
                })
            
            equipment_bonus = await game.calculate_equipment_bonus(self.player["user_id"])
            self.player["attack"] = self.player.get("attack", 5) + equipment_bonus["attack_bonus"]
            self.player["defense"] = self.player.get("defense", 2) + equipment_bonus["defense_bonus"]

            unlocked_skills = await db.get_unlocked_skills(self.player["user_id"])
            if unlocked_skills:
                skill_options = []
                for skill_id in unlocked_skills[:25]:
                    skill_info = game.get_skill_info(skill_id)
                    if skill_info:
                        skill_options.append(discord.SelectOption(
                            label=skill_info["name"],
                            description=f"MP:{skill_info['mp_cost']} - {skill_info['description'][:50]}",
                            value=skill_id
                        ))

                if skill_options:
                    skill_select = discord.ui.Select(
                        placeholder="スキルを選択",
                        options=skill_options,
                        custom_id="final_skill_select"
                    )
                    skill_select.callback = self.use_skill
                    self.add_item(skill_select)

    async def send_initial_embed(self):
        embed = await self.create_battle_embed()
        self.message = await self.ctx.send(embed=embed, view=self)

    async def create_battle_embed(self):
        embed = discord.Embed(
            title="⚔️ 最終決戦！",
            description=f"**{self.boss['name']}** との最後の戦い！\n\nこいつを倒せば……ダンジョン踏破だ――。",
            color=discord.Color.dark_gold()
        )
        embed.add_field(
            name="💀 ラスボスの情報",
            value=f"HP：{self.boss['hp']}\n攻撃力：{self.boss['atk']}\n防御力：{self.boss['def']}",
            inline=False
        )

        if "user_id" in self.player:
            player_data = await db.get_player(self.player["user_id"])
            mp = player_data.get("mp", 20) if player_data else 20
            max_mp = player_data.get("max_mp", 20) if player_data else 20
            player_info = f"HP：{self.player['hp']}\nMP：{mp}/{max_mp}\n攻撃力：{self.player['attack']}\n防御力：{self.player['defense']}"
        else:
            player_info = f"HP：{self.player['hp']}\n攻撃力：{self.player['attack']}\n防御力：{self.player['defense']}"

        embed.add_field(
            name="🧍‍♂️ あなたの情報",
            value=player_info,
            inline=False
        )
        embed.set_footer(text="全力で戦え！")
        return embed

    async def update_embed(self, text=""):
        embed = await self.create_battle_embed()
        if text:
            embed.description += f"\n\n{text}"
        await self.message.edit(embed=embed, view=self)

    # =====================================
    # ✨ スキル使用
    # =====================================
    async def use_skill(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # アトミックなロックチェック（ロック取得できなければ処理中）
        if self._battle_lock.locked():
            return await interaction.response.send_message("⚠️ 処理中です。少々お待ちください。", ephemeral=True)
        
        async with self._battle_lock:
            try:
                # ボタンを即座に無効化
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

                # ✅ プレイヤーデータを最新化
                fresh_player_data = await db.get_player(interaction.user.id)
                if fresh_player_data:
                    self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
                    self.player["mp"] = fresh_player_data.get("mp", self.player.get("mp", 20))
                    self.player["max_hp"] = fresh_player_data.get("max_hp", self.player.get("max_hp", 50))
                    self.player["max_mp"] = fresh_player_data.get("max_mp", self.player.get("max_mp", 20))
                    
                    # ✅ 装備ボーナスを再計算してattackとdefenseを更新
                    base_atk = fresh_player_data.get("atk", 5)
                    base_def = fresh_player_data.get("def", 2)
                    equipment_bonus = await game.calculate_equipment_bonus(interaction.user.id)
                    self.player["attack"] = base_atk + equipment_bonus["attack_bonus"]
                    self.player["defense"] = base_def + equipment_bonus["defense_bonus"]
                    print(f"[DEBUG] use_skill - プレイヤーデータ最新化: HP={self.player['hp']}, MP={self.player['mp']}, ATK={base_atk}+{equipment_bonus['attack_bonus']}={self.player['attack']}")

                if await db.is_mp_stunned(interaction.user.id):
                    await db.set_mp_stunned(interaction.user.id, False)
                    await interaction.response.send_message("⚠️ MP枯渇で行動不能！\n『嘘だろ!?』\n次のターンから行動可能になります。", ephemeral=True)
                    # ボタンを再有効化
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return

                skill_id = interaction.data['values'][0]
                skill_info = game.get_skill_info(skill_id)

                if not skill_info:
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message("⚠️ スキル情報が見つかりません。", ephemeral=True)

                player_data = await db.get_player(interaction.user.id)
                current_mp = player_data.get("mp", 20)
                mp_cost = skill_info["mp_cost"]

                if current_mp < mp_cost:
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message(f"⚠️ MPが足りません！（必要: {mp_cost}, 現在: {current_mp}）", ephemeral=True)

                if not await db.consume_mp(interaction.user.id, mp_cost):
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message("⚠️ MP消費に失敗しました。", ephemeral=True)

                player_data = await db.get_player(interaction.user.id)
                if player_data and player_data.get("mp", 0) == 0:
                    await db.set_mp_stunned(interaction.user.id, True)

                text = f"✨ **{skill_info['name']}** を使用！（MP -{mp_cost}）\n"

                if skill_info["type"] == "attack":
                    base_damage = max(0, self.player["attack"] + random.randint(-3, 3) - self.enemy["def"])
                    skill_damage = int(base_damage * skill_info["power"])
                    self.enemy["hp"] -= skill_damage
                    text += f"⚔️ {skill_damage} のダメージを与えた！"

                    if self.enemy["hp"] <= 0:
                        await db.update_player(interaction.user.id, hp=self.player["hp"])
                        distance = self.player.get("distance", 0)
                        drop_result = game.get_enemy_drop(self.enemy["name"], distance)

                        drop_text = ""
                        if drop_result:
                            if drop_result["type"] == "coins":
                                await db.add_gold(interaction.user.id, drop_result["amount"])
                                drop_text = f"\n💰 **{drop_result['amount']}コイン** を手に入れた！"
                            elif drop_result["type"] == "item":
                                await db.add_item_to_inventory(interaction.user.id, drop_result["name"])
                                drop_text = f"\n🎁 **{drop_result['name']}** を手に入れた！"

                        await self.update_embed(text + "\n🏆 敵を倒した！" + drop_text)
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        await interaction.response.defer()
                        return

                    enemy_dmg = max(0, self.enemy["atk"] + random.randint(-2, 2) - self.player["defense"])
                    self.player["hp"] -= enemy_dmg
                    self.player["hp"] = max(0, self.player["hp"])
                    text += f"\n敵の反撃！ {enemy_dmg} のダメージを受けた！"

                    if self.player["hp"] <= 0:
                        death_result = await handle_death_with_triggers(
                            self.ctx if hasattr(self, 'ctx') else interaction.channel,
                            interaction.user.id, 
                            self.user_processing if hasattr(self, 'user_processing') else {},
                            enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                            enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                        )
                        if death_result:
                            await self.update_embed(text + f"\n💀 あなたは倒れた…\n\n🔄 周回リスタート\n📍 アップグレードポイント: +{death_result['points']}pt")
                        else:
                            await self.update_embed(text + "\n💀 あなたは倒れた…")
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        await interaction.response.defer()
                        return

                elif skill_info["type"] == "heal":
                    heal_amount = skill_info["heal_amount"]
                    max_hp = self.player.get("max_hp", 50)
                    old_hp = self.player["hp"]
                    self.player["hp"] = min(max_hp, self.player["hp"] + heal_amount)
                    actual_heal = self.player["hp"] - old_hp
                    text += f"💚 HP+{actual_heal} 回復した！"

                await db.update_player(interaction.user.id, hp=self.player["hp"])
                await self.update_embed(text)
                # ボタンを再有効化
                for child in self.children:
                    child.disabled = False
                await self.message.edit(view=self)
                await interaction.response.defer()
            
            except Exception as e:
                print(f"[BattleView] use_skill error: {e}")
                import traceback
                traceback.print_exc()
                # エラー時もボタンを再有効化
                for child in self.children:
                    child.disabled = False
                try:
                    await self.message.edit(view=self)
                    if not interaction.response.is_done():
                        await interaction.response.send_message("⚠️ エラーが発生しました。もう一度お試しください。", ephemeral=True)
                except:
                    pass

    @button(label="戦う", style=discord.ButtonStyle.danger, emoji="⚔️")
    async def fight(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        if await db.is_mp_stunned(interaction.user.id):
            await db.set_mp_stunned(interaction.user.id, False)
            text = "⚠️ MP枯渇で行動不能…次のターンから行動可能になります。"
            await self.update_embed(text)
            await interaction.response.defer()
            return

        # プレイヤー攻撃
        base_damage = max(0, self.player["attack"] + random.randint(-5, 5) - self.boss["def"])

        # ability効果を適用
        enemy_type = "boss"
        equipment_bonus = await game.calculate_equipment_bonus(self.player["user_id"]) if "user_id" in self.player else {}
        weapon_ability = equipment_bonus.get("weapon_ability", "")

        ability_result = game.apply_ability_effects(base_damage, weapon_ability, self.player["hp"], enemy_type)

        player_dmg = ability_result["damage"]
        self.boss["hp"] -= player_dmg

        # HP吸収
        if ability_result["lifesteal"] > 0:
            self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + ability_result["lifesteal"])

        # 召喚回復
        if ability_result.get("summon_heal", 0) > 0:
            self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + ability_result["summon_heal"])

        # 自傷ダメージ
        if ability_result.get("self_damage", 0) > 0:
            self.player["hp"] -= ability_result["self_damage"]
            self.player["hp"] = max(0, self.player["hp"])

        text = f"あなたの攻撃！ {player_dmg} のダメージを与えた！"
        if ability_result["effect_text"]:
            text += f"\n{ability_result['effect_text']}"

        # 即死判定（ボス戦では無効）
        if ability_result["instant_kill"]:
            text += "\n💀即死効果発動！...しかしボスには効かなかった！"

        if self.boss["hp"] <= 0:
            # HPを保存
            await db.update_player(interaction.user.id, hp=self.player["hp"])
            await db.set_boss_defeated(interaction.user.id, self.boss_stage)

            reward_gold = random.randint(10000, 20000)
            await db.add_gold(interaction.user.id, reward_gold)

            embed = discord.Embed(
                title="🎉 ダンジョンクリア！",
                description=f"**{self.boss['name']}** を倒した！\n\n🏆 ダンジョンを踏破した――\n💰 {reward_gold}ゴールドを手に入れた！",
                color=discord.Color.gold()
            )

            self.disable_all_items()

            # ラスボスクリア時の選択Viewを表示
            clear_view = await FinalBossClearView.create(interaction.user.id, self.ctx, self.user_processing, self.boss_stage)
            await interaction.message.edit(embed=embed, view=clear_view)
            await interaction.response.defer()
            return

        # 怯み効果で敵がスキップ
        if ability_result.get("enemy_flinch", False):
            text += "\nラスボスは怯んで動けない！"
            # HPを保存
            await db.update_player(interaction.user.id, hp=self.player["hp"])
            await self.update_embed(text)
            await interaction.response.defer()
            return

        # 凍結効果で敵がスキップ
        if ability_result.get("freeze", False):
            text += "\nラスボスは凍結して動けない！"
            # HPを保存
            await db.update_player(interaction.user.id, hp=self.player["hp"])
            await self.update_embed(text)
            await interaction.response.defer()
            return

        # ラスボス反撃
        enemy_base_dmg = max(0, self.boss["atk"] + random.randint(-3, 3) - self.player["defense"])

        # 防具効果を適用
        armor_ability = equipment_bonus.get("armor_ability", "")
        armor_result = game.apply_armor_effects(
            enemy_base_dmg, 
            armor_ability, 
            self.player["hp"], 
            self.player.get("max_hp", 50),
            enemy_base_dmg,
            self.boss.get("attribute", "none")
        )

        if armor_result["evaded"]:
            text += f"\nラスボスの攻撃！ {armor_result['effect_text']}"
        else:
            enemy_dmg = armor_result["damage"]
            self.player["hp"] -= enemy_dmg
            self.player["hp"] = max(0, self.player["hp"])
            text += f"\nラスボスの反撃！ {enemy_dmg} のダメージを受けた！"
            if armor_result["effect_text"]:
                text += f"\n{armor_result['effect_text']}"

            # 反撃ダメージ
            if armor_result["counter_damage"] > 0:
                self.boss["hp"] -= armor_result["counter_damage"]
                if self.boss["hp"] <= 0:
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    text += "\n反撃でラスボスを倒した！"
                    await db.set_boss_defeated(interaction.user.id, self.boss_stage)
                    reward_gold = random.randint(10000, 20000)
                    await db.add_gold(interaction.user.id, reward_gold)
                    embed = discord.Embed(
                        title="🎉 ダンジョンクリア！",
                        description=f"反撃で **{self.boss['name']}** を倒した！\n\n🏆 ダンジョンを踏破した――\n💰 {reward_gold}ゴールドを手に入れた！",
                        color=discord.Color.gold()
                    )
                    embed.add_field(
                        name="📦 アイテムを倉庫に保管", 
                        value="インベントリから1つアイテムを選んで倉庫に保管できます。\n次回 `!start` 時に倉庫から取り出せます。", 
                        inline=False
                    )
                    self.disable_all_items()
                    await interaction.message.edit(embed=embed, view=None)
                    await interaction.response.defer()

                    # アイテム持ち帰りViewを表示
                    storage_view = await FinalBossClearView.create(interaction.user.id, self.ctx, self.user_processing, self.boss_stage)
                    storage_embed = discord.Embed(
                        title="📦 倉庫にアイテムを保管",
                        description="インベントリから1つ選んで倉庫に保管してください。\n次回の冒険で取り出すことができます。",
                        color=discord.Color.blue()
                    )
                    await interaction.channel.send(embed=storage_embed, view=storage_view)
                    return

            # 反射ダメージ
            if armor_result["reflect_damage"] > 0:
                self.boss["hp"] -= armor_result["reflect_damage"]
                if self.boss["hp"] <= 0:
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    text += "\n反射ダメージでラスボスを倒した！"
                    await db.set_boss_defeated(interaction.user.id, self.boss_stage)
                    reward_gold = random.randint(10000, 20000)
                    await db.add_gold(interaction.user.id, reward_gold)
                    embed = discord.Embed(
                        title="🎉 ダンジョンクリア！",
                        description=f"反射ダメージで **{self.boss['name']}** を倒した！\n\n🏆 ダンジョンを制覇した！\n💰 {reward_gold}ゴールドを手に入れた！",
                        color=discord.Color.gold()
                    )
                    embed.add_field(
                        name="📦 アイテムを倉庫に保管", 
                        value="インベントリから1つアイテムを選んで倉庫に保管できます。\n次回 `!start` 時に倉庫から取り出せます。", 
                        inline=False
                    )
                    self.disable_all_items()
                    await interaction.message.edit(embed=embed, view=None)
                    await interaction.response.defer()

                    # アイテム持ち帰りViewを表示
                    storage_view = await FinalBossClearView.create(interaction.user.id, self.ctx, self.user_processing, self.boss_stage)
                    storage_embed = discord.Embed(
                        title="📦 倉庫にアイテムを保管",
                        description="インベントリから1つ選んで倉庫に保管してください。\n次回の冒険で取り出すことができます。",
                        color=discord.Color.blue()
                    )
                    await interaction.channel.send(embed=storage_embed, view=storage_view)
                    return

            # HP回復
            if armor_result["hp_regen"] > 0:
                self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + armor_result["hp_regen"])

            if self.player["hp"] <= 0:
                if armor_result.get("revived", False):
                    self.player["hp"] = 1
                    text += "\n蘇生効果で生き残った！"
                else:
                    # 【重要】先にインタラクションに応答
                    await interaction.response.defer()

                    # 死亡処理 + トリガーチェック
                    death_result = await handle_death_with_triggers(
                        self.ctx,
                        interaction.user.id,
                        self.user_processing,
                        enemy_name=self.boss.get('name', '不明'),
                        enemy_type='boss'
                    )

                    # 死亡通知を送信
                    try:
                        notify_channel = interaction.client.get_channel(1424712515396305007)
                        if notify_channel and death_result:
                            distance = death_result.get("distance", 0)
                            await notify_channel.send(
                                f"💀 {interaction.user.mention} がラスボス戦で倒れた…\n"
                                f"到達距離: {distance}m"
                            )
                    except Exception as e:
                        print(f"通知送信エラー: {e}")

                    if death_result:
                        await self.update_embed(
                            text + f"\n\n💀 あなたは倒れた…\n\n⭐ {death_result['points']}アップグレードポイントを獲得！"
                        )
                    else:
                        await self.update_embed(text + "\n💀 あなたは倒れた…")

                    self.disable_all_items()
                    await self.message.edit(view=self)

                    if self.ctx.author.id in self.user_processing:
                        self.user_processing[self.ctx.author.id] = False
                    return

            # 生存している場合
            await interaction.response.defer()
            await self.update_embed(text)

    @button(label="防御", style=discord.ButtonStyle.secondary, emoji="🛡️")
    async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        reduction = random.randint(40, 70)
        enemy_dmg = max(0, int((self.boss["atk"] + random.randint(-3, 3)) * (1 - reduction / 100)) - self.player["defense"])
        self.player["hp"] -= enemy_dmg
        self.player["hp"] = max(0, self.player["hp"])

        text = f"防御した！ ダメージを {reduction}% 軽減！\nラスボスの攻撃で {enemy_dmg} のダメージを受けた！"

        if self.player["hp"] <= 0:
            # 【重要】先にインタラクションに応答
            await interaction.response.defer()

            # 死亡処理 + トリガーチェック
            death_result = await handle_death_with_triggers(
                self.ctx,
                interaction.user.id,
                self.user_processing,
                enemy_name=self.boss.get('name', '不明'),
                enemy_type='boss'
            )

            # 死亡通知を送信
            try:
                notify_channel = interaction.client.get_channel(1424712515396305007)
                if notify_channel and death_result:
                    distance = death_result.get("distance", 0)
                    await notify_channel.send(
                        f"💀 {interaction.user.mention} がラスボス戦で倒れた…\n"
                        f"到達距離: {distance}m"
                    )
            except Exception as e:
                print(f"通知送信エラー: {e}")

            if death_result:
                await self.update_embed(
                    text + f"\n\n💀 あなたは倒れた…\n\n⭐ {death_result['points']}アップグレードポイントを獲得！"
                )
            else:
                await self.update_embed(text + "\n💀 あなたは倒れた…")

            self.disable_all_items()
            await self.message.edit(view=self)

            if self.ctx.author.id in self.user_processing:
                self.user_processing[self.ctx.author.id] = False
            return

        # 生存している場合
        await interaction.response.defer()
        await self.update_embed(text)

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.ctx.author.id in self.user_processing:
            self.user_processing[self.ctx.author.id] = False

# ==============================
# ボス戦View
# ==============================
class BossBattleView(View):
    def __init__(self, ctx, player, boss, user_processing: dict, boss_stage: int):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player = player
        self.boss = boss
        self.message = None
        self.user_processing = user_processing
        self.boss_stage = boss_stage

    @classmethod
    async def create(cls, ctx, player, boss, user_processing: dict, boss_stage: int):
        """Async factory method to create and initialize BossBattleView"""
        instance = cls(ctx, player, boss, user_processing, boss_stage)
        await instance._async_init()
        return instance

    async def _async_init(self):
        """Async initialization logic"""
        fresh_boss = game.get_boss(self.boss_stage)
        if fresh_boss:
            self.boss = fresh_boss
            print(f"[DEBUG] ボス初期化 - {self.boss['name']}: HP={self.boss['hp']}, ATK={self.boss['atk']}, DEF={self.boss['def']}")
        
        if "user_id" in self.player:
            fresh_player = await db.get_player(self.player["user_id"])
            if fresh_player:
                self.player.update({
                    "hp": fresh_player.get("hp", self.player.get("hp", 50)),
                    "max_hp": fresh_player.get("max_hp", self.player.get("max_hp", 50)),
                    "mp": fresh_player.get("mp", self.player.get("mp", 20)),
                    "max_mp": fresh_player.get("max_mp", self.player.get("max_mp", 20)),
                    "attack": fresh_player.get("atk", self.player.get("attack", 5)),
                    "defense": fresh_player.get("def", self.player.get("defense", 2))
                })
            
            equipment_bonus = await game.calculate_equipment_bonus(self.player["user_id"])
            self.player["attack"] = self.player.get("attack", 5) + equipment_bonus["attack_bonus"]
            self.player["defense"] = self.player.get("defense", 2) + equipment_bonus["defense_bonus"]

            unlocked_skills = await db.get_unlocked_skills(self.player["user_id"])
            if unlocked_skills:
                skill_options = []
                for skill_id in unlocked_skills[:25]:
                    skill_info = game.get_skill_info(skill_id)
                    if skill_info:
                        skill_options.append(discord.SelectOption(
                            label=skill_info["name"],
                            description=f"MP:{skill_info['mp_cost']} - {skill_info['description'][:50]}",
                            value=skill_id
                        ))

                if skill_options:
                    skill_select = discord.ui.Select(
                        placeholder="スキルを選択",
                        options=skill_options,
                        custom_id="boss_skill_select"
                    )
                    skill_select.callback = self.use_skill
                    self.add_item(skill_select)

    async def send_initial_embed(self):
        embed = await self.create_battle_embed()
        self.message = await self.ctx.send(embed=embed, view=self)

    async def create_battle_embed(self):
        embed = discord.Embed(
            title="🔥 ボス戦！",
            description=f"強大な敵が立ちはだかる！\n\n**{self.boss['name']}**",
            color=discord.Color.dark_red()
        )
        embed.add_field(
            name="💀 ボスの情報",
            value=f"HP：{self.boss['hp']}\n攻撃力：{self.boss['atk']}\n防御力：{self.boss['def']}",
            inline=False
        )

        if "user_id" in self.player:
            player_data = await db.get_player(self.player["user_id"])
            mp = player_data.get("mp", 20) if player_data else 20
            max_mp = player_data.get("max_mp", 20) if player_data else 20
            player_info = f"HP：{self.player['hp']}\nMP：{mp}/{max_mp}\n攻撃力：{self.player['attack']}\n防御力：{self.player['defense']}"
        else:
            player_info = f"HP：{self.player['hp']}\n攻撃力：{self.player['attack']}\n防御力：{self.player['defense']}"

        embed.add_field(
            name="🧍‍♂️ あなたの情報",
            value=player_info,
            inline=False
        )
        embed.set_footer(text="行動を選択してください。")
        return embed

    async def update_embed(self, text=""):
        embed = await self.create_battle_embed()
        if text:
            embed.description += f"\n\n{text}"
        await self.message.edit(embed=embed, view=self)

    # =====================================
    # ✨ スキル使用
    # =====================================
    async def use_skill(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # アトミックなロックチェック（ロック取得できなければ処理中）
        if self._battle_lock.locked():
            return await interaction.response.send_message("⚠️ 処理中です。少々お待ちください。", ephemeral=True)
        
        async with self._battle_lock:
            try:
                # ボタンを即座に無効化
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

                # ✅ プレイヤーデータを最新化
                fresh_player_data = await db.get_player(interaction.user.id)
                if fresh_player_data:
                    self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
                    self.player["mp"] = fresh_player_data.get("mp", self.player.get("mp", 20))
                    self.player["max_hp"] = fresh_player_data.get("max_hp", self.player.get("max_hp", 50))
                    self.player["max_mp"] = fresh_player_data.get("max_mp", self.player.get("max_mp", 20))
                    
                    # ✅ 装備ボーナスを再計算してattackとdefenseを更新
                    base_atk = fresh_player_data.get("atk", 5)
                    base_def = fresh_player_data.get("def", 2)
                    equipment_bonus = await game.calculate_equipment_bonus(interaction.user.id)
                    self.player["attack"] = base_atk + equipment_bonus["attack_bonus"]
                    self.player["defense"] = base_def + equipment_bonus["defense_bonus"]
                    print(f"[DEBUG] use_skill - プレイヤーデータ最新化: HP={self.player['hp']}, MP={self.player['mp']}, ATK={base_atk}+{equipment_bonus['attack_bonus']}={self.player['attack']}")

                if await db.is_mp_stunned(interaction.user.id):
                    await db.set_mp_stunned(interaction.user.id, False)
                    await interaction.response.send_message("⚠️ MP枯渇で行動不能！\n『嘘だろ!?』\n次のターンから行動可能になります。", ephemeral=True)
                    # ボタンを再有効化
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return

                skill_id = interaction.data['values'][0]
                skill_info = game.get_skill_info(skill_id)

                if not skill_info:
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message("⚠️ スキル情報が見つかりません。", ephemeral=True)

                player_data = await db.get_player(interaction.user.id)
                current_mp = player_data.get("mp", 20)
                mp_cost = skill_info["mp_cost"]

                if current_mp < mp_cost:
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message(f"⚠️ MPが足りません！（必要: {mp_cost}, 現在: {current_mp}）", ephemeral=True)

                if not await db.consume_mp(interaction.user.id, mp_cost):
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message("⚠️ MP消費に失敗しました。", ephemeral=True)

                player_data = await db.get_player(interaction.user.id)
                if player_data and player_data.get("mp", 0) == 0:
                    await db.set_mp_stunned(interaction.user.id, True)

                text = f"✨ **{skill_info['name']}** を使用！（MP -{mp_cost}）\n"

                if skill_info["type"] == "attack":
                    base_damage = max(0, self.player["attack"] + random.randint(-3, 3) - self.enemy["def"])
                    skill_damage = int(base_damage * skill_info["power"])
                    self.enemy["hp"] -= skill_damage
                    text += f"⚔️ {skill_damage} のダメージを与えた！"

                    if self.enemy["hp"] <= 0:
                        await db.update_player(interaction.user.id, hp=self.player["hp"])
                        distance = self.player.get("distance", 0)
                        drop_result = game.get_enemy_drop(self.enemy["name"], distance)

                        drop_text = ""
                        if drop_result:
                            if drop_result["type"] == "coins":
                                await db.add_gold(interaction.user.id, drop_result["amount"])
                                drop_text = f"\n💰 **{drop_result['amount']}コイン** を手に入れた！"
                            elif drop_result["type"] == "item":
                                await db.add_item_to_inventory(interaction.user.id, drop_result["name"])
                                drop_text = f"\n🎁 **{drop_result['name']}** を手に入れた！"

                        await self.update_embed(text + "\n🏆 敵を倒した！" + drop_text)
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        await interaction.response.defer()
                        return

                    enemy_dmg = max(0, self.enemy["atk"] + random.randint(-2, 2) - self.player["defense"])
                    self.player["hp"] -= enemy_dmg
                    self.player["hp"] = max(0, self.player["hp"])
                    text += f"\n敵の反撃！ {enemy_dmg} のダメージを受けた！"

                    if self.player["hp"] <= 0:
                        death_result = await handle_death_with_triggers(
                            self.ctx if hasattr(self, 'ctx') else interaction.channel,
                            interaction.user.id, 
                            self.user_processing if hasattr(self, 'user_processing') else {},
                            enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                            enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                        )
                        if death_result:
                            await self.update_embed(text + f"\n💀 あなたは倒れた…\n\n🔄 周回リスタート\n📍 アップグレードポイント: +{death_result['points']}pt")
                        else:
                            await self.update_embed(text + "\n💀 あなたは倒れた…")
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        await interaction.response.defer()
                        return

                elif skill_info["type"] == "heal":
                    heal_amount = skill_info["heal_amount"]
                    max_hp = self.player.get("max_hp", 50)
                    old_hp = self.player["hp"]
                    self.player["hp"] = min(max_hp, self.player["hp"] + heal_amount)
                    actual_heal = self.player["hp"] - old_hp
                    text += f"💚 HP+{actual_heal} 回復した！"

                await db.update_player(interaction.user.id, hp=self.player["hp"])
                await self.update_embed(text)
                # ボタンを再有効化
                for child in self.children:
                    child.disabled = False
                await self.message.edit(view=self)
                await interaction.response.defer()
            
            except Exception as e:
                print(f"[BattleView] use_skill error: {e}")
                import traceback
                traceback.print_exc()
                # エラー時もボタンを再有効化
                for child in self.children:
                    child.disabled = False
                try:
                    await self.message.edit(view=self)
                    if not interaction.response.is_done():
                        await interaction.response.send_message("⚠️ エラーが発生しました。もう一度お試しください。", ephemeral=True)
                except:
                    pass

    @button(label="戦う", style=discord.ButtonStyle.danger, emoji="⚔️")
    async def fight(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        if await db.is_mp_stunned(interaction.user.id):
            await db.set_mp_stunned(interaction.user.id, False)
            text = "⚠️ MP枯渇で行動不能…\n『嘘だろ!?』\n次のターンから行動可能になります。"
            await self.update_embed(text)
            await interaction.response.defer()
            return

        # プレイヤー攻撃
        base_damage = max(0, self.player["attack"] + random.randint(-5, 5) - self.boss["def"])

        # ability効果を適用
        enemy_type = "boss"
        equipment_bonus = await game.calculate_equipment_bonus(self.player["user_id"]) if "user_id" in self.player else {}
        weapon_ability = equipment_bonus.get("weapon_ability", "")

        ability_result = game.apply_ability_effects(base_damage, weapon_ability, self.player["hp"], enemy_type)

        player_dmg = ability_result["damage"]
        self.boss["hp"] -= player_dmg

        # HP吸収
        if ability_result["lifesteal"] > 0:
            self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + ability_result["lifesteal"])

        # 召喚回復
        if ability_result.get("summon_heal", 0) > 0:
            self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + ability_result["summon_heal"])

        # 自傷ダメージ
        if ability_result.get("self_damage", 0) > 0:
            self.player["hp"] -= ability_result["self_damage"]
            self.player["hp"] = max(0, self.player["hp"])

        text = f"あなたの攻撃！ {player_dmg} のダメージを与えた！"
        if ability_result["effect_text"]:
            text += f"\n{ability_result['effect_text']}"

        # 即死判定（ボス戦では無効）
        if ability_result["instant_kill"]:
            text += "\n💀即死効果発動！...しかしボスには効かなかった！"

        if self.boss["hp"] <= 0:
            # HPを保存
            await db.update_player(interaction.user.id, hp=self.player["hp"])
            await db.set_boss_defeated(interaction.user.id, self.boss_stage)

            reward_gold = random.randint(500, 1000)
            await db.add_gold(interaction.user.id, reward_gold)

            # ボス撃破通知を送信
            try:
                notify_channel = interaction.client.get_channel(1424712515396305007)
                if notify_channel:
                    await notify_channel.send(
                        f"⚔️ {interaction.user.mention} がステージ{self.boss_stage}のボス「{self.boss['name']}」を撃破した！"
                    )
            except Exception as e:
                print(f"通知送信エラー: {e}")

            await self.update_embed(text + f"\n\n🏆 ボスを倒した！\n💰 {reward_gold}ゴールドを手に入れた！")
            self.disable_all_items()
            await self.message.edit(view=self)

            story_id = f"boss_post_{self.boss_stage}"
            if not await db.get_story_flag(interaction.user.id, story_id):
                await asyncio.sleep(2)
                from story import StoryView
                view = StoryView(interaction.user.id, story_id, self.user_processing)
                await view.send_story(self.ctx)
                return

            if self.ctx.author.id in self.user_processing:
                self.user_processing[self.ctx.author.id] = False
            return

        # 怯み効果で敵がスキップ
        if ability_result.get("enemy_flinch", False):
            text += "\nボスは怯んで動けない！"
            # HPを保存
            await db.update_player(interaction.user.id, hp=self.player["hp"])
            await self.update_embed(text)
            await interaction.response.defer()
            return

        # 凍結効果で敵がスキップ
        if ability_result.get("freeze", False):
            text += "\nボスは凍結して動けない！"
            # HPを保存
            await db.update_player(interaction.user.id, hp=self.player["hp"])
            await self.update_embed(text)
            await interaction.response.defer()
            return

        # ボス反撃
        enemy_base_dmg = max(0, self.boss["atk"] + random.randint(-3, 3) - self.player["defense"])

        # 防具効果を適用
        armor_ability = equipment_bonus.get("armor_ability", "")
        armor_result = game.apply_armor_effects(
            enemy_base_dmg, 
            armor_ability, 
            self.player["hp"], 
            self.player.get("max_hp", 50),
            enemy_base_dmg,
            self.boss.get("attribute", "none")
        )

        if armor_result["evaded"]:
            text += f"\nボスの攻撃！ {armor_result['effect_text']}"
        else:
            enemy_dmg = armor_result["damage"]
            self.player["hp"] -= enemy_dmg
            self.player["hp"] = max(0, self.player["hp"])
            text += f"\nボスの反撃！ {enemy_dmg} のダメージを受けた！"
            if armor_result["effect_text"]:
                text += f"\n{armor_result['effect_text']}"

            # 反撃ダメージ
            if armor_result["counter_damage"] > 0:
                self.boss["hp"] -= armor_result["counter_damage"]
                if self.boss["hp"] <= 0:
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    text += "\n反撃でボスを倒した！"
                    await db.set_boss_defeated(interaction.user.id, self.boss_stage)
                    reward_gold = random.randint(500, 1000)
                    await db.add_gold(interaction.user.id, reward_gold)
                    await self.update_embed(text + f"\n💰 {reward_gold}ゴールドを手に入れた！")
                    self.disable_all_items()
                    await self.message.edit(view=self)

                    story_id = f"boss_post_{self.boss_stage}"
                    if not await db.get_story_flag(interaction.user.id, story_id):
                        await asyncio.sleep(2)
                        from story import StoryView
                        view = StoryView(interaction.user.id, story_id, self.user_processing)
                        await view.send_story(self.ctx)
                        return

                    if self.ctx.author.id in self.user_processing:
                        self.user_processing[self.ctx.author.id] = False
                    return

            # 反射ダメージ
            if armor_result["reflect_damage"] > 0:
                self.boss["hp"] -= armor_result["reflect_damage"]
                if self.boss["hp"] <= 0:
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    text += "\n反射ダメージでボスを倒した！"
                    await db.set_boss_defeated(interaction.user.id, self.boss_stage)
                    reward_gold = random.randint(500, 1000)
                    await db.add_gold(interaction.user.id, reward_gold)
                    await self.update_embed(text + f"\n💰 {reward_gold}ゴールドを手に入れた！")
                    self.disable_all_items()
                    await self.message.edit(view=self)

                    story_id = f"boss_post_{self.boss_stage}"
                    if not await db.get_story_flag(interaction.user.id, story_id):
                        await asyncio.sleep(2)
                        from story import StoryView
                        view = StoryView(interaction.user.id, story_id, self.user_processing)
                        await view.send_story(self.ctx)
                        return

                    if self.ctx.author.id in self.user_processing:
                        self.user_processing[self.ctx.author.id] = False
                    return

            # HP回復
            if armor_result["hp_regen"] > 0:
                self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + armor_result["hp_regen"])

        if self.player["hp"] <= 0:
            if armor_result.get("revived", False):
                self.player["hp"] = 1
                text += "\n蘇生効果で生き残った！"
            else:
                death_result = await handle_death_with_triggers(
                    self.ctx if hasattr(self, 'ctx') else interaction.channel,
                    interaction.user.id, 
                    self.user_processing if hasattr(self, 'user_processing') else {},
                    enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                    enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                )

                # 死亡通知を送信
                try:
                    notify_channel = interaction.client.get_channel(1424712515396305007)
                    if notify_channel:
                        player = await db.get_player(interaction.user.id)
                        distance = player.get("distance", 0) if player else 0
                        await notify_channel.send(
                            f"💀 {interaction.user.mention} がボス戦で倒れた…\n"
                            f"到達距離: {distance}m"
                        )
                except Exception as e:
                    print(f"通知送信エラー: {e}")

                if death_result:
                    await self.update_embed(
                        text + f"\n\n💀 あなたは倒れた…\n\n⭐ {death_result['points']}アップグレードポイントを獲得！\n（死亡回数: {death_result['death_count']}回）"
                    )
                else:
                    await self.update_embed(text + "\n💀 あなたは倒れた…")

                self.disable_all_items()
                await self.message.edit(view=self)

                if self.ctx.author.id in self.user_processing:
                    self.user_processing[self.ctx.author.id] = False
                return

        await self.update_embed(text)
        await interaction.response.defer()

    @button(label="防御", style=discord.ButtonStyle.secondary, emoji="🛡️")
    async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        reduction = random.randint(30, 60)
        enemy_dmg = max(0, int((self.boss["atk"] + random.randint(-3, 3)) * (1 - reduction / 100)) - self.player["defense"])
        self.player["hp"] -= enemy_dmg
        self.player["hp"] = max(0, self.player["hp"])

        text = f"防御した！ ダメージを {reduction}% 軽減！\nボスの攻撃で {enemy_dmg} のダメージを受けた！"

        if self.player["hp"] <= 0:
            death_result = await handle_death_with_triggers(
                self.ctx if hasattr(self, 'ctx') else interaction.channel,
                interaction.user.id, 
                self.user_processing if hasattr(self, 'user_processing') else {},
                enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                enemy_type='boss' if hasattr(self, 'boss') else 'normal'
            )
            if death_result:
                await self.update_embed(
                    text + f"\n\n💀 あなたは倒れた…\n\n⭐ {death_result['points']}アップグレードポイントを獲得！"
                )
            else:
                await self.update_embed(text + "\n💀 あなたは倒れた…")

            self.disable_all_items()
            await self.message.edit(view=self)

            if self.ctx.author.id in self.user_processing:
                self.user_processing[self.ctx.author.id] = False
            return

        # HPを保存
        await db.update_player(interaction.user.id, hp=self.player["hp"])
        await self.update_embed(text)
        await interaction.response.defer()

    def disable_all_items(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.ctx.author.id in self.user_processing:
            self.user_processing[self.ctx.author.id] = False

#戦闘Embed
import discord
from discord.ui import View, button, Select
import random

class BattleView(View):
    def __init__(self, ctx, player, enemy, user_processing: dict):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player = player  # { "hp": int, "attack": int, "defense": int, "inventory": [ ... ] }
        self.enemy = enemy    # { "name": str, "hp": int, "atk": int, "def": int }
        self.message = None
        self.user_processing = user_processing
        self._battle_lock = asyncio.Lock()  # アトミックなロック機構

    @classmethod
    async def create(cls, ctx, player, enemy, user_processing: dict):
        """Async factory method to create and initialize BattleView"""
        instance = cls(ctx, player, enemy, user_processing)
        await instance._async_init()
        return instance

    async def _async_init(self):
        """Async initialization logic"""
        if "user_id" in self.player:
            equipment_bonus = await game.calculate_equipment_bonus(self.player["user_id"])
            self.player["attack"] = self.player.get("attack", 10) + equipment_bonus["attack_bonus"]
            self.player["defense"] = self.player.get("defense", 5) + equipment_bonus["defense_bonus"]

            unlocked_skills = await db.get_unlocked_skills(self.player["user_id"])
            if unlocked_skills:
                skill_options = []
                for skill_id in unlocked_skills[:25]:
                    skill_info = game.get_skill_info(skill_id)
                    if skill_info:
                        skill_options.append(discord.SelectOption(
                            label=skill_info["name"],
                            description=f"MP:{skill_info['mp_cost']} - {skill_info['description'][:50]}",
                            value=skill_id
                        ))

                if skill_options:
                    skill_select = discord.ui.Select(
                        placeholder="スキルを選択",
                        options=skill_options,
                        custom_id="skill_select"
                    )
                    skill_select.callback = self.use_skill
                    self.add_item(skill_select)

    async def send_initial_embed(self):
        embed = await self.create_battle_embed()
        self.message = await self.ctx.send(embed=embed, view=self)

    async def create_battle_embed(self):
        embed = discord.Embed(
            title="⚔️ 戦闘開始！",
            description=f"敵が現れた！：**{self.enemy['name']}**",
            color=0xff4444
        )
        embed.add_field(
            name="💀 敵の情報",
            value=f"HP：{self.enemy['hp']}\n攻撃力：{self.enemy['atk']}\n防御力：{self.enemy['def']}",
            inline=False
        )

        if "user_id" in self.player:
            player_data = await db.get_player(self.player["user_id"])
            mp = player_data.get("mp", 20) if player_data else 20
            max_mp = player_data.get("max_mp", 20) if player_data else 20
            player_info = f"HP：{self.player['hp']}\nMP：{mp}/{max_mp}\n攻撃力：{self.player['attack']}\n防御力：{self.player['defense']}"
        else:
            player_info = f"HP：{self.player['hp']}\n攻撃力：{self.player['attack']}\n防御力：{self.player['defense']}"

        embed.add_field(
            name="🧍‍♂️ あなたの情報",
            value=player_info,
            inline=False
        )
        embed.set_footer(text="行動を選択してください。")
        return embed

    async def update_embed(self, text=""):
        embed = await self.create_battle_embed()
        if text:
            embed.description += f"\n\n{text}"
        await self.message.edit(embed=embed, view=self)

    # =====================================
    # ✨ スキル使用
    # =====================================
    async def use_skill(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # アトミックなロックチェック（ロック取得できなければ処理中）
        if self._battle_lock.locked():
            return await interaction.response.send_message("⚠️ 処理中です。少々お待ちください。", ephemeral=True)
        
        async with self._battle_lock:
            try:
                # ボタンを即座に無効化
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

                # ✅ プレイヤーデータを最新化
                fresh_player_data = await db.get_player(interaction.user.id)
                if fresh_player_data:
                    self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
                    self.player["mp"] = fresh_player_data.get("mp", self.player.get("mp", 20))
                    self.player["max_hp"] = fresh_player_data.get("max_hp", self.player.get("max_hp", 50))
                    self.player["max_mp"] = fresh_player_data.get("max_mp", self.player.get("max_mp", 20))
                    
                    # ✅ 装備ボーナスを再計算してattackとdefenseを更新
                    base_atk = fresh_player_data.get("atk", 5)
                    base_def = fresh_player_data.get("def", 2)
                    equipment_bonus = await game.calculate_equipment_bonus(interaction.user.id)
                    self.player["attack"] = base_atk + equipment_bonus["attack_bonus"]
                    self.player["defense"] = base_def + equipment_bonus["defense_bonus"]
                    print(f"[DEBUG] use_skill - プレイヤーデータ最新化: HP={self.player['hp']}, MP={self.player['mp']}, ATK={base_atk}+{equipment_bonus['attack_bonus']}={self.player['attack']}")

                if await db.is_mp_stunned(interaction.user.id):
                    await db.set_mp_stunned(interaction.user.id, False)
                    await interaction.response.send_message("⚠️ MP枯渇で行動不能！\n『嘘だろ!?』\n次のターンから行動可能になります。", ephemeral=True)
                    # ボタンを再有効化
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return

                skill_id = interaction.data['values'][0]
                skill_info = game.get_skill_info(skill_id)

                if not skill_info:
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message("⚠️ スキル情報が見つかりません。", ephemeral=True)

                player_data = await db.get_player(interaction.user.id)
                current_mp = player_data.get("mp", 20)
                mp_cost = skill_info["mp_cost"]

                if current_mp < mp_cost:
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message(f"⚠️ MPが足りません！（必要: {mp_cost}, 現在: {current_mp}）", ephemeral=True)

                if not await db.consume_mp(interaction.user.id, mp_cost):
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return await interaction.response.send_message("⚠️ MP消費に失敗しました。", ephemeral=True)

                player_data = await db.get_player(interaction.user.id)
                if player_data and player_data.get("mp", 0) == 0:
                    await db.set_mp_stunned(interaction.user.id, True)

                text = f"✨ **{skill_info['name']}** を使用！（MP -{mp_cost}）\n"

                if skill_info["type"] == "attack":
                    base_damage = max(0, self.player["attack"] + random.randint(-3, 3) - self.enemy["def"])
                    skill_damage = int(base_damage * skill_info["power"])
                    self.enemy["hp"] -= skill_damage
                    text += f"⚔️ {skill_damage} のダメージを与えた！"

                    if self.enemy["hp"] <= 0:
                        await db.update_player(interaction.user.id, hp=self.player["hp"])
                        distance = self.player.get("distance", 0)
                        drop_result = game.get_enemy_drop(self.enemy["name"], distance)

                        drop_text = ""
                        if drop_result:
                            if drop_result["type"] == "coins":
                                await db.add_gold(interaction.user.id, drop_result["amount"])
                                drop_text = f"\n💰 **{drop_result['amount']}コイン** を手に入れた！"
                            elif drop_result["type"] == "item":
                                await db.add_item_to_inventory(interaction.user.id, drop_result["name"])
                                drop_text = f"\n🎁 **{drop_result['name']}** を手に入れた！"

                        await self.update_embed(text + "\n🏆 敵を倒した！" + drop_text)
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        await interaction.response.defer()
                        return

                    enemy_dmg = max(0, self.enemy["atk"] + random.randint(-2, 2) - self.player["defense"])
                    self.player["hp"] -= enemy_dmg
                    self.player["hp"] = max(0, self.player["hp"])
                    text += f"\n敵の反撃！ {enemy_dmg} のダメージを受けた！"

                    if self.player["hp"] <= 0:
                        death_result = await handle_death_with_triggers(
                            self.ctx if hasattr(self, 'ctx') else interaction.channel,
                            interaction.user.id, 
                            self.user_processing if hasattr(self, 'user_processing') else {},
                            enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                            enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                        )
                        if death_result:
                            await self.update_embed(text + f"\n💀 あなたは倒れた…\n\n🔄 周回リスタート\n📍 アップグレードポイント: +{death_result['points']}pt")
                        else:
                            await self.update_embed(text + "\n💀 あなたは倒れた…")
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        await interaction.response.defer()
                        return

                elif skill_info["type"] == "heal":
                    heal_amount = skill_info["heal_amount"]
                    max_hp = self.player.get("max_hp", 50)
                    old_hp = self.player["hp"]
                    self.player["hp"] = min(max_hp, self.player["hp"] + heal_amount)
                    actual_heal = self.player["hp"] - old_hp
                    text += f"💚 HP+{actual_heal} 回復した！"

                await db.update_player(interaction.user.id, hp=self.player["hp"])
                await self.update_embed(text)
                # ボタンを再有効化
                for child in self.children:
                    child.disabled = False
                await self.message.edit(view=self)
                await interaction.response.defer()
            
            except Exception as e:
                print(f"[BattleView] use_skill error: {e}")
                import traceback
                traceback.print_exc()
                # エラー時もボタンを再有効化
                for child in self.children:
                    child.disabled = False
                try:
                    await self.message.edit(view=self)
                    if not interaction.response.is_done():
                        await interaction.response.send_message("⚠️ エラーが発生しました。もう一度お試しください。", ephemeral=True)
                except:
                    pass

    # =====================================
    # 🗡️ 戦う
    # =====================================
    @button(label="戦う", style=discord.ButtonStyle.danger, emoji="🗡️")
    async def fight(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 権限チェック
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # アトミックなロックチェック（ロック取得できなければ処理中）
        if self._battle_lock.locked():
            return await interaction.response.send_message("⚠️ 処理中です。少々お待ちください。", ephemeral=True)
        
        # 先にdeferしてタイムアウトを回避
        await interaction.response.defer()
        
        async with self._battle_lock:
            try:
                # ボタンを即座に無効化
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

                # ✅ プレイヤーデータを最新化
                fresh_player_data = await db.get_player(interaction.user.id)
                if fresh_player_data:
                    self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
                    self.player["max_hp"] = fresh_player_data.get("max_hp", self.player.get("max_hp", 50))
                    
                    # ✅ 装備ボーナスを再計算してattackとdefenseを更新
                    base_atk = fresh_player_data.get("atk", 5)
                    base_def = fresh_player_data.get("def", 2)
                    equipment_bonus = await game.calculate_equipment_bonus(interaction.user.id)
                    self.player["attack"] = base_atk + equipment_bonus["attack_bonus"]
                    self.player["defense"] = base_def + equipment_bonus["defense_bonus"]
                    print(f"[DEBUG] fight - プレイヤーデータ最新化: HP={self.player['hp']}, ATK={base_atk}+{equipment_bonus['attack_bonus']}={self.player['attack']}, DEF={base_def}+{equipment_bonus['defense_bonus']}={self.player['defense']}")

                # MP枯渇チェック
                if await db.is_mp_stunned(interaction.user.id):
                    await db.set_mp_stunned(interaction.user.id, False)
                    text = "⚠️ MP枯渇で行動不能…\n『嘘だろ!?』\n次のターンから行動可能になります。"
                    await self.update_embed(text)
                    # ボタンを再有効化
                    for child in self.children:
                        child.disabled = False
                    await self.message.edit(view=self)
                    return

                # プレイヤー攻撃
                base_damage = max(0, self.player["attack"] + random.randint(-3, 3) - self.enemy["def"])

                # ability効果を適用
                enemy_type = game.get_enemy_type(self.enemy["name"])
                equipment_bonus = await game.calculate_equipment_bonus(self.player["user_id"]) if "user_id" in self.player else {}
                weapon_ability = equipment_bonus.get("weapon_ability", "")

                ability_result = game.apply_ability_effects(base_damage, weapon_ability, self.player["hp"], enemy_type)
                
                player_dmg = ability_result["damage"]
                self.enemy["hp"] -= player_dmg

                # HP吸収
                if ability_result["lifesteal"] > 0:
                    self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + ability_result["lifesteal"])

                # 召喚回復
                if ability_result.get("summon_heal", 0) > 0:
                    self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + ability_result["summon_heal"])

                # 自傷ダメージ
                if ability_result.get("self_damage", 0) > 0:
                    self.player["hp"] -= ability_result["self_damage"]
                    self.player["hp"] = max(0, self.player["hp"])

                text = f"あなたの攻撃！ {player_dmg} のダメージを与えた！"
                if ability_result["effect_text"]:
                    text += f"\n{ability_result['effect_text']}"

                # 即死判定
                if ability_result["instant_kill"]:
                    self.enemy["hp"] = 0

                # 勝利チェック
                if self.enemy["hp"] <= 0:
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])

                    # ドロップアイテムを取得
                    distance = self.player.get("distance", 0)
                    drop_result = game.get_enemy_drop(self.enemy["name"], distance)

                    drop_text = ""
                    if drop_result:
                        if drop_result["type"] == "coins":
                            await db.add_gold(interaction.user.id, drop_result["amount"])
                            drop_text = f"\n💰 **{drop_result['amount']}コイン** を手に入れた！"
                        elif drop_result["name"] == "none":
                            drop_text = f"\n **敵は何も落とさなかった...**"
                        elif drop_result["type"] == "item":
                            await db.add_item_to_inventory(interaction.user.id, drop_result["name"])
                            drop_text = f"\n🎁 **{drop_result['name']}** を手に入れた！"

                    await self.update_embed(text + "\n🏆 敵を倒した！" + drop_text)
                    self.disable_all_items()
                    await self.message.edit(view=self)
                    if self.ctx.author.id in self.user_processing:
                        self.user_processing[self.ctx.author.id] = False
                        # ロックはasync withで自動解放される
                    return

                # 怯み効果で敵がスキップ
                if ability_result.get("enemy_flinch", False):
                    text += "\n敵は怯んで動けない！\n『よしっ！』"
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    await self.update_embed(text)
                    # ロックはasync withで自動解放される
                    return

                # 凍結効果で敵がスキップ
                if ability_result.get("freeze", False):
                    text += "\n敵は凍結して動けない！"
                    # HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    await self.update_embed(text)
                    # ロックはasync withで自動解放される
                    return

                # 敵反撃
                enemy_base_dmg = max(0, self.enemy["atk"] + random.randint(-2, 2) - self.player["defense"])

                # 防具効果を適用
                armor_ability = equipment_bonus.get("armor_ability", "")
                armor_result = game.apply_armor_effects(
                    enemy_base_dmg, 
                    armor_ability, 
                    self.player["hp"], 
                    self.player.get("max_hp", 50),
                    enemy_base_dmg,
                    self.enemy.get("attribute", "none")
                )

                if armor_result["evaded"]:
                    text += f"\n敵の攻撃！ {armor_result['effect_text']}"
                else:
                    enemy_dmg = armor_result["damage"]
                    self.player["hp"] -= enemy_dmg
                    self.player["hp"] = max(0, self.player["hp"])
                    text += f"\n敵の反撃！ {enemy_dmg} のダメージを受けた！"
                    if armor_result["effect_text"]:
                        text += f"\n{armor_result['effect_text']}"

                    # 反撃ダメージ
                    if armor_result["counter_damage"] > 0:
                        self.enemy["hp"] -= armor_result["counter_damage"]
                        if self.enemy["hp"] <= 0:
                            # HPを保存
                            await db.update_player(interaction.user.id, hp=self.player["hp"])
                            text += "\n反撃で敵を倒した！"
                            await self.update_embed(text)
                            self.disable_all_items()
                            await self.message.edit(view=self)
                            if self.ctx.author.id in self.user_processing:
                                self.user_processing[self.ctx.author.id] = False
                            # ロックはasync with‌で自動解放される
                            return

                    # 反射ダメージ
                    if armor_result["reflect_damage"] > 0:
                        self.enemy["hp"] -= armor_result["reflect_damage"]
                        if self.enemy["hp"] <= 0:
                            # HPを保存
                            await db.update_player(interaction.user.id, hp=self.player["hp"])
                            text += "\n反射ダメージで敵を倒した！"
                            await self.update_embed(text)
                            self.disable_all_items()
                            await self.message.edit(view=self)
                            if self.ctx.author.id in self.user_processing:
                                self.user_processing[self.ctx.author.id] = False
                            # ロックはasync withで自動解放される
                            return

                    # HP回復
                    if armor_result["hp_regen"] > 0:
                        self.player["hp"] = min(self.player.get("max_hp", 50), self.player["hp"] + armor_result["hp_regen"])

                # 敗北チェック
                if self.player["hp"] <= 0:
                    if armor_result.get("revived", False):
                        self.player["hp"] = 1
                        text += "\n蘇生効果で生き残った！\n『死んだかと思った……どんなシステムなんだろう』"
                    else:
                        # 死亡処理（HPリセット、距離リセット、アップグレードポイント付与）
                        death_result = await handle_death_with_triggers(
                            self.ctx if hasattr(self, 'ctx') else interaction.channel,
                            interaction.user.id, 
                            self.user_processing if hasattr(self, 'user_processing') else {},
                            enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                            enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                        )
                        if death_result:
                            await self.update_embed(text + f"\n💀 あなたは倒れた…\n\n🔄 周回リスタート\n📍 アップグレードポイント: +{death_result['points']}pt")
                        else:
                            await self.update_embed(text + "\n💀 あなたは倒れた…")
                        self.disable_all_items()
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                        # ロックはasync withで自動解放される
                        return

                # HPを保存（戦闘継続時）
                await db.update_player(interaction.user.id, hp=self.player["hp"])
                await self.update_embed(text)
                # ボタンを再有効化
                for child in self.children:
                    child.disabled = False
                await self.message.edit(view=self)
            
            except Exception as e:
                print(f"[BattleView] fight error: {e}")
                import traceback
                traceback.print_exc()
                # エラー時もボタンを再有効化
                for child in self.children:
                    child.disabled = False
                try:
                    await self.message.edit(view=self)
                except:
                    pass

    # =====================================
    # 🛡️ 防御
    # =====================================
    @button(label="防御", style=discord.ButtonStyle.secondary, emoji="🛡️")
    async def defend(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # アトミックなロックチェック
        if self._battle_lock.locked():
            return await interaction.response.send_message("⚠️ 処理中です。少々お待ちください。", ephemeral=True)
        
        # 先にdeferしてタイムアウトを回避
        await interaction.response.defer()
        
        async with self._battle_lock:
            try:
                # ボタンを即座に無効化
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

                # ✅ プレイヤーデータを最新化
                fresh_player_data = await db.get_player(interaction.user.id)
                if fresh_player_data:
                    self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
                    
                    # ✅ 装備ボーナスを再計算してdefenseを更新
                    base_def = fresh_player_data.get("def", 2)
                    equipment_bonus = await game.calculate_equipment_bonus(interaction.user.id)
                    self.player["defense"] = base_def + equipment_bonus["defense_bonus"]
                    print(f"[DEBUG] defend - プレイヤーデータ最新化: HP={self.player['hp']}, DEF={base_def}+{equipment_bonus['defense_bonus']}={self.player['defense']}")

                reduction = random.randint(10, 50)
                enemy_dmg = max(0, int((self.enemy["atk"] + random.randint(-2, 2)) * (1 - reduction / 100)) - self.player["defense"])
                self.player["hp"] -= enemy_dmg
                self.player["hp"] = max(0, self.player["hp"])

                text = f"防御した！ ダメージを {reduction}% 軽減！\n敵の攻撃で {enemy_dmg} のダメージを受けた！"

                if self.player["hp"] <= 0:
                    # 死亡処理
                    death_result = await handle_death_with_triggers(
                        self.ctx if hasattr(self, 'ctx') else interaction.channel,
                        interaction.user.id, 
                        self.user_processing if hasattr(self, 'user_processing') else {},
                        enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                        enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                    )
                    if death_result:
                        await self.update_embed(text + f"\n💀 あなたは倒れた…\n\n🔄 周回リスタート\n📍 アップグレードポイント: +{death_result['points']}pt")
                    else:
                        await self.update_embed(text + "\n💀 あなたは倒れた…")
                    self.disable_all_items()
                    await self.message.edit(view=self)
                    if self.ctx.author.id in self.user_processing:
                        self.user_processing[self.ctx.author.id] = False
                    return

                # HPを保存
                await db.update_player(interaction.user.id, hp=self.player["hp"])
                await self.update_embed(text)
                # ボタンを再有効化
                for child in self.children:
                    child.disabled = False
                await self.message.edit(view=self)
            
            except Exception as e:
                print(f"[BattleView] defend error: {e}")
                import traceback
                traceback.print_exc()
                # エラー時もボタンを再有効化
                for child in self.children:
                    child.disabled = False
                try:
                    await self.message.edit(view=self)
                except:
                    pass

    # =====================================
    # 🏃‍♂️ 逃げる
    # =====================================
    @button(label="逃げる", style=discord.ButtonStyle.success, emoji="🏃‍♂️")
    async def run(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # アトミックなロックチェック
        if self._battle_lock.locked():
            return await interaction.response.send_message("⚠️ 処理中です。少々お待ちください。", ephemeral=True)
        
        # 先にdeferしてタイムアウトを回避
        await interaction.response.defer()
        
        async with self._battle_lock:
            try:
                # ボタンを即座に無効化
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

                # ✅ プレイヤーデータを最新化
                fresh_player_data = await db.get_player(interaction.user.id)
                if fresh_player_data:
                    self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
                    
                    # ✅ 装備ボーナスを再計算してdefenseを更新
                    base_def = fresh_player_data.get("def", 2)
                    equipment_bonus = await game.calculate_equipment_bonus(interaction.user.id)
                    self.player["defense"] = base_def + equipment_bonus["defense_bonus"]
                    print(f"[DEBUG] run - プレイヤーデータ最新化: HP={self.player['hp']}, DEF={base_def}+{equipment_bonus['defense_bonus']}={self.player['defense']}")

                # 逃走確率
                if random.randint(1, 100) <= 20:
                    # 逃走成功 - HPを保存
                    await db.update_player(interaction.user.id, hp=self.player["hp"])
                    text = "🏃‍♂️ うまく逃げ切れた！\n『戦っとけば良かったかな――。』"
                    self.disable_all_items()
                    await self.update_embed(text)
                    await self.message.edit(view=self)
                    if self.ctx.author.id in self.user_processing:
                        self.user_processing[self.ctx.author.id] = False
                else:
                    enemy_dmg = max(0, self.enemy["atk"] - self.player["defense"])
                    self.player["hp"] -= enemy_dmg
                    self.player["hp"] = max(0, self.player["hp"])
                    
                    # ★修正: 死亡判定を先に行い、条件分岐で適切なEmbed表示
                    if self.player["hp"] <= 0:
                        # 死亡処理
                        death_result = await handle_death_with_triggers(
                            self.ctx if hasattr(self, 'ctx') else interaction.channel,
                            interaction.user.id, 
                            self.user_processing if hasattr(self, 'user_processing') else {},
                            enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                            enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                        )
                        if death_result:
                            text = f"逃げられなかった！ 敵の攻撃で {enemy_dmg} のダメージ！\n💀 あなたは倒れた…\n\n🔄 周回リスタート\n📍 アップグレードポイント: +{death_result['points']}pt"
                        else:
                            text = f"逃げられなかった！ 敵の攻撃で {enemy_dmg} のダメージ！\n💀 あなたは倒れた…"
                        self.disable_all_items()
                        await self.update_embed(text)
                        await self.message.edit(view=self)
                        if self.ctx.author.id in self.user_processing:
                            self.user_processing[self.ctx.author.id] = False
                    else:
                        # HPを保存（生存時）
                        await db.update_player(interaction.user.id, hp=self.player["hp"])
                        text = f"逃げられなかった！ 敵の攻撃で {enemy_dmg} のダメージ！"
                        await self.update_embed(text)
                        # ボタンを再有効化
                        for child in self.children:
                            child.disabled = False
                        await self.message.edit(view=self)
            
            except Exception as e:
                print(f"[BattleView] run error: {e}")
                import traceback
                traceback.print_exc()
                # エラー時もボタンを再有効化
                for child in self.children:
                    child.disabled = False
                try:
                    await self.message.edit(view=self)
                except:
                    pass

    # =====================================
    # 💊 アイテム使用
    # =====================================
    @button(label="アイテム使用", style=discord.ButtonStyle.primary, emoji="💊")
    async def use_item(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

        # ✅ 最新のプレイヤーデータを取得
        self.player = await db.get_player(self.ctx.author.id)
        if not self.player:
            return await interaction.response.send_message("プレイヤーデータが見つかりません", ephemeral=True)

        items = self.player.get("inventory", [])
        if not items:
            return await interaction.response.send_message("使えるアイテムがありません！", ephemeral=True)

        # HP回復薬とMP回復薬を分類
        hp_potions = []
        mp_potions = []
        
        for item in items:
            item_info = game.get_item_info(item)
            if item_info and item_info.get('type') == 'potion':
                effect = item_info.get('effect', '')
                if 'MP+' in effect or 'MP全回復' in effect:
                    mp_potions.append((item, item_info))
                else:
                    hp_potions.append((item, item_info))

        if not hp_potions and not mp_potions:
            return await interaction.response.send_message("戦闘で使えるアイテムがありません！", ephemeral=True)

        # （以下は元のコードと同じ）

        # Viewを作成
        item_view = discord.ui.View(timeout=60)
        
        # HP回復薬のプルダウン（最大15個）
        if hp_potions:
            hp_options = []
            for idx, (item, info) in enumerate(hp_potions[:15]):
                effect = info.get('effect', 'HP回復')
                hp_options.append(discord.SelectOption(
                    label=item,
                    description=effect,
                    value=f"hp_{idx}_{item}",
                    emoji="💚"
                ))
            
            hp_select = discord.ui.Select(
                placeholder="💚 HP回復薬",
                options=hp_options,
                custom_id="hp_potion_select"
            )
            hp_select.callback = self.make_item_callback(hp_potions)
            item_view.add_item(hp_select)
        
        # MP回復薬のプルダウン（最大15個）
        if mp_potions:
            mp_options = []
            for idx, (item, info) in enumerate(mp_potions[:15]):
                effect = info.get('effect', 'MP回復')
                mp_options.append(discord.SelectOption(
                    label=item,
                    description=effect,
                    value=f"mp_{idx}_{item}",
                    emoji="💙"
                ))
            
            mp_select = discord.ui.Select(
                placeholder="💙 MP回復薬",
                options=mp_options,
                custom_id="mp_potion_select"
            )
            mp_select.callback = self.make_item_callback(mp_potions)
            item_view.add_item(mp_select)

        await interaction.response.send_message("アイテムを選択してください:", view=item_view, ephemeral=True)
    
    def make_item_callback(self, potion_list):
        """アイテム選択のコールバック関数を生成"""

        async def item_select_callback(select_interaction: discord.Interaction):
            if select_interaction.user.id != self.ctx.author.id:
                return await select_interaction.response.send_message("これはあなたの戦闘ではありません！", ephemeral=True)

            # ✅ プレイヤーデータを再取得（アイテム所持確認のため）
            fresh_player_data = await db.get_player(select_interaction.user.id)
            if not fresh_player_data:
                return await select_interaction.response.send_message("プレイヤーデータが見つかりません。", ephemeral=True)
            
            self.player["hp"] = fresh_player_data.get("hp", self.player["hp"])
            self.player["mp"] = fresh_player_data.get("mp", self.player.get("mp", 20))
            self.player["max_hp"] = fresh_player_data.get("max_hp", self.player.get("max_hp", 50))
            self.player["max_mp"] = fresh_player_data.get("max_mp", self.player.get("max_mp", 20))
            self.player["inventory"] = fresh_player_data.get("inventory", [])
            print(f"[DEBUG] item_select_callback - プレイヤーデータ再取得: HP={self.player['hp']}, インベントリ={len(self.player['inventory'])}個")

            selected_value = select_interaction.data['values'][0]
            parts = selected_value.split("_", 2)  # 例: "hp_0_小さい回復薬"
            potion_type = parts[0]
            idx = int(parts[1])
            item_name = parts[2]

            # ✅ アイテム所持確認
            if item_name not in self.player["inventory"]:
                print(f"[DEBUG] item_select_callback - アイテム未所持: {item_name}")
                return await select_interaction.response.send_message(f"⚠️ {item_name} を所持していません。", ephemeral=True)

            item_info = game.get_item_info(item_name)
            if not item_info:
                return await select_interaction.response.send_message("アイテム情報が見つかりません。", ephemeral=True)

            text = ""
            
            # MP回復薬の処理
            if potion_type == "mp":
                current_mp = self.player.get('mp', 20)
                max_mp = self.player.get('max_mp', 20)
                effect = item_info.get('effect', '')
                
                if 'MP+15' in effect:
                    mp_heal = 15
                elif 'MP+40' in effect:
                    mp_heal = 40
                elif 'MP+100' in effect:
                    mp_heal = 100
                else:
                    mp_heal = 30
                
                new_mp = min(max_mp, current_mp + mp_heal)
                actual_mp_heal = new_mp - current_mp
                self.player['mp'] = new_mp
                
                await db.remove_item_from_inventory(self.ctx.author.id, item_name)
                await db.update_player(self.ctx.author.id, mp=new_mp)
                
                text = f"✨ **{item_name}** を使用した！\nMP +{actual_mp_heal} 回復！"
            
            # HP回復薬の処理
            else:
                current_hp = self.player.get('hp', 50)
                max_hp = self.player.get('max_hp', 50)
                effect = item_info.get('effect', '')

                if 'HP+30' in effect:
                    heal = 30
                elif 'HP+80' in effect:
                    heal = 80
                elif 'HP200' in effect:
                    heal = 200
                else:
                    heal = 30

                new_hp = min(max_hp, current_hp + heal)
                actual_heal = new_hp - current_hp
                self.player['hp'] = new_hp

                await db.remove_item_from_inventory(self.ctx.author.id, item_name)
                await db.update_player(self.ctx.author.id, hp=new_hp)

                text = f"✨ **{item_name}** を使用した！\nHP +{actual_heal} 回復！"
                
            # 敵の反撃
            enemy_dmg = max(0, self.enemy["atk"] + random.randint(-3, 3) - self.player["defense"])
            self.player["hp"] -= enemy_dmg
            self.player["hp"] = max(0, self.player["hp"])
            text += f"\n敵の攻撃！ {enemy_dmg} のダメージを受けた！"

            if self.player["hp"] <= 0:
                death_result = await handle_death_with_triggers(
                    self.ctx, 
                    self.ctx.author.id, 
                    self.user_processing if hasattr(self, 'user_processing') else {},
                    enemy_name=getattr(self, 'enemy', {}).get('name') or getattr(self, 'boss', {}).get('name') or '不明',
                    enemy_type='boss' if hasattr(self, 'boss') else 'normal'
                )
                if death_result:
                    text += f"\n\n💀 あなたは倒れた…\n\n⭐ {death_result['points']}アップグレードポイントを獲得！\n（死亡回数: {death_result['death_count']}回）"
                else:
                    text += "\n💀 あなたは倒れた…"
                self.disable_all_items()
                await self.update_embed(text)
                await self.message.edit(view=self)
                if self.ctx.author.id in self.user_processing:
                    self.user_processing[self.ctx.author.id] = False
                await select_interaction.response.defer()
                return

            # HPを保存（生存時）
            await db.update_player(self.ctx.author.id, hp=self.player["hp"])
            await self.update_embed(text)
            await select_interaction.response.defer()
        
        return item_select_callback

    # =====================================
    # 終了時無効化
    # =====================================
    def disable_all_items(self):
        for item in self.children:
            item.disabled = True

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.ctx.author.id in self.user_processing:
            self.user_processing[self.ctx.author.id] = False


#ステータスEmbed
def status_embed(player):
    embed = discord.Embed(title="📊 ステータス", color=discord.Color.blue())
    embed.add_field(name="名前", value=player.get("name", "未設定"))
    embed.add_field(name="HP", value=player.get("hp", 50))
    embed.add_field(name="攻撃力", value=player.get("attack", 5))
    embed.add_field(name="防御力", value=player.get("defense", 2))
    embed.add_field(name="所持金", value=f'{player.get("gold", 0)}G')
    return embed

from collections import Counter

class InventorySelectView(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=60)
        self.player = player
        self.user_id = player.get("user_id") if isinstance(player, dict) else None
        inventory = player.get("inventory", [])

        if not inventory:
            options = [discord.SelectOption(label="アイテムなし", description="インベントリは空です", value="none")]
            select = discord.ui.Select(
                placeholder="アイテムを選んで詳細を表示",
                options=options,
                custom_id="inventory_select"
            )
            select.callback = self.select_callback
            self.add_item(select)
        else:
            # アイテムをカウント（集約）
            item_counts = Counter(inventory)
            
            # アイテムを種類別に分類
            potions = []
            weapons = []
            armors = []
            materials = []
            
            for item_name, count in item_counts.items():
                item_info = game.get_item_info(item_name)
                if item_info:
                    if item_info['type'] == 'potion':
                        potions.append((item_name, count, item_info))
                    elif item_info['type'] == 'weapon':
                        weapons.append((item_name, count, item_info))
                    elif item_info['type'] == 'armor':
                        armors.append((item_name, count, item_info))
                    else:
                        materials.append((item_name, count, item_info))
            
            # ポーションのプルダウン（最大25個）
            if potions:
                potion_options = []
                for i, (item_name, count, info) in enumerate(potions[:25]):
                    desc = info.get('description', 'ポーション')[:80]
                    label = f"{item_name} ×{count}" if count > 1 else item_name
                    potion_options.append(discord.SelectOption(
                        label=label,
                        description=desc,
                        value=f"potion_{i}_{item_name}",  # 重複回避
                        emoji="🧪"
                    ))
                
                potion_select = discord.ui.Select(
                    placeholder="🧪 ポーション",
                    options=potion_options,
                    custom_id="potion_select"
                )
                potion_select.callback = self.select_callback
                self.add_item(potion_select)
            
            # 武器のプルダウン（最大25個）
            if weapons:
                weapon_options = []
                for i, (item_name, count, info) in enumerate(weapons[:25]):
                    desc = f"攻撃力:{info.get('attack', 0)} | 所持数:{count}"
                    label = f"{item_name} ×{count}" if count > 1 else item_name
                    weapon_options.append(discord.SelectOption(
                        label=label,
                        description=desc[:100],
                        value=f"weapon_{i}_{item_name}",
                        emoji="⚔️"
                    ))
                
                weapon_select = discord.ui.Select(
                    placeholder="⚔️ 武器",
                    options=weapon_options,
                    custom_id="weapon_select"
                )
                weapon_select.callback = self.select_callback
                self.add_item(weapon_select)
            
            # 防具のプルダウン（最大25個）
            if armors:
                armor_options = []
                for i, (item_name, count, info) in enumerate(armors[:25]):
                    desc = f"防御力:{info.get('defense', 0)} | 所持数:{count}"
                    label = f"{item_name} ×{count}" if count > 1 else item_name
                    armor_options.append(discord.SelectOption(
                        label=label,
                        description=desc[:100],
                        value=f"armor_{i}_{item_name}",
                        emoji="🛡️"
                    ))
                
                armor_select = discord.ui.Select(
                    placeholder="🛡️ 防具",
                    options=armor_options,
                    custom_id="armor_select"
                )
                armor_select.callback = self.select_callback
                self.add_item(armor_select)
            
            # 素材のプルダウン（最大25個）
            if materials:
                material_options = []
                for i, (item_name, count, info) in enumerate(materials[:25]):
                    desc = f"{info.get('description', '素材')[:80]} | 所持数:{count}"
                    label = f"{item_name} ×{count}" if count > 1 else item_name
                    material_options.append(discord.SelectOption(
                        label=label,
                        description=desc[:100],
                        value=f"material_{i}_{item_name}",
                        emoji="📦"
                    ))
                
                material_select = discord.ui.Select(
                    placeholder="📦 素材",
                    options=material_options,
                    custom_id="material_select"
                )
                material_select.callback = self.select_callback
                self.add_item(material_select)

    async def select_callback(self, interaction: discord.Interaction):
        if self.player.get("user_id") and interaction.user.id != int(self.player.get("user_id")):
            return await interaction.response.send_message("これはあなたのインベントリではありません！", ephemeral=True)

        selected_value = interaction.data['values'][0]
        if selected_value == "none":
            return await interaction.response.send_message("アイテムがありません。", ephemeral=True)

        # valueから型、インデックス、アイテム名を分離
        parts = selected_value.split("_", 2)
        if len(parts) < 3:
            return await interaction.response.send_message("不正な選択です。", ephemeral=True)
        
        item_type, idx, item_name = parts
        item_info = game.get_item_info(item_name)

        if not item_info:
            return await interaction.response.send_message("アイテム情報が見つかりません。", ephemeral=True)

        # 所持数を取得
        inventory = self.player.get("inventory", [])
        item_count = inventory.count(item_name)

        # アイテムタイプ別処理
        if item_info['type'] == 'potion':
            # 回復薬使用
            player = await get_player(interaction.user.id)
            if not player:
                return await interaction.response.send_message("プレイヤーデータが見つかりません。", ephemeral=True)

            effect = item_info.get('effect', '')
            
            # MP回復薬の処理
            if 'MP+' in effect or 'MP全回復' in effect:
                current_mp = player.get('mp', 20)
                max_mp = player.get('max_mp', 20)
                
                if current_mp >= max_mp:
                    return await interaction.response.send_message("MPは既に最大です！", ephemeral=True)
                
                if 'MP+30' in effect:
                    mp_heal = 30
                elif 'MP+80' in effect:
                    mp_heal = 80
                elif 'MP+200' in effect:
                    mp_heal = 200
                elif 'MP全回復' in effect:
                    mp_heal = max_mp
                else:
                    mp_heal = 30
                
                new_mp = min(max_mp, current_mp + mp_heal)
                actual_mp_heal = new_mp - current_mp
                
                await update_player(interaction.user.id, mp=new_mp)
                await db.remove_item_from_inventory(interaction.user.id, item_name)
                
                remaining = item_count - 1
                await interaction.response.send_message(
                    f"✨ **{item_name}** を使用した！\nMP +{actual_mp_heal} 回復！（{current_mp} → {new_mp}）\n残り: {remaining}個",
                    ephemeral=True
                )
            # HP回復薬の処理
            else:
                current_hp = player.get('hp', 50)
                max_hp = player.get('max_hp', 50)
                
                if current_hp >= max_hp:
                    return await interaction.response.send_message("HPは既に最大です！", ephemeral=True)

                if 'HP+30' in effect:
                    heal = 30
                elif 'HP+80' in effect:
                    heal = 80
                elif 'HP+200' in effect:
                    heal = 200
                elif 'HP全回復' in effect:
                    heal = max_hp
                else:
                    heal = 30

                new_hp = min(max_hp, current_hp + heal)
                actual_heal = new_hp - current_hp

                await update_player(interaction.user.id, hp=new_hp)
                await db.remove_item_from_inventory(interaction.user.id, item_name)

                remaining = item_count - 1
                await interaction.response.send_message(
                    f"✨ **{item_name}** を使用した！\nHP +{actual_heal} 回復！（{current_hp} → {new_hp}）\n残り: {remaining}個",
                    ephemeral=True
                )

        elif item_info['type'] == 'weapon':
            attack = item_info.get('attack', 0)
            ability = item_info.get('ability', 'なし')
            description = item_info.get('description', '')
            await interaction.response.send_message(
                f"⚔️ **{item_name}** (所持数: {item_count})\n攻撃力: {attack}\n能力: {ability}\n\n{description}\n\n装備するには `!status` コマンドから装備変更してください。",
                ephemeral=True
            )

        elif item_info['type'] == 'armor':
            defense = item_info.get('defense', 0)
            ability = item_info.get('ability', 'なし')
            description = item_info.get('description', '')
            await interaction.response.send_message(
                f"🛡️ **{item_name}** (所持数: {item_count})\n防御力: {defense}\n能力: {ability}\n\n{description}\n\n装備するには `!status` コマンドから装備変更してください。",
                ephemeral=True
            )

        else:
            await interaction.response.send_message(
                f"📦 {item_name} (所持数: {item_count})\n{item_info.get('description', '')}",
                ephemeral=True
            )


from collections import Counter

class EquipmentSelectView(discord.ui.View):
    """装備変更用View"""
    def __init__(self, player):
        super().__init__(timeout=60)
        self.player = player
        self.user_id = player.get("user_id") if isinstance(player, dict) else None
        inventory = player.get("inventory", [])

        # アイテムをカウント（集約）
        item_counts = Counter(inventory)

        # 武器リストと防具リスト
        weapons = []
        armors = []
        
        for item_name, count in item_counts.items():
            item_info = game.get_item_info(item_name)
            if item_info:
                if item_info['type'] == 'weapon':
                    weapons.append((item_name, count, item_info))
                elif item_info['type'] == 'armor':
                    armors.append((item_name, count, item_info))

        # 武器選択プルダウン1（1〜25個目）
        if weapons:
            weapon_options_1 = []
            for i, (weapon_name, count, item_info) in enumerate(weapons[:25]):
                desc = f"攻撃力: {item_info.get('attack', 0)} | 所持数: {count}"
                label = f"{weapon_name} ×{count}" if count > 1 else weapon_name
                weapon_options_1.append(discord.SelectOption(
                    label=label,
                    description=desc[:100],
                    value=f"weapon_{i}_{weapon_name}",
                    emoji="⚔️"
                ))
            
            weapon_select_1 = discord.ui.Select(
                placeholder="⚔️ 武器を選択 (1/2)",
                options=weapon_options_1,
                custom_id="weapon_select_1"
            )
            weapon_select_1.callback = self.select_callback
            self.add_item(weapon_select_1)

        # 武器選択プルダウン2（26〜50個目）
        if len(weapons) > 25:
            weapon_options_2 = []
            for i, (weapon_name, count, item_info) in enumerate(weapons[25:50], start=25):
                desc = f"攻撃力: {item_info.get('attack', 0)} | 所持数: {count}"
                label = f"{weapon_name} ×{count}" if count > 1 else weapon_name
                weapon_options_2.append(discord.SelectOption(
                    label=label,
                    description=desc[:100],
                    value=f"weapon_{i}_{weapon_name}",
                    emoji="⚔️"
                ))
            
            weapon_select_2 = discord.ui.Select(
                placeholder="⚔️ 武器を選択 (2/2)",
                options=weapon_options_2,
                custom_id="weapon_select_2"
            )
            weapon_select_2.callback = self.select_callback
            self.add_item(weapon_select_2)

        # 防具選択プルダウン1（1〜25個目）
        if armors:
            armor_options_1 = []
            for i, (armor_name, count, item_info) in enumerate(armors[:25]):
                desc = f"防御力: {item_info.get('defense', 0)} | 所持数: {count}"
                label = f"{armor_name} ×{count}" if count > 1 else armor_name
                armor_options_1.append(discord.SelectOption(
                    label=label,
                    description=desc[:100],
                    value=f"armor_{i}_{armor_name}",
                    emoji="🛡️"
                ))
            
            armor_select_1 = discord.ui.Select(
                placeholder="🛡️ 防具を選択 (1/2)",
                options=armor_options_1,
                custom_id="armor_select_1"
            )
            armor_select_1.callback = self.select_callback
            self.add_item(armor_select_1)

        # 防具選択プルダウン2（26〜50個目）
        if len(armors) > 25:
            armor_options_2 = []
            for i, (armor_name, count, item_info) in enumerate(armors[25:50], start=25):
                desc = f"防御力: {item_info.get('defense', 0)} | 所持数: {count}"
                label = f"{armor_name} ×{count}" if count > 1 else armor_name
                armor_options_2.append(discord.SelectOption(
                    label=label,
                    description=desc[:100],
                    value=f"armor_{i}_{armor_name}",
                    emoji="🛡️"
                ))
            
            armor_select_2 = discord.ui.Select(
                placeholder="🛡️ 防具を選択 (2/2)",
                options=armor_options_2,
                custom_id="armor_select_2"
            )
            armor_select_2.callback = self.select_callback
            self.add_item(armor_select_2)

    async def select_callback(self, interaction: discord.Interaction):
        if self.player.get("user_id") and interaction.user.id != int(self.player.get("user_id")):
            return await interaction.response.send_message("これはあなたの装備ではありません！", ephemeral=True)

        selected_value = interaction.data['values'][0]
        parts = selected_value.split("_", 2)
        
        if len(parts) < 3:
            return await interaction.response.send_message("⚠️ 不正な選択です。", ephemeral=True)
        
        equip_type = parts[0]
        item_name = parts[2]

        if equip_type == "weapon":
            await db.equip_weapon(interaction.user.id, item_name)
            await interaction.response.send_message(f"⚔️ **{item_name}** を武器として装備した！", ephemeral=True)
        elif equip_type == "armor":
            await db.equip_armor(interaction.user.id, item_name)
            await interaction.response.send_message(f"🛡️ **{item_name}** を防具として装備した！", ephemeral=True)


class BlacksmithView(discord.ui.View):
    """鍛冶屋View - 素材を使って装備を合成"""
    def __init__(self, user_id: int, user_processing: dict, materials: dict):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.user_processing = user_processing
        self.materials = materials

        self.available_recipes = []
        for recipe_name, recipe in game.CRAFTING_RECIPES.items():
            can_craft = True
            for material, required_count in recipe["materials"].items():
                if self.materials.get(material, 0) < required_count:
                    can_craft = False
                    break
            if can_craft:
                self.available_recipes.append(recipe_name)

        if self.available_recipes:
            options = []
            for recipe_name in self.available_recipes[:25]:
                recipe = game.CRAFTING_RECIPES[recipe_name]
                materials_str = ", ".join([f"{mat}x{count}" for mat, count in recipe["materials"].items()])
                desc = f"{materials_str}"
                options.append(discord.SelectOption(
                    label=recipe_name,
                    description=desc[:100],
                    value=recipe_name
                ))

            select = discord.ui.Select(
                placeholder="合成したいアイテムを選択",
                options=options
            )
            select.callback = self.craft_callback
            self.add_item(select)
        
        # 「戻る」ボタンを常に追加
        close_button = discord.ui.Button(
            label="戻る",
            style=discord.ButtonStyle.secondary,
            emoji="🚪"
        )
        close_button.callback = self.close_callback
        self.add_item(close_button)

    def get_embed(self):
        embed = discord.Embed(
            title="🔨 鍛冶屋",
            description="「素材を使って強力な装備を作ることができるぞ。俺ちゃん天才！」\n\n所持素材:",
            color=discord.Color.blue()
        )

        if self.materials:
            for material, count in self.materials.items():
                embed.add_field(name=material, value=f"x{count}", inline=True)
        else:
            embed.add_field(name="素材なし", value="素材を集めてきてください", inline=False)

        if self.available_recipes:
            embed.add_field(name="\n合成可能なレシピ", value="下のメニューから選択してください", inline=False)
        else:
            embed.add_field(
                name="\n⚠️ 合成可能なレシピなし", 
                value="現在の素材では合成できるアイテムがありません。\nもっと素材を集めてから来てください。\n\n「戻る」ボタンで特殊イベント選択に戻れます。", 
                inline=False
            )

        return embed

    async def craft_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたの鍛冶屋ではありません！", ephemeral=True)

        recipe_name = interaction.data['values'][0]
        recipe = game.CRAFTING_RECIPES.get(recipe_name)
        
        if not recipe:
            return await interaction.response.send_message("⚠️ レシピ情報が見つかりません。", ephemeral=True)

        player = await get_player(interaction.user.id)
        if not player:
            return await interaction.response.send_message("⚠️ プレイヤーデータが見つかりません。", ephemeral=True)

        # 素材を消費
        for material, required_count in recipe["materials"].items():
            for _ in range(required_count):
                await db.remove_item_from_inventory(interaction.user.id, material)

        # アイテムを追加
        await db.add_item_to_inventory(interaction.user.id, recipe_name)

        # アイテムデータベースに登録（存在しない場合）
        if recipe_name not in game.ITEMS_DATABASE:
            game.ITEMS_DATABASE[recipe_name] = {
                "type": recipe["result_type"],
                "attack": recipe.get("attack", 0),
                "defense": recipe.get("defense", 0),
                "ability": recipe["ability"],
                "description": recipe["description"]
            }

        materials_used = ", ".join([f"{mat}x{count}" for mat, count in recipe["materials"].items()])

        embed = discord.Embed(
            title="✨ 合成成功！",
            description=f"**{recipe_name}** を作成した！\n『ほらよ。ちゃんと作ってやったぜ』\n\n使用素材: {materials_used}",
            color=discord.Color.gold()
        )

        if recipe["result_type"] == "weapon":
            embed.add_field(name="攻撃力", value=str(recipe.get("attack", 0)), inline=True)
        elif recipe["result_type"] == "armor":
            embed.add_field(name="防御力", value=str(recipe.get("defense", 0)), inline=True)

        embed.add_field(name="能力", value=recipe["ability"], inline=False)
        embed.add_field(name="説明", value=recipe["description"], inline=False)

        await interaction.response.edit_message(embed=embed, view=None)

        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    async def close_callback(self, interaction: discord.Interaction):
        """戻るボタン"""
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたの鍛冶屋ではありません！", ephemeral=True)

        embed = discord.Embed(
            title="🏛️ 特殊イベント",
            description="鍛冶屋を後にした。\n\n他の選択肢を選んでください。",
            color=discord.Color.blue()
        )

        await interaction.response.edit_message(embed=embed, view=None)

        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    async def on_timeout(self):
        """タイムアウト時にuser_processingをクリア"""
        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

class MaterialMerchantView(discord.ui.View):
    """素材商人View - 素材を売却"""
    def __init__(self, user_id: int, user_processing: dict, materials: dict):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.user_processing = user_processing
        self.materials = materials

        options = []
        for material, count in materials.items():
            price = game.MATERIAL_PRICES.get(material, 10)
            total_price = price * count
            options.append(discord.SelectOption(
                label=f"{material} (x{count})",
                description=f"単価: {price}G × {count}個 = {total_price}G",
                value=material
            ))

        select = discord.ui.Select(
            placeholder="売却する素材を選択",
            options=options
        )
        select.callback = self.sell_callback
        self.add_item(select)

        sell_all_button = discord.ui.Button(label="全て売却", style=discord.ButtonStyle.success, emoji="💰")
        sell_all_button.callback = self.sell_all_callback
        self.add_item(sell_all_button)

    def get_embed(self):
        embed = discord.Embed(
            title="💰 素材商人",
            description="「素材を買い取るぞ。良い値で引き取ろう――」\n\n所持素材と買取価格:",
            color=discord.Color.green()
        )

        total_value = 0
        for material, count in self.materials.items():
            price = game.MATERIAL_PRICES.get(material, 10)
            total_price = price * count
            total_value += total_price
            embed.add_field(
                name=f"{material} (x{count})",
                value=f"{price}G × {count} = {total_price}G",
                inline=False
            )

        embed.add_field(name="\n💎 全素材の合計価値", value=f"**{total_value}G**", inline=False)
        embed.set_footer(text="下のメニューから売却する素材を選択してください")

        return embed

    async def sell_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたの商人ではありません！", ephemeral=True)

        material = interaction.data['values'][0]
        count = self.materials[material]
        price = game.MATERIAL_PRICES.get(material, 10)
        total_price = price * count

        for _ in range(count):
            await db.remove_item_from_inventory(interaction.user.id, material)

        await db.add_gold(interaction.user.id, total_price)

        embed = discord.Embed(
            title="✅ 売却完了！",
            description=f"**{material}** を {count}個売却した！\n\n💰 {total_price}ゴールドを獲得！",
            color=discord.Color.gold()
        )

        await interaction.response.edit_message(embed=embed, view=None)

        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

    async def sell_all_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたの商人ではありません！", ephemeral=True)

        total_gold = 0
        sold_items = []

        for material, count in self.materials.items():
            price = game.MATERIAL_PRICES.get(material, 10)
            total_price = price * count
            total_gold += total_price

            for _ in range(count):
                await db.remove_item_from_inventory(interaction.user.id, material)

            sold_items.append(f"{material} x{count} = {total_price}G")

        await db.add_gold(interaction.user.id, total_gold)

        sold_text = "\n".join(sold_items)

        embed = discord.Embed(
            title="✅ 一括売却完了！",
            description=f"全ての素材を売却した！\n\n{sold_text}\n\n💰 合計 {total_gold}ゴールドを獲得！",
            color=discord.Color.gold()
        )

        await interaction.response.edit_message(embed=embed, view=None)

        if self.user_id in self.user_processing:
            self.user_processing[self.user_id] = False

# 死亡処理 + トリガーチェック 共通ヘルパー
async def handle_death_with_triggers(ctx, user_id, user_processing, enemy_name=None, enemy_type="normal"):
    """
    死亡処理 + ストーリー/称号トリガーを統合
    全ての戦闘クラスから呼び出される共通処理
    """
    # 死亡処理
    death_result = await db.handle_player_death(
        user_id, 
        killed_by_enemy_name=enemy_name, 
        enemy_type=enemy_type
    )

    # トリガーチェック
    trigger_result = await death_system.check_death_triggers(user_id)

    # ストーリーイベント発動
    if trigger_result["type"] == "story":
        from story import StoryView
        story_view = StoryView(user_id, trigger_result["story_id"], user_processing)
        await story_view.send_story(ctx)

    # 称号獲得
    elif trigger_result["type"] == "title":
        title_data = trigger_result["data"]
        embed = discord.Embed(
            title=f"{get_title_rarity_emoji(trigger_result['title_id'])} 称号獲得！",
            description=f"**{title_data['name']}** を獲得しました！\n\n{title_data['description']}",
            color=get_title_rarity_color(trigger_result['title_id'])
        )
        await ctx.send(embed=embed)

    return death_result
