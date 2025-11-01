-- ========================================
-- Discord RPG Bot - Supabase Schema
-- ========================================

-- プレイヤーテーブル
CREATE TABLE IF NOT EXISTS players (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    name TEXT,
    hp INTEGER DEFAULT 50,
    max_hp INTEGER DEFAULT 50,
    mp INTEGER DEFAULT 20,
    max_mp INTEGER DEFAULT 20,
    atk INTEGER DEFAULT 5,
    def INTEGER DEFAULT 2,
    distance INTEGER DEFAULT 0,
    current_floor INTEGER DEFAULT 0,
    current_stage INTEGER DEFAULT 0,
    gold INTEGER DEFAULT 0,
    exp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    death_count INTEGER DEFAULT 0,
    upgrade_points INTEGER DEFAULT 0,
    coin_multiplier NUMERIC DEFAULT 1.0,
    inventory JSONB DEFAULT '[]'::jsonb,
    equipped_weapon TEXT,
    equipped_armor TEXT,
    unlocked_skills JSONB DEFAULT '["体当たり"]'::jsonb,
    story_flags JSONB DEFAULT '{}'::jsonb,
    boss_defeated_flags JSONB DEFAULT '{}'::jsonb,
    milestone_flags JSONB DEFAULT '{}'::jsonb,
    tutorial_flags JSONB DEFAULT '{}'::jsonb,
    secret_weapon_ids JSONB DEFAULT '[]'::jsonb,
    mp_stunned BOOLEAN DEFAULT FALSE,
    game_cleared BOOLEAN DEFAULT FALSE,
    is_banned BOOLEAN DEFAULT FALSE,
    active_title_id TEXT,
    
    -- アップグレードレベル
    initial_hp_upgrade INTEGER DEFAULT 0,
    initial_mp_upgrade INTEGER DEFAULT 0,
    coin_gain_upgrade INTEGER DEFAULT 0,
    max_hp_upgrade INTEGER DEFAULT 0,
    max_mp_upgrade INTEGER DEFAULT 0,
    atk_upgrade INTEGER DEFAULT 0,
    def_upgrade INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 倉庫テーブル
CREATE TABLE IF NOT EXISTS storage (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    is_taken BOOLEAN DEFAULT FALSE,
    stored_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    taken_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (user_id) REFERENCES players(user_id) ON DELETE CASCADE
);

-- シークレット武器グローバル統計
CREATE TABLE IF NOT EXISTS secret_weapons_global (
    id BIGSERIAL PRIMARY KEY,
    weapon_id TEXT UNIQUE NOT NULL,
    total_dropped INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 死亡履歴テーブル
CREATE TABLE IF NOT EXISTS death_history (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    enemy_name TEXT NOT NULL,
    enemy_type TEXT DEFAULT 'normal',
    distance INTEGER DEFAULT 0,
    floor INTEGER DEFAULT 0,
    stage INTEGER DEFAULT 0,
    died_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES players(user_id) ON DELETE CASCADE
);

-- プレイヤー称号テーブル
CREATE TABLE IF NOT EXISTS player_titles (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    title_id TEXT NOT NULL,
    title_name TEXT NOT NULL,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, title_id),
    FOREIGN KEY (user_id) REFERENCES players(user_id) ON DELETE CASCADE
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_players_user_id ON players(user_id);
CREATE INDEX IF NOT EXISTS idx_storage_user_id ON storage(user_id);
CREATE INDEX IF NOT EXISTS idx_storage_is_taken ON storage(is_taken);
CREATE INDEX IF NOT EXISTS idx_death_history_user_id ON death_history(user_id);
CREATE INDEX IF NOT EXISTS idx_death_history_enemy_name ON death_history(enemy_name);
CREATE INDEX IF NOT EXISTS idx_player_titles_user_id ON player_titles(user_id);

-- 更新時刻の自動更新トリガー
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_players_updated_at BEFORE UPDATE ON players
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_secret_weapons_updated_at BEFORE UPDATE ON secret_weapons_global
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- サンプルデータ（オプション）
COMMENT ON TABLE players IS 'プレイヤーの基本情報とゲーム進行状況';
COMMENT ON TABLE storage IS 'プレイヤーの倉庫アイテム';
COMMENT ON TABLE secret_weapons_global IS 'シークレット武器のグローバル排出統計';
COMMENT ON TABLE death_history IS 'プレイヤーの死亡履歴';
COMMENT ON TABLE player_titles IS 'プレイヤーが獲得した称号';

-- ========================================
-- レイドボステーブル
-- ========================================

-- レイドボステーブル
CREATE TABLE IF NOT EXISTS raid_bosses (
    id BIGSERIAL PRIMARY KEY,
    boss_id TEXT UNIQUE NOT NULL,
    boss_name TEXT NOT NULL,
    distance INTEGER NOT NULL,
    current_hp INTEGER NOT NULL,
    max_hp INTEGER NOT NULL,
    atk INTEGER NOT NULL,
    def INTEGER NOT NULL,
    last_defeated_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- レイドボス貢献度テーブル
CREATE TABLE IF NOT EXISTS raid_contributions (
    id BIGSERIAL PRIMARY KEY,
    boss_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    total_damage INTEGER DEFAULT 0,
    last_contribution_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(boss_id, user_id),
    FOREIGN KEY (boss_id) REFERENCES raid_bosses(boss_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES players(user_id) ON DELETE CASCADE
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_raid_bosses_boss_id ON raid_bosses(boss_id);
CREATE INDEX IF NOT EXISTS idx_raid_bosses_distance ON raid_bosses(distance);
CREATE INDEX IF NOT EXISTS idx_raid_contributions_boss_id ON raid_contributions(boss_id);
CREATE INDEX IF NOT EXISTS idx_raid_contributions_user_id ON raid_contributions(user_id);

-- トリガー
CREATE TRIGGER update_raid_bosses_updated_at BEFORE UPDATE ON raid_bosses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- コメント
COMMENT ON TABLE raid_bosses IS 'レイドボス情報（500m毎、HP継続、1日復活）';
COMMENT ON TABLE raid_contributions IS 'プレイヤーのレイドボス貢献度（与ダメージ）';
