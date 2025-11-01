"""
デバッグコマンド - テスト用コマンド集
このファイルを削除しても、main.pyは正常に動作します。
"""

import discord
from discord.ext import commands
import db
from story import StoryView, STORY_DATA

def setup(bot: commands.Bot, user_processing: dict):
    """デバッグコマンドをbotに登録"""

    @bot.command(name="debug")
    async def debug_info(ctx: commands.Context):
        """プレイヤーの現在の状態を表示"""
        user = ctx.author
        player = db.get_player(user.id)

        if not player:
            await ctx.send("❌ プレイヤーデータが見つかりません。`!start` でゲームを開始してください。")
            return

        # デバッグ情報を整形
        embed = discord.Embed(
            title=f"🔍 デバッグ情報 - {player.get('name', '名前未設定')}",
            color=discord.Color.blue()
        )

        # 基本情報
        embed.add_field(
            name="💪 ステータス",
            value=f"HP: {player.get('hp', 0)}/{player.get('max_hp', 100)}\n"
                  f"MP: {player.get('mp', 0)}/{player.get('max_mp', 100)}\n"
                  f"ATK: {player.get('atk', 10)}\n"
                  f"DEF: {player.get('def', 5)}",
            inline=True
        )

        # 進行状況
        embed.add_field(
            name="📍 進行状況",
            value=f"距離: {player.get('distance', 0)}m\n"
                  f"階層: {player.get('current_floor', 0)}\n"
                  f"ステージ: {player.get('current_stage', 0)}",
            inline=True
        )

        # 死亡情報
        death_count = player.get('death_count', 0)

        embed.add_field(
            name="💀 死亡情報",
            value=f"死亡回数: {death_count}",
            inline=True
        )

        # アップグレードポイント
        upgrade_points = player.get('upgrade_points', 0)
        embed.add_field(
            name="⭐ ポイント",
            value=f"アップグレードポイント: {upgrade_points}",
            inline=True
        )

        # 装備
        weapon = player.get('equipped_weapon') or "なし"
        armor = player.get('equipped_armor') or "なし"
        embed.add_field(
            name="⚔️ 装備",
            value=f"武器: {weapon}\n防具: {armor}",
            inline=True
        )

        # インベントリ
        inventory = player.get('inventory', [])
        inventory_text = ", ".join(inventory[:5]) if inventory else "なし"
        if len(inventory) > 5:
            inventory_text += f" ...他{len(inventory)-5}個"

        embed.add_field(
            name="🎒 インベントリ",
            value=inventory_text,
            inline=True
        )

        # ストーリーフラグ
        story_flags = player.get('story_flags', {})
        story_count = len([k for k, v in story_flags.items() if v])

        embed.add_field(
            name="📖 ストーリー進行",
            value=f"閲覧済み: {story_count}個\n"
                  f"intro_2表示済み: {'✅' if story_flags.get('intro_2') else '❌'}",
            inline=True
        )

        # ボス撃破情報
        boss_flags = player.get('boss_defeated_flags', {})
        defeated_bosses = [k for k, v in boss_flags.items() if v]
        boss_text = ", ".join(defeated_bosses) if defeated_bosses else "なし"

        embed.add_field(
            name="👹 撃破済みボス",
            value=boss_text,
            inline=False
        )

        embed.set_footer(text=f"User ID: {user.id}")

        await ctx.send(embed=embed)

    @bot.command(name="force_story")
    async def force_story(ctx: commands.Context, story_id: str = None):
        """指定したストーリーを強制表示（テスト用）"""
        user = ctx.author

        if not story_id:
            # 利用可能なストーリーIDを表示
            available_stories = list(STORY_DATA.keys())
            story_list = "\n".join([f"- `{sid}`" for sid in available_stories[:20]])
            if len(available_stories) > 20:
                story_list += f"\n...他{len(available_stories)-20}個"

            embed = discord.Embed(
                title="📚 利用可能なストーリーID",
                description=f"使い方: `!force_story <story_id>`\n\n{story_list}",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            return

        # ストーリーが存在するかチェック
        if story_id not in STORY_DATA:
            await ctx.send(f"❌ ストーリーID `{story_id}` は存在しません。`!force_story` で一覧を確認してください。")
            return

        player = db.get_player(user.id)
        if not player:
            await ctx.send("❌ プレイヤーデータが見つかりません。`!start` でゲームを開始してください。")
            return

        # ストーリー表示
        embed = discord.Embed(
            title="🧪 テスト: ストーリー強制表示",
            description=f"ストーリーID: `{story_id}` を表示します...",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

        view = StoryView(user.id, story_id, user_processing)
        await view.send_story(ctx)

    @bot.command(name="set_death_count")
    async def set_death_count(ctx: commands.Context, count: int):
        """死亡回数を設定（テスト用）"""
        if count < 0:
            await ctx.send("❌ 死亡回数は0以上の数値を指定してください。")
            return

        player = db.get_player(ctx.author.id)
        if not player:
            await ctx.send("❌ プレイヤーデータが見つかりません。`!start` でゲームを開始してください。")
            return

        db.update_player(ctx.author.id, death_count=count)

        embed = discord.Embed(
            title="✅ 死亡回数を設定しました",
            description=f"死亡回数: {count}\n\nこれで `intro_2` のテストができます（death_count=1で表示）",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @bot.command(name="clear_story_flags")
    async def clear_story_flags(ctx: commands.Context):
        """ストーリーフラグをクリア（テスト用）"""
        player = db.get_player(ctx.author.id)
        if not player:
            await ctx.send("❌ プレイヤーデータが見つかりません。`!start` でゲームを開始してください。")
            return

        db.clear_story_flags(ctx.author.id)

        embed = discord.Embed(
            title="✅ ストーリーフラグをクリアしました",
            description="すべてのストーリーを再度見ることができます。",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    print(f"📝 デバッグコマンド登録完了: !debug, !force_story, !set_death_count, !clear_story_flags")
