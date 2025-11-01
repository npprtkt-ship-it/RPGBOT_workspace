"""
死亡関連ストーリーデータ
特定の敵に殺された時、特定パターンで死んだ時のストーリー
"""

# ==============================
# 敵別死亡ストーリー（Lv1: テキスト変化）
# ==============================

DEATH_STORIES = {
    # スライム系
    "slime_death_3": {
        "trigger_type": "enemy_count",
        "enemy_name": "スライム",
        "required_count": 3,
        "title": "スライムの呪い",
        "lines": [
            {"speaker": "ナレーション", "text": "また…スライムに殺された。"},
            {"speaker": "ナレーション", "text": "なんだこの既視感は…"},
            {"speaker": "スライム", "text": "「また来たのか…お前、学習しないな」"},
            {"speaker": "ナレーション", "text": "スライムが…喋った？"},
            {"speaker": "スライム", "text": "「お前は何度もここで死んでいる。俺が覚えているぞ」"}
        ]
    },
    "slime_death_10": {
        "trigger_type": "enemy_count",
        "enemy_name": "スライム",
        "required_count": 10,
        "title": "スライムの友",
        "lines": [
            {"speaker": "スライム", "text": "「…もういいだろ、お前」"},
            {"speaker": "スライム", "text": "「10回も俺に殺されるなんて、それはもう縁だ」"},
            {"speaker": "ナレーション", "text": "スライムが何かを渡してきた…"},
            {"speaker": "スライム", "text": "「これを持っていけ。次は…負けるなよ」"},
            {"speaker": "ナレーション", "text": "スライムとの奇妙な友情が芽生えた気がする…"}
        ]
    },

    # ゴブリン系
    "goblin_death_5": {
        "trigger_type": "enemy_count",
        "enemy_name": "ゴブリン",
        "required_count": 5,
        "title": "ゴブリンの記憶",
        "lines": [
            {"speaker": "ゴブリン", "text": "「ギャハハ！また来たか、弱虫！」"},
            {"speaker": "ゴブリン", "text": "「お前、何回俺に殺されてんだ？」"},
            {"speaker": "ナレーション", "text": "ゴブリンは笑いながら指を折り始めた…"},
            {"speaker": "ゴブリン", "text": "「1、2、3、4…5回目だな！記念すべき5回目だ！」"},
            {"speaker": "ナレーション", "text": "なぜこいつは覚えているんだ…"}
        ]
    },

    # スケルトン系
    "skeleton_death_7": {
        "trigger_type": "enemy_count",
        "enemy_name": "スケルトン",
        "required_count": 7,
        "title": "骨との対話",
        "lines": [
            {"speaker": "スケルトン", "text": "「カタカタ…またお前か…」"},
            {"speaker": "ナレーション", "text": "スケルトンが剣を下ろした。"},
            {"speaker": "スケルトン", "text": "「お前…何度死んでも戻ってくるのだな」"},
            {"speaker": "スケルトン", "text": "「まるで…かつての俺のようだ」"},
            {"speaker": "ナレーション", "text": "スケルトンは遠い目をしている…気がする。"}
        ]
    },

    # ボス系
    "boss1_death_3": {
        "trigger_type": "enemy_count",
        "enemy_name": "スライムキング",
        "required_count": 3,
        "title": "王の慈悲",
        "lines": [
            {"speaker": "スライムキング", "text": "「…また来たのですか」"},
            {"speaker": "スライムキング", "text": "「あなたは何度私に挑むのですか？」"},
            {"speaker": "ナレーション", "text": "スライムキングが悲しそうに揺れている…"},
            {"speaker": "スライムキング", "text": "「もうやめてください…私も辛いのです」"},
            {"speaker": "ナレーション", "text": "ボスが…泣いている？"}
        ]
    },

    # 吸血鬼系
    "vampire_death_5": {
        "trigger_type": "enemy_count",
        "enemy_name": "吸血鬼",
        "required_count": 5,
        "title": "血の絆",
        "lines": [
            {"speaker": "吸血鬼", "text": "「フフフ…また会ったな、我が獲物よ」"},
            {"speaker": "吸血鬼", "text": "「お前の血は…もう何度味わったことか」"},
            {"speaker": "ナレーション", "text": "吸血鬼が不気味に笑う…"},
            {"speaker": "吸血鬼", "text": "「お前の血には…記憶が宿っている」"},
            {"speaker": "吸血鬼", "text": "「何度も何度も…死の記憶がな」"}
        ]
    },

    # 一般的な多死
    "many_deaths": {
        "trigger_type": "enemy_count",
        "enemy_name": "ANY",  # 特殊：任意の敵
        "required_count": 50,
        "title": "死の達人",
        "lines": [
            {"speaker": "???", "text": "「よく死んだな…」"},
            {"speaker": "ナレーション", "text": "どこからか声が聞こえる…"},
            {"speaker": "???", "text": "「お前はもう…死の達人だ」"},
            {"speaker": "???", "text": "「死ぬことに…慣れてしまったのだろう？」"},
            {"speaker": "ナレーション", "text": "確かに…死ぬことが怖くなくなってきた…"}
        ]
    }
}

# ==============================
# 連続死亡パターンストーリー
# ==============================

DEATH_PATTERNS = {
    "slime_triple": {
        "pattern": ["スライム", "スライム", "スライム"],
        "story_id": "pattern_slime_triple",
        "title": "スライム地獄",
        "lines": [
            {"speaker": "ナレーション", "text": "3連続でスライムに殺された…"},
            {"speaker": "ナレーション", "text": "これは…屈辱だ。"},
            {"speaker": "スライム", "text": "「プルプル…（学習しろよ…）」"},
            {"speaker": "ナレーション", "text": "スライムに煽られている気がする…"}
        ]
    },

    "boss_chain": {
        "pattern": ["スライムキング", "ゴーレム", "闇の騎士"],
        "story_id": "pattern_boss_chain",
        "title": "ボス巡礼",
        "lines": [
            {"speaker": "ナレーション", "text": "ボスに連続で殺された…"},
            {"speaker": "ナレーション", "text": "まるで…ボスに狙われているかのようだ。"},
            {"speaker": "???", "text": "「お前は…選ばれた存在なのかもしれんな」"},
            {"speaker": "ナレーション", "text": "選ばれた？何のために…？"}
        ]
    },

    "variety_deaths": {
        "pattern": ["スライム", "ゴブリン", "スケルトン", "ゾンビ", "吸血鬼"],
        "story_id": "pattern_variety",
        "title": "平等な死",
        "lines": [
            {"speaker": "ナレーション", "text": "様々な敵に殺された…"},
            {"speaker": "ナレーション", "text": "俺は…誰にでも殺される男なのか？"},
            {"speaker": "???", "text": "「お前は平等だ。どの敵にも分け隔てなく殺される」"},
            {"speaker": "ナレーション", "text": "それは…褒め言葉なのか…？"}
        ]
    },

    "undead_curse": {
        "pattern": ["スケルトン", "ゾンビ", "幽霊"],
        "story_id": "pattern_undead",
        "title": "不死者の呪い",
        "lines": [
            {"speaker": "ナレーション", "text": "アンデッド系に連続で殺された…"},
            {"speaker": "幽霊", "text": "「ウォォォ…仲間になれ…」"},
            {"speaker": "ナレーション", "text": "体が…冷たくなってきた気がする。"},
            {"speaker": "ナレーション", "text": "まさか…俺もアンデッドに…？"}
        ]
    }
}