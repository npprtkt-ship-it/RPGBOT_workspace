-- ========================================
-- Discord RPG Bot - Extended Schema for New Features
-- ========================================

-- プレイヤーテーブルに属性耐性カラムを追加
ALTER TABLE players 
ADD COLUMN IF NOT EXISTS fire_resistance INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS ice_resistance INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS lightning_resistance INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS dark_resistance INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS holy_resistance INTEGER DEFAULT 0;

-- レイドボステーブル（サーバー全体で共有）
CREATE TABLE IF NOT EXISTS raid_bosses (
    id BIGSERIAL PRIMARY KEY,
    boss_id TEXT UNIQUE NOT NULL,
    boss_name TEXT NOT NULL,
    distance INTEGER NOT NULL,
    current_hp INTEGER NOT NULL,
    max_hp INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    defeated_at TIMESTAMP WITH TIME ZONE,
    respawn_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- レイドボス貢献度テーブル
CREATE TABLE IF NOT EXISTS raid_contributions (
    id BIGSERIAL PRIMARY KEY,
    raid_boss_id BIGINT NOT NULL,
    user_id TEXT NOT NULL,
    damage_dealt INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (raid_boss_id) REFERENCES raid_bosses(id) ON DELETE CASCADE,
    UNIQUE(raid_boss_id, user_id)
);

-- 商人在庫テーブル（プレイヤー毎にランダム生成）
CREATE TABLE IF NOT EXISTS merchant_inventories (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    price INTEGER NOT NULL,
    slot_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES players(user_id) ON DELETE CASCADE
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_raid_bosses_boss_id ON raid_bosses(boss_id);
CREATE INDEX IF NOT EXISTS idx_raid_bosses_is_active ON raid_bosses(is_active);
CREATE INDEX IF NOT EXISTS idx_raid_contributions_raid_boss_id ON raid_contributions(raid_boss_id);
CREATE INDEX IF NOT EXISTS idx_raid_contributions_user_id ON raid_contributions(user_id);
CREATE INDEX IF NOT EXISTS idx_merchant_inventories_user_id ON merchant_inventories(user_id);

-- 更新時刻の自動更新トリガー
CREATE TRIGGER update_raid_bosses_updated_at BEFORE UPDATE ON raid_bosses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_raid_contributions_updated_at BEFORE UPDATE ON raid_contributions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- コメント
COMMENT ON TABLE raid_bosses IS 'サーバー全体で共有されるレイドボス情報';
COMMENT ON TABLE raid_contributions IS 'レイドボスへのプレイヤー貢献度';
COMMENT ON TABLE merchant_inventories IS '商人のアイテム在庫（プレイヤー毎）';
