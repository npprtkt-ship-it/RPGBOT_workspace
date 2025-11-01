"""
デバッグコマンドシステム
- 管理者専用コマンド（User ID制限付き）
- ユーザー向けロールバックシステム
- エラーログ管理
"""

import discord
from discord.ext import commands
import db
import logging
from datetime import datetime, timedelta
from typing import Optional
import json
import asyncio
import copy

logger = logging.getLogger("rpgbot")

# ==============================
# 管理者ID定義
# ==============================
ADMIN_IDS = [1301416493401243694, 785051117323026463]

# ==============================
# エラーログストレージ
# ==============================
class ErrorLogManager:
    """エラーログを管理するクラス"""
    def __init__(self, max_logs=100):
        self.logs = []
        self.max_logs = max_logs
    
    def add_error(self, error_type: str, message: str, user_id: Optional[int] = None, context: Optional[str] = None):
        """エラーログを追加"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": message,
            "user_id": user_id,
            "context": context
        }
        self.logs.append(log_entry)
        
        # 最大数を超えたら古いものから削除
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
        
        logger.error(f"[ErrorLog] {error_type}: {message} (User: {user_id}, Context: {context})")
    
    def get_recent_logs(self, limit: int = 10):
        """最近のエラーログを取得"""
        return self.logs[-limit:]
    
    def get_user_logs(self, user_id: int, limit: int = 5):
        """特定ユーザーのエラーログを取得"""
        user_logs = [log for log in self.logs if log.get("user_id") == user_id]
        return user_logs[-limit:]
    
    def clear_logs(self):
        """全ログをクリア"""
        self.logs = []

# グローバルエラーログマネージャー
error_log_manager = ErrorLogManager()

# ==============================
# ユーザースナップショット管理
# ==============================
class SnapshotManager:
    """ユーザーアクションのスナップショットを管理"""
    def __init__(self):
        self.snapshots = {}  # user_id: [snapshot1, snapshot2, ...]
    
    async def create_snapshot(self, user_id: int, action_type: str, player_data: dict):
        """スナップショットを作成（ディープコピーで完全な独立性を確保）"""
        if user_id not in self.snapshots:
            self.snapshots[user_id] = []
        
        # ディープコピーで完全に独立したスナップショットを作成
        # これにより、inventory、milestone_flags、equipped_weaponなどの
        # ネストされた可変オブジェクトも完全にコピーされる
        try:
            # JSON経由でディープコピー（最も安全な方法）
            player_data_copy = json.loads(json.dumps(player_data, default=str)) if player_data else None
        except (TypeError, ValueError):
            # JSON化できない場合はcopy.deepcopyを使用
            player_data_copy = copy.deepcopy(player_data) if player_data else None
        
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "data": player_data_copy
        }
        
        self.snapshots[user_id].append(snapshot)
        
        # 最大5個まで保持
        if len(self.snapshots[user_id]) > 5:
            self.snapshots[user_id] = self.snapshots[user_id][-5:]
        
        logger.info(f"Snapshot created (deep copy) for user {user_id}: {action_type}")
    
    def get_last_snapshot(self, user_id: int) -> Optional[dict]:
        """最後のスナップショットを取得"""
        if user_id in self.snapshots and len(self.snapshots[user_id]) > 0:
            return self.snapshots[user_id][-1]
        return None
    
    def remove_last_snapshot(self, user_id: int):
        """最後のスナップショットを削除（ロールバック後）"""
        if user_id in self.snapshots and len(self.snapshots[user_id]) > 0:
            self.snapshots[user_id].pop()

# グローバルスナップショットマネージャー
snapshot_manager = SnapshotManager()

# ==============================
# 管理者チェックデコレーター
# ==============================
def admin_only():
    """管理者専用コマンドチェック"""
    async def predicate(ctx: commands.Context):
        if ctx.author.id not in ADMIN_IDS:
            await ctx.send("⛔ このコマンドは管理者専用です。", delete_after=5)
            return False
        return True
    return commands.check(predicate)

# ==============================
# 管理者専用コマンド
# ==============================

@commands.command(name="admin_stats")
@admin_only()
async def admin_stats(ctx: commands.Context):
    """システム統計を表示"""
    try:
        # プレイヤー数をカウント
        all_players = await db.get_all_players()
        total_players = len(all_players) if all_players else 0
        
        # アクティブプレイヤー（距離>0）
        active_players = len([p for p in all_players if p.get("distance", 0) > 0]) if all_players else 0
        
        # 最も進んでいるプレイヤー
        max_distance_player = max(all_players, key=lambda p: p.get("distance", 0)) if all_players else None
        
        embed = discord.Embed(
            title="📊 システム統計",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        embed.add_field(name="総プレイヤー数", value=f"{total_players}人", inline=True)
        embed.add_field(name="アクティブプレイヤー", value=f"{active_players}人", inline=True)
        embed.add_field(name="エラーログ数", value=f"{len(error_log_manager.logs)}件", inline=True)
        
        if max_distance_player:
            embed.add_field(
                name="最遠到達プレイヤー",
                value=f"{max_distance_player.get('name', 'Unknown')} - {max_distance_player.get('distance', 0)}m",
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        error_log_manager.add_error("ADMIN_STATS", str(e), ctx.author.id, "admin_stats command")
        await ctx.send(f"⚠️ エラーが発生しました: {e}")

@commands.command(name="admin_logs")
@admin_only()
async def admin_logs(ctx: commands.Context, limit: int = 10):
    """最近のエラーログを表示"""
    try:
        logs = error_log_manager.get_recent_logs(min(limit, 25))
        
        if not logs:
            await ctx.send("📝 エラーログはありません。")
            return
        
        embed = discord.Embed(
            title=f"🔍 最近のエラーログ (最大{len(logs)}件)",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        
        for i, log in enumerate(logs[-10:], 1):  # 最大10件表示
            timestamp = log.get("timestamp", "Unknown")
            error_type = log.get("type", "Unknown")
            message = log.get("message", "No message")[:100]  # 100文字まで
            user_id = log.get("user_id", "N/A")
            
            embed.add_field(
                name=f"{i}. {error_type} ({timestamp[:19]})",
                value=f"User: {user_id}\nMessage: {message}",
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"⚠️ ログの取得に失敗しました: {e}")

@commands.command(name="admin_clear_logs")
@admin_only()
async def admin_clear_logs(ctx: commands.Context):
    """エラーログをクリア"""
    log_count = len(error_log_manager.logs)
    error_log_manager.clear_logs()
    await ctx.send(f"✅ {log_count}件のエラーログをクリアしました。")

@commands.command(name="admin_ban")
@admin_only()
async def admin_ban(ctx: commands.Context, user_id: str):
    """ユーザーをBAN"""
    try:
        await db.ban_player(user_id)
        await ctx.send(f"🔨 ユーザーID `{user_id}` をBANしました。")
        logger.warning(f"Admin {ctx.author.id} banned user {user_id}")
    except Exception as e:
        await ctx.send(f"⚠️ BANに失敗しました: {e}")

@commands.command(name="admin_unban")
@admin_only()
async def admin_unban(ctx: commands.Context, user_id: str):
    """ユーザーのBANを解除"""
    try:
        await db.unban_player(user_id)
        await ctx.send(f"✅ ユーザーID `{user_id}` のBANを解除しました。")
        logger.warning(f"Admin {ctx.author.id} unbanned user {user_id}")
    except Exception as e:
        await ctx.send(f"⚠️ BAN解除に失敗しました: {e}")

@commands.command(name="admin_player")
@admin_only()
async def admin_player(ctx: commands.Context, user_id: str):
    """プレイヤー情報を表示"""
    try:
        player = await db.get_player(user_id)
        
        if not player:
            await ctx.send(f"⚠️ ユーザーID `{user_id}` のデータが見つかりません。")
            return
        
        embed = discord.Embed(
            title=f"👤 プレイヤー情報: {player.get('name', 'Unknown')}",
            color=discord.Color.green()
        )
        
        embed.add_field(name="User ID", value=user_id, inline=True)
        embed.add_field(name="HP", value=f"{player.get('hp', 0)}/{player.get('max_hp', 0)}", inline=True)
        embed.add_field(name="距離", value=f"{player.get('distance', 0)}m", inline=True)
        embed.add_field(name="ゴールド", value=f"{player.get('gold', 0)}G", inline=True)
        embed.add_field(name="死亡回数", value=f"{player.get('death_count', 0)}回", inline=True)
        embed.add_field(name="レベル", value=f"{player.get('level', 1)}", inline=True)
        embed.add_field(name="BAN状態", value="🔨 BAN中" if player.get('is_banned') else "✅ 正常", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"⚠️ プレイヤー情報の取得に失敗しました: {e}")

@commands.command(name="admin_clear_processing")
@admin_only()
async def admin_clear_processing(ctx: commands.Context, user_id: int):
    """ユーザーのprocessingフラグをクリア（Embed固まり対策）"""
    try:
        # user_processing辞書から削除
        if hasattr(ctx.bot, 'user_processing'):
            if user_id in ctx.bot.user_processing:
                ctx.bot.user_processing[user_id] = False
                await ctx.send(f"✅ ユーザーID `{user_id}` のprocessingフラグをクリアしました。")
            else:
                await ctx.send(f"ℹ️ ユーザーID `{user_id}` のprocessingフラグは設定されていません。")
        else:
            await ctx.send("⚠️ user_processing辞書が見つかりません。")
        
        logger.info(f"Admin {ctx.author.id} cleared processing flag for user {user_id}")
        
    except Exception as e:
        await ctx.send(f"⚠️ クリアに失敗しました: {e}")

@commands.command(name="admin_force_reset")
@admin_only()
async def admin_force_reset(ctx: commands.Context, user_id: str):
    """プレイヤーデータを強制リセット"""
    try:
        await db.delete_player(user_id)
        await ctx.send(f"✅ ユーザーID `{user_id}` のデータを削除しました。")
        logger.warning(f"Admin {ctx.author.id} force reset user {user_id}")
    except Exception as e:
        await ctx.send(f"⚠️ リセットに失敗しました: {e}")

# ==============================
# ロールバック確認View
# ==============================
class RollbackConfirmView(discord.ui.View):
    def __init__(self, user_id: int, snapshot_data: dict, bot):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.snapshot_data = snapshot_data
        self.bot = bot
    
    @discord.ui.button(label="ロールバックする", style=discord.ButtonStyle.danger)
    async def confirm_rollback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたのロールバックではありません。", ephemeral=True)
        
        try:
            # 🔴 処理中フラグを強制クリア
            if hasattr(self.bot, 'user_processing'):
                self.bot.user_processing[self.user_id] = False
                logger.info(f"🔄 Rollback: user_processing cleared for user {self.user_id}")
            
            # プレイヤーデータを復元
            await db.update_player(
                self.user_id,
                hp=self.snapshot_data.get("hp"),
                mp=self.snapshot_data.get("mp"),
                distance=self.snapshot_data.get("distance"),
                gold=self.snapshot_data.get("gold"),
                inventory=self.snapshot_data.get("inventory"),
                equipped_weapon=self.snapshot_data.get("equipped_weapon"),
                equipped_armor=self.snapshot_data.get("equipped_armor"),
                current_floor=self.snapshot_data.get("current_floor"),
                current_stage=self.snapshot_data.get("current_stage"),
                milestone_flags=self.snapshot_data.get("milestone_flags", {}),
                story_flags=self.snapshot_data.get("story_flags", {})
            )
            
            # スナップショットを削除
            snapshot_manager.remove_last_snapshot(self.user_id)
            
            embed = discord.Embed(
                title="✅ ロールバック完了",
                description=f"アクションを取り消し、前の状態に戻しました。\n\n復元されたステータス:\n**HP**: {self.snapshot_data.get('hp')}/{self.snapshot_data.get('max_hp')}\n**MP**: {self.snapshot_data.get('mp')}/{self.snapshot_data.get('max_mp')}\n**距離**: {self.snapshot_data.get('distance')}m\n**ゴールド**: {self.snapshot_data.get('gold')}G\n\n再度 `!move` で冒険を続けられます。",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(embed=embed, view=None)
            
            logger.info(f"✅ Rollback completed for user {self.user_id}")
            
        except Exception as e:
            error_log_manager.add_error("ROLLBACK_CONFIRM", str(e), self.user_id, "rollback confirmation")
            await interaction.response.send_message(f"⚠️ ロールバックに失敗しました: {e}", ephemeral=True)
    
    @discord.ui.button(label="キャンセル", style=discord.ButtonStyle.secondary)
    async def cancel_rollback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("これはあなたのロールバックではありません。", ephemeral=True)
        
        embed = discord.Embed(
            title="❌ キャンセル",
            description="ロールバックをキャンセルしました。",
            color=discord.Color.grey()
        )
        await interaction.response.edit_message(embed=embed, view=None)


# ==============================
# ユーザー向けコマンド
# ==============================

@commands.command(name="rollback", aliases=["rb"])
async def rollback(ctx: commands.Context, force: str = None):
    """最後のアクションを取り消す
    
    使い方:
    !rollback - 確認後にロールバック
    !rollback force - 確認なしで即座にロールバック（戦闘中断用）
    """
    user_id = ctx.author.id
    
    try:
        # スナップショットを取得
        snapshot = snapshot_manager.get_last_snapshot(user_id)
        
        if not snapshot:
            embed = discord.Embed(
                title="⚠️ ロールバックできません",
                description="最近のアクション記録が見つかりませんでした。\n\n**!move**、戦闘、装備変更などのアクション後に使用できます。",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
        
        snapshot_data = snapshot.get("data")
        action_type = snapshot.get("action_type", "不明なアクション")
        timestamp = snapshot.get("timestamp", "不明な時刻")
        
        if not snapshot_data:
            embed = discord.Embed(
                title="⚠️ データが見つかりません",
                description="スナップショットデータが破損しています。",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # 🔴 forceオプションが指定された場合は即座にロールバック
        if force and force.lower() == "force":
            # 処理中フラグを強制クリア
            if hasattr(ctx.bot, 'user_processing'):
                ctx.bot.user_processing[user_id] = False
                logger.info(f"🔄 Force Rollback: user_processing cleared for user {user_id}")
            
            # プレイヤーデータを復元
            await db.update_player(
                user_id,
                hp=snapshot_data.get("hp"),
                mp=snapshot_data.get("mp"),
                distance=snapshot_data.get("distance"),
                gold=snapshot_data.get("gold"),
                inventory=snapshot_data.get("inventory"),
                equipped_weapon=snapshot_data.get("equipped_weapon"),
                equipped_armor=snapshot_data.get("equipped_armor"),
                current_floor=snapshot_data.get("current_floor"),
                current_stage=snapshot_data.get("current_stage"),
                milestone_flags=snapshot_data.get("milestone_flags", {}),
                story_flags=snapshot_data.get("story_flags", {})
            )
            
            # スナップショットを削除
            snapshot_manager.remove_last_snapshot(user_id)
            
            embed = discord.Embed(
                title="⚡ 強制ロールバック完了",
                description=f"**{action_type}** を強制的に取り消しました。\n\n復元されたステータス:\n**HP**: {snapshot_data.get('hp')}/{snapshot_data.get('max_hp')}\n**MP**: {snapshot_data.get('mp')}/{snapshot_data.get('max_mp')}\n**距離**: {snapshot_data.get('distance')}m\n**ゴールド**: {snapshot_data.get('gold')}G\n\n再度 `!move` で冒険を続けられます。",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
            logger.info(f"✅ Force rollback completed for user {user_id}")
            return
        
        # 通常の確認付きロールバック
        confirm_embed = discord.Embed(
            title="🔄 ロールバック確認",
            description=f"以下のアクションを取り消しますか？\n\n**アクション**: {action_type}\n**時刻**: {timestamp[:19]}\n\n⚠️ **進行中の戦闘・イベントは強制的に中断されます**\n\nヒント: `!rollback force` で即座にロールバックできます",
            color=discord.Color.blue()
        )
        
        view = RollbackConfirmView(user_id, snapshot_data, ctx.bot)
        await ctx.send(embed=confirm_embed, view=view)
        
    except Exception as e:
        error_log_manager.add_error("ROLLBACK", str(e), user_id, "rollback command")
        await ctx.send(f"⚠️ ロールバックに失敗しました: {e}")

@commands.command(name="debug_status")
async def debug_status(ctx: commands.Context):
    """自分のデバッグ情報を表示"""
    user_id = ctx.author.id
    
    try:
        # 処理状態を確認
        processing_status = "処理中" if ctx.bot.user_processing.get(user_id) else "待機中"
        
        # 最後のスナップショット情報
        snapshot = snapshot_manager.get_last_snapshot(user_id)
        snapshot_info = "なし"
        if snapshot:
            action_type = snapshot.get("action_type", "不明")
            timestamp = snapshot.get("timestamp", "不明")[:19]
            snapshot_info = f"{action_type} ({timestamp})"
        
        # ユーザーのエラーログを取得
        user_errors = error_log_manager.get_user_logs(user_id, limit=3)
        error_info = f"{len(user_errors)}件" if user_errors else "なし"
        
        embed = discord.Embed(
            title="🔍 デバッグ情報",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        embed.add_field(name="処理状態", value=processing_status, inline=True)
        embed.add_field(name="最後のスナップショット", value=snapshot_info, inline=False)
        embed.add_field(name="最近のエラー", value=error_info, inline=True)
        
        if user_errors:
            error_details = "\n".join([
                f"• {err.get('type', 'Unknown')}: {err.get('message', 'No message')[:50]}"
                for err in user_errors
            ])
            embed.add_field(name="エラー詳細", value=error_details, inline=False)
        
        embed.set_footer(text=f"User ID: {user_id}")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        error_log_manager.add_error("DEBUG_STATUS", str(e), user_id, "debug_status command")
        await ctx.send(f"⚠️ デバッグ情報の取得に失敗しました: {e}")

# ==============================
# お知らせ確認View
# ==============================
class NoticeConfirmView(discord.ui.View):
    def __init__(self, admin_id: int, message: str, bot: commands.Bot):
        super().__init__(timeout=300)
        self.admin_id = admin_id
        self.message = message
        self.bot = bot
    
    @discord.ui.button(label="📢 送信する", style=discord.ButtonStyle.primary)
    async def confirm_send(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.admin_id:
            return await interaction.response.send_message("これは管理者専用の操作です。", ephemeral=True)
        
        await interaction.response.defer()
        
        try:
            # RPGカテゴリを取得
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="RPG")
            
            if not category:
                await interaction.followup.send("⚠️ RPGカテゴリが見つかりません。")
                return
            
            # 成功/失敗カウンター
            success_count = 0
            failure_count = 0
            failed_channels = []
            
            # RPGカテゴリ内の全チャンネルを検索
            for channel in category.channels:
                # チャンネルのトピックに "UserID:" が含まれているかチェック
                if isinstance(channel, discord.TextChannel) and channel.topic and "UserID:" in channel.topic:
                    try:
                        # お知らせをEmbedで送信
                        embed = discord.Embed(
                            title="📢 運営からのお知らせ",
                            description=self.message,
                            color=discord.Color.blue(),
                            timestamp=datetime.now()
                        )
                        embed.set_footer(text="イニシエダンジョン運営チーム")
                        
                        await channel.send(embed=embed)
                        success_count += 1
                        
                        # レート制限（0.5秒待機）
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        failure_count += 1
                        failed_channels.append(f"{channel.name}: {str(e)[:50]}")
                        error_log_manager.add_error("NOTICE_SEND", str(e), None, f"channel: {channel.name}")
            
            # 結果を報告
            result_embed = discord.Embed(
                title="✅ お知らせ送信完了",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            
            result_embed.add_field(name="送信成功", value=f"{success_count}チャンネル", inline=True)
            result_embed.add_field(name="送信失敗", value=f"{failure_count}チャンネル", inline=True)
            result_embed.add_field(name="送信メッセージ", value=self.message[:200], inline=False)
            
            if failed_channels and len(failed_channels) <= 10:
                failure_text = "\n".join(failed_channels)
                result_embed.add_field(name="失敗詳細", value=failure_text, inline=False)
            
            await interaction.edit_original_response(embed=result_embed, view=None)
            
            logger.info(f"Admin {self.admin_id} sent notice to {success_count} channels")
            
        except Exception as e:
            error_log_manager.add_error("NOTICE_CONFIRM", str(e), self.admin_id, "notice confirmation")
            await interaction.followup.send(f"⚠️ お知らせ送信に失敗しました: {e}")
    
    @discord.ui.button(label="❌ キャンセル", style=discord.ButtonStyle.secondary)
    async def cancel_send(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.admin_id:
            return await interaction.response.send_message("これは管理者専用の操作です。", ephemeral=True)
        
        embed = discord.Embed(
            title="❌ キャンセル",
            description="お知らせ送信をキャンセルしました。",
            color=discord.Color.grey()
        )
        await interaction.response.edit_message(embed=embed, view=None)

# ==============================
# 管理者専用: お知らせ送信コマンド
# ==============================
@commands.command(name="notice")
@admin_only()
async def notice(ctx: commands.Context, *, message: str = None):
    """全プレイヤーチャンネルにお知らせを送信
    
    使い方:
    !notice <メッセージ>
    
    例:
    !notice メンテナンスのお知らせ：本日23時よりメンテナンスを実施します。
    """
    if not message:
        await ctx.send("⚠️ 使い方: `!notice <メッセージ>`")
        return
    
    try:
        # 確認Embedを表示
        confirm_embed = discord.Embed(
            title="📢 お知らせ送信確認",
            description="以下のメッセージを全プレイヤーチャンネルに送信しますか？",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        
        confirm_embed.add_field(
            name="送信メッセージ",
            value=message,
            inline=False
        )
        
        confirm_embed.add_field(
            name="⚠️ 注意",
            value="RPGカテゴリ内の全プレイヤーチャンネルに送信されます。\n送信後の取り消しはできません。",
            inline=False
        )
        
        view = NoticeConfirmView(ctx.author.id, message, ctx.bot)
        await ctx.send(embed=confirm_embed, view=view)
        
    except Exception as e:
        error_log_manager.add_error("NOTICE", str(e), ctx.author.id, "notice command")
        await ctx.send(f"⚠️ エラーが発生しました: {e}")

        
# ==============================
# コマンド登録ヘルパー
# ==============================

def setup_debug_commands(bot: commands.Bot):
    """デバッグコマンドをBotに登録"""
    bot.add_command(admin_stats)
    bot.add_command(admin_logs)
    bot.add_command(admin_clear_logs)
    bot.add_command(admin_ban)
    bot.add_command(admin_unban)
    bot.add_command(admin_player)
    bot.add_command(admin_clear_processing)
    bot.add_command(admin_force_reset)
    bot.add_command(notice)
    bot.add_command(rollback)
    bot.add_command(debug_status)
    
    # user_processingをbotに追加（存在しない場合）
    if not hasattr(bot, 'user_processing'):
        bot.user_processing = {}
    
    logger.info("✅ デバッグコマンドを登録しました")

# ==============================
# エクスポート
# ==============================

__all__ = [
    'setup_debug_commands',
    'error_log_manager',
    'snapshot_manager',
    'ErrorLogManager',
    'SnapshotManager'
]
