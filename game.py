import random

ITEMS_DATABASE = {
    "none": {
    },
    "HP回復薬（小）": {
        "type": "potion",
        "effect": "HP+30",
        "ability": "HP回復",
        "description": "HPを30回復する薬。"
    },
    "HP回復薬（中）": {
        "type": "potion",
        "effect": "HP+80",
        "ability": "HP中回復",
        "description": "HPを80回復する高級な薬。"
    },
    "HP回復薬（大）": {
        "type": "potion",
        "effect": "HP+200",
        "ability": "HP大回復",
        "description": "HPを200回復する貴重な薬。"
    },
    "MP回復薬（小）": {
        "type": "potion",
        "effect": "MP+30",
        "ability": "MP回復",
        "description": "MPを30回復する薬。"
    },
    "MP回復薬（中）": {
        "type": "potion",
        "effect": "MP+80",
        "ability": "MP中回復",
        "description": "MPを80回復する高級な薬。"
    },
    "MP回復薬（大）": {
        "type": "potion",
        "effect": "MP+200",
        "ability": "MP大回復",
        "description": "MPを200回復する貴重な薬。"
    },
    "エリクサー": {
        "type": "potion",
        "effect": "HPMPMAX",
        "ability": "HP・MP完全回復",
        "description": "HPとMPを完全回復させる幻の薬"
    },
    "木の剣": {
        "type": "weapon",
        "attack": 2,
        "ability": "なし",
        "description": "初心者向けの木製の剣。軽くて扱いやすい。"
    },
    "石の剣": {
        "type": "weapon",
        "attack": 4,
        "ability": "なし",
        "description": "石で作られた剣。木の剣より頑丈。"
    },
    "鉄の剣": {
        "type": "weapon",
        "attack": 6,
        "ability": "なし",
        "description": "鉄製の剣。切れ味が良い。"
    },
    "毒の短剣": {
        "type": "weapon",
        "attack": 10,
        "ability": "毒付与（5%の確率で追加ダメージ）",
        "description": "毒が塗られた短剣。相手を弱らせる。"
    },
    "王者の剣": {
        "type": "weapon",
        "attack": 8,
        "ability": "全ステータス+20%、全状態異常耐性+50%",
        "description": "遥か昔に造られた剣。刀身の輝きは未だ失われていない。"
    },
    "骨の剣": {
        "type": "weapon",
        "attack": 5,
        "ability": "アンデッド特効（アンデッド系に+30%ダメージ）",
        "description": "骨で作られた不気味な剣。"
    },
    "呪いの剣": {
        "type": "weapon",
        "attack": 6,
        "ability": "呪い（攻撃時にHP-5、ダメージ+50%）",
        "description": "呪われた剣。強力だが使用者にも害を及ぼす。"
    },
    "魔法の杖": {
        "type": "weapon",
        "attack": 10,
        "ability": "魔力増幅（魔法攻撃+50%）",
        "description": "魔力が込められた杖。魔法使いに最適。"
    },
    "死神の鎌": {
        "type": "weapon",
        "attack": 16,
        "ability": "攻撃時10%で即死効果（ボス無効）",
        "description": "死神が持つ恐るべき鎌。"
    },
    "炎の大剣": {
        "type": "weapon",
        "attack": 10,
        "ability": "炎属性（追加で炎ダメージ+5）",
        "description": "炎を纏った大剣。燃え盛る力を持つ。"
    },
    "ドラゴンソード": {
        "type": "weapon",
        "attack": 12,
        "ability": "竜の力（全ステータス+15%）",
        "description": "伝説の竜の牙から作られた剣。"
    },
    "黒騎士の剣": {
        "type": "weapon",
        "attack": 12,
        "ability": "闇属性（闇の敵に+50%ダメージ）",
        "description": "黒騎士が使っていた漆黒の剣。"
    },
    "炎獄の剣": {
        "type": "weapon",
        "attack": 12,
        "ability": "攻撃時30%で敵を燃焼（2ターン、ダメージ10）",
        "description": "業火を纏う剣。敵を焼き尽くす。"
    },
    "業火の剣": {
        "type": "weapon",
        "attack": 12,
        "ability": "攻撃時20%で敵を燃焼状態にする（2ターン、ダメージ10）",
        "description": "地獄の炎を纏った大剣。"
    },
    "影の短剣": {
        "type": "weapon",
        "attack": 14,
        "ability": "クリティカル率+25%、背後攻撃時ダメージ2倍",
        "description": "影より生まれし短剣。"
    },
    "血の剣": {
        "type": "weapon",
        "attack": 16,
        "ability": "攻撃時HP吸収（ダメージの10%）",
        "description": "血を吸う魔剣。生命力を奪う。"
    },
    "死霊の杖": {
        "type": "weapon",
        "attack": 18,
        "ability": "攻撃時25%でアンデッド召喚（次ターンHP10回復）",
        "description": "死霊を操る杖。"
    },
    "雷神の槍": {
        "type": "weapon",
        "defense": 20,
        "ability": "攻撃時20%で敵を麻痺状態にする、クリティカル率+15%",
        "description": "雷の力を宿した槍。敵を麻痺させる。"
    },
    "暗黒の弓": {
        "type": "weapon",
        "attack": 18,
        "ability": "遠距離攻撃、命中率+20%、貫通ダメージ",
        "description": "闇の力を矢に込める弓。"
    },
    "破壊の斧": {
        "type": "weapon",
        "attack": 18,
        "ability": "攻撃力+20%、防御力-10%、装甲貫通+30%",
        "description": "全てを破壊する巨斧。"
    },
    "虚無の剣": {
        "type": "weapon",
        "attack": 22,
        "ability": "攻撃時15%で敵の防御力無視、MP吸収10",
        "description": "虚無の力を宿す剣。"
    },
    "氷結の杖": {
        "type": "weapon",
        "defense": 20,
        "ability": "攻撃時20%で敵を凍結状態にする、装甲貫通+20%",
        "description": "氷の力を宿した杖。敵を凍結させる。"
    },
    "カオスブレード": {
        "type": "weapon",
        "attack": 20,
        "ability": "攻撃時ランダム効果（燃焼・毒・防御無視・分身攻撃のいずれか）",
        "description": "混沌の力を宿す剣。予測不能な力。"
    },
    "炎の剣": {
        "type": "weapon",
        "attack": 24,
        "ability": "炎属性（追加で炎ダメージ+5）、攻撃時20%で燃焼（2ターン、ダメージ15）",
        "description": "炎を司る神剣。"
    },
    "滅びの剣": {
        "type": "weapon",
        "attack": 24,
        "ability": "攻撃力+30%、攻撃時10%で敵の最大HP-10%",
        "description": "炎を司る神剣。"
    },
    "炎の大剣": {
        "type": "weapon",
        "attack": 26,
        "ability": "炎属性（追加で炎ダメージ+10）、攻撃時30%で燃焼（2ターン、ダメージ15）",
        "description": "炎を司る神剣。"
    },
    "深淵の剣": {
        "type": "weapon",
        "attack": 30,
        "ability": "攻撃時敵のMP-20、MP吸収30%、闇属性",
        "description": "深淵の力を解放する剣。"
    },
    "四元の剣": {
        "type": "weapon",
        "attack": 25,
        "ability": "全属性攻撃、敵の弱点属性自動判定+50%ダメージ",
        "description": "四大元素を操る神剣。"
    },
    "天の槌": {
        "type": "weapon",
        "attack": 22,
        "ability": "攻撃力+20%、クリティカル時ダメージ3倍、神聖属性",
        "description": "天界の鍛冶神が造りし槌。"
    },
    "深淵の剣": {
        "type": "weapon",
        "attack": 25,
        "ability": "攻撃力+20%、攻撃時15%で敵の防御力無視",
        "description": "深淵の底に眠る剣。"
    },
    "暗黒聖剣": {
        "type": "weapon",
        "attack": 28,
        "ability": "攻撃時HP吸収20%、闇属性、聖属性の敵に特効+50%",
        "description": "堕ちた聖剣。闇に染まりし力。"
    },
    "水神の槍": {
        "type": "weapon",
        "attack": 32,
        "ability": "水属性、攻撃時20%で敵を凍結（2ターン行動不能）",
        "description": "水神が持つ聖槍。"
    },
    "獄炎の剣": {
        "type": "weapon",
        "attack": 26,
        "ability": "3回攻撃、各攻撃40%で燃焼（累積ダメージ）",
        "description": "地獄の炎を3連撃で放つ剣。"
    },
    "竜帝の剣": {
        "type": "weapon",
        "attack": 30,
        "ability": "全ステータス+20%、竜の咆哮（敵怯み）",
        "description": "竜帝が振るう至高の剣。"
    },
    "幻影の剣": {
        "type": "weapon",
        "attack": 32,
        "ability": "回避率+30%、攻撃時分身攻撃（2回攻撃）",
        "description": "幻影を生み出す神秘の剣。"
    },
    "混沌神剣": {
        "type": "weapon",
        "attack": 28,
        "ability": "攻撃力+50%、ボスに特効+50%",
        "description": "混沌の神が振るう剣。"
    },
    "死神の剣": {
        "type": "weapon",
        "attack": 30,
        "ability": "攻撃時HP吸収（ダメージの10%）, アンデッド特効+50%",
        "description": "死神が持つ究極の大鎌。"
    },
    "魔王の双剣": {
        "type": "weapon",
        "attack": 35,
        "ability": "2回攻撃, クリティカル率+20%, クリティカル時ダメージ3倍",
        "description": "ダンジョンの最奥地に眠る魔王が持っていると語り継がれていた双剣。"
    },
    "革の盾": {
        "type": "armor",
        "defense": 1,
        "ability": "なし",
        "description": "革製の盾。何も装備しないよりはいい。"
    },
    "木の盾": {
        "type": "armor",
        "defense": 2,
        "ability": "なし",
        "description": "木製の盾。簡素だが軽い。"
    },
    "石の盾": {
        "type": "armor",
        "defense": 4,
        "ability": "なし",
        "description": "石で作られた盾。頑丈。"
    },
    "鉄の盾": {
        "type": "armor",
        "defense": 7,
        "ability": "なし",
        "description": "鉄製の盾。高い防御力を持つ。"
    },
    "スライムの王冠": {
        "type": "armor",
        "defense": 5,
        "ability": "HP+30",
        "description": "スライムキングが落とした王冠。生命力が強くなる。"
    }, 
    "骨の盾": {
        "type": "armor",
        "defense": 5,
        "ability": "物理ダメージ軽減-15%",
        "description": "骨で作られた盾。意外と丈夫。"
    },
    "死者の兜": {
        "type": "armor",
        "defense": 6,
        "ability": "即死耐性（即死攻撃無効）",
        "description": "死者が被っていた兜。死を恐れない。"
    },
    "不死の鎧": {
        "type": "armor",
        "defense": 8,
        "ability": "HP自動回復（ターン毎+5HP）",
        "description": "不死者の鎧。生命力が湧き出る。"
    },
    "幽霊の布": {
        "type": "armor",
        "defense": 10,
        "ability": "回避率+20%",
        "description": "幽霊が纏っていた布。攻撃をすり抜ける。"
    },
    "地獄の鎧": {
        "type": "armor",
        "defense": 8,
        "ability": "炎耐性+50%",
        "description": "地獄の炎で鍛えられた鎧。"
    },
    "黒騎士の盾": {
        "type": "armor",
        "defense": 9,
        "ability": "反撃（被ダメージの10%を返す）",
        "description": "黒騎士の盾。攻撃を跳ね返す。"
    },
    "黒騎士の鎧": {
        "type": "armor",
        "defense": 10,
        "ability": "闇耐性+70%",
        "description": "黒騎士の漆黒の鎧。闇の力に強い。"
    },
    "竜の鱗": {
        "type": "armor",
        "defense": 13,
        "ability": "全属性耐性+20%",
        "description": "竜の鱗で作られた鎧。あらゆる攻撃に強い。"
    },
    "悪魔の盾": {
        "type": "armor",
        "defense": 11,
        "ability": "魔法ダメージ30%軽減",
        "description": "悪魔の力が込められた盾。"
    },
    "冥界の盾": {
        "type": "armor",
        "defense": 12,
        "ability": "アンデッド特効+30%、毒無効",
        "description": "冥界の力を宿した盾。"
    },
    "死の鎧": {
        "type": "armor",
        "defense": 15,
        "ability": "被ダメージ時20%でHP吸収（ダメージの30%）、HP+50",
        "description": "死の力を纏う漆黒の鎧。"
    },
    "炎の鎧": {
        "type": "armor",
        "defense": 13,
        "ability": "炎耐性+50%、被攻撃時10%で反射ダメージ10",
        "description": "炎を纏う鎧。攻撃を焼き返す。"
    },
    "夜の外套": {
        "type": "armor",
        "defense": 14,
        "ability": "回避率+20%、夜間戦闘時攻撃力+30%",
        "description": "闇夜に溶け込む外套。"
    },
    "不死王の冠": {
        "type": "armor",
        "defense": 16,
        "ability": "HP+30、毒・麻痺・呪い無効",
        "description": "不死の王が被る冠。"
    },
    "祝福の盾": {
        "type": "armor",
        "defense": 16,
        "ability": "全状態異常無効、HP自動回復+10/ターン",
        "description": "神の加護を受けた盾。あらゆる異常を防ぐ。"
    },
    "巨人の鎧": {
        "type": "armor",
        "defense": 18,
        "ability": "HP+50、被ダメージ-20%、移動速度-10%",
        "description": "巨人族の鎧。圧倒的な防御力。"
    },
    "幻影の鎧": {
        "type": "armor",
        "defense": 21,
        "ability": "回避率+20%、幻影分身（被攻撃時20%で回避）",
        "description": "実体を持たぬ幻の鎧。"
    },
    "氷の鎧": {
        "type": "armor",
        "defense": 20,
        "ability": "物理ダメージ軽減-30%",
        "description": "氷で作られた鎧。この氷は永遠に溶けることがない。"
    },
    "混沌の鎧": {
        "type": "armor",
        "defense": 22,
        "ability": "全状態異常耐性+50%、ランダム属性耐性+50%",
        "description": "混沌が守護する鎧。"
    },
    "再生の鎧": {
        "type": "armor",
        "defense": 20,
        "ability": "HP自動回復（ターン毎+5HP）",
        "description": "再生能力を持つ鎧。"
    },
    "終焉の盾": {
        "type": "armor",
        "defense": 20,
        "ability": "全ダメージ-25%、必殺技ダメージ-50%",
        "description": "終焉を防ぐ究極の盾。"
    },
    "虚空の鎧": {
        "type": "armor",
        "defense": 26,
        "ability": "回避率+30%",
        "description": "虚空の力で魔法を無効化する鎧。"
    },
    "精霊の盾": {
        "type": "armor",
        "defense": 24,
        "ability": "全属性耐性+20%、精霊加護（致死ダメージ時1回生存）",
        "description": "精霊の加護を受けた盾。"
    },
    "神の盾": {
        "type": "armor",
        "defense": 20,
        "ability": "全ダメージ-20%、神の加護（HP30%以下で防御力1.5倍）",
        "description": "神々が守護する盾。"
    },
    "勇者の鎧": {
        "type": "armor",
        "defense": 24,
        "ability": "全ステータス+30%",
        "description": "伝説の勇者が身に纏った鎧。"
    },
    "堕天の鎧": {
        "type": "armor",
        "defense": 22,
        "ability": "HP+50、攻撃力+20%、防御力+20%",
        "description": "堕天使が纏う漆黒の鎧。"
    },
    "深海の鎧": {
        "type": "armor",
        "defense": 25,
        "ability": "水・氷耐性40%、HP自動回復+5/ターン",
        "description": "深海の圧力に耐える鎧。"
    },
    "地獄門の鎧": {
        "type": "armor",
        "defense": 28,
        "ability": "HP+50、被攻撃時30%で反撃ダメージ20",
        "description": "地獄の門を守る鎧。"
    },
    "竜帝の鎧": {
        "type": "armor",
        "defense": 30,
        "ability": "HP+80、全属性耐性+20%、竜鱗の守護（致死ダメージ無効1回）",
        "description": "竜帝の力を宿す究極の鎧。"
    },
    "幻王の鎧": {
        "type": "armor",
        "defense": 25,
        "ability": "回避率+25%、被攻撃時25%で完全回避",
        "description": "幻王が纏う実体なき鎧。"
    },
    "創世の盾": {
        "type": "armor",
        "defense": 28,
        "ability": "全ダメージ-30%、HP+50、完全蘇生（戦闘中1回のみ）",
        "description": "世界を創りし神の盾。"
    },
    "死帝の鎧": {
        "type": "armor",
        "defense": 30,
        "ability": "HP+50、全状態異常耐性+50%、不死の力（HP0で復活3回まで）",
        "description": "死の皇帝が纏う不滅の鎧。"
    },
    "魔王の鎧": {
        "type": "armor",
        "defense": 35,
        "ability": "HP+100、全ステータス+30%",
        "description": "ダンジョンの最奥地に眠る魔王が持っていると語り継がれていた双剣。"
    },
    "呪いの首輪": {
        "type": "armor",
        "defense": -10,
        "ability": "攻撃力+50%（デバフ防具）",
        "description": "装備者の防御を下げるが、攻撃力が大幅に上がる呪われた首輪。"
    },
    "重い鎖": {
        "type": "armor",
        "defense": -5,
        "ability": "HP+100、移動速度-20%（デバフ防具）",
        "description": "重い鎖。防御は下がるがHPが増加する。"
    },
    "破滅の兜": {
        "type": "armor",
        "defense": -15,
        "ability": "クリティカル率+30%（デバフ防具）",
        "description": "防御を犠牲にクリティカル率を大幅に上げる危険な兜。"
    },
    "狂戦士の鎧": {
        "type": "armor",
        "defense": -20,
        "ability": "攻撃力+100%、被ダメージ+50%（デバフ防具）",
        "description": "狂戦士が纏う鎧。攻撃力を劇的に上げるが致命的に脆くなる。"
    },
    "蜘蛛の糸": {
        "type": "material",
        "ability": "素材",
        "description": "蜘蛛から採れる糸。装備の素材になる。"
    },
    "悪魔の角": {
        "type": "material",
        "ability": "素材",
        "description": "悪魔の角。強力な装備の素材。"
    },
    "竜の牙": {
        "type": "material",
        "ability": "素材",
        "description": "竜の牙。伝説の武器を作れる。"
    },
    "闇の宝珠": {
        "type": "material",
        "ability": "素材",
        "description": "闇の力が込められた宝珠。"
    },
    "腐った肉": {
        "type": "material",
        "ability": "素材",
        "description": "ゾンビの肉。錬金術に使える。"
    },
    "魔界の結晶": {
        "type": "material",
        "ability": "素材",
        "description": "魔界の力が宿る結晶。高位の装備に使える。"
    },
    "古竜の心臓": {
        "type": "material",
        "ability": "素材",
        "description": "古竜の心臓。絶大な力を秘めている。"
    },
    "竜王の牙": {
        "type": "material",
        "ability": "素材",
        "description": "竜王の牙。ドラゴン系特効武器の素材。"
    },
    "地獄犬の牙": {
        "type": "material",
        "ability": "素材",
        "description": "地獄の番犬の牙。炎属性武器の素材。"
    },
    "吸血鬼の牙": {
        "type": "material",
        "ability": "素材",
        "description": "吸血鬼の牙。HP吸収武器の素材。"
    },
    "魔導書の欠片": {
        "type": "material",
        "ability": "素材",
        "description": "古代魔導書の欠片。魔法系装備の素材。"
    },
    "闇の宝石": {
        "type": "material",
        "ability": "素材",
        "description": "漆黒の宝石。闇属性装備の核となる。"
    },
    "巨獣の皮": {
        "type": "material",
        "ability": "素材",
        "description": "巨大な獣の皮。強固な防具の素材。"
    },
    "影の欠片": {
        "type": "material",
        "ability": "素材",
        "description": "影そのものの欠片。幻影系装備の素材。"
    },
    "混沌の欠片": {
        "type": "material",
        "ability": "素材",
        "description": "混沌の力の欠片。究極装備の素材。"
    },
    "不死鳥の羽": {
        "type": "material",
        "ability": "素材",
        "description": "不死鳥の羽。復活系装備の素材。"
    },
    "破壊の核": {
        "type": "material",
        "ability": "素材",
        "description": "破壊の化身の核。破壊力を極めた装備の素材。"
    },
    "深淵の結晶": {
        "type": "material",
        "ability": "素材",
        "description": "深淵の底から取れる結晶。深遠な力を秘める。"
    },
    "元素の核": {
        "type": "material",
        "ability": "素材",
        "description": "四大元素の核。全属性を操る装備の素材。"
    },
    "神の鉱石": {
        "type": "material",
        "ability": "素材",
        "description": "神々が使う鉱石。神器の素材。"
    },
    "闇の聖典": {
        "type": "material",
        "ability": "素材",
        "description": "禁断の魔導書。禁忌の力を解き放つ。"
    },
    "海皇の鱗": {
        "type": "material",
        "ability": "素材",
        "description": "海の支配者の鱗。水属性最強装備の素材。"
    },
    "三首の牙": {
        "type": "material",
        "ability": "素材",
        "description": "三つの首を持つ獣の牙。多重攻撃装備の素材。"
    },
    "幻王の魂": {
        "type": "material",
        "ability": "素材",
        "description": "幻影の王の魂。究極の幻影装備の素材。"
    },
    "竜帝の心臓": {
        "type": "material",
        "ability": "素材",
        "description": "竜の皇帝の心臓。竜系最強装備の素材。"
    },
    "神殺しの結晶": {
        "type": "material",
        "ability": "素材",
        "description": "神をも殺す力を秘めた結晶。禁断の力。"
    },
    "死皇の冠": {
        "type": "material",
        "ability": "素材",
        "description": "死を統べる皇帝の冠。死の力を極めた装備の素材。"
    }
}


ENEMY_ZONES = {
    "0-1000": {
        "enemies": [
            {
                "name": "スライム",
                "hp": 20,
                "atk": 3,
                "def": 2,
                "element": "none",
                "ai_pattern": "balanced",
                "weight": 35,
                "exp": 8,
                "drops": [
                    {"item": "none", "weight": 55},
                    {"item": "木の剣", "weight": 10},
                    {"item": "革の盾", "weight": 10},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [10, 30], "weight": 15}
                ]
            },
            {
                "name": "バット",
                "hp": 15,
                "atk": 4,
                "def": 1,
                "element": "dark",
                "ai_pattern": "aggressive",
                "weight": 30,
                "exp": 10,
                "drops": [
                    {"item": "none", "weight": 60},
                    {"item": "蝙蝠の翼", "weight": 20},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [15, 25], "weight": 10}
                ]
            },
            {
                "name": "ゴブリン",
                "hp": 25,
                "atk": 5,
                "def": 3,
                "element": "none",
                "ai_pattern": "aggressive",
                "weight": 25,
                "exp": 12,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "石の剣", "weight": 15},
                    {"item": "木の盾", "weight": 10},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [20, 40], "weight": 15}
                ]
            },
            {
                "name": "スパイダー",
                "hp": 30,
                "atk": 6,
                "def": 2,
                "element": "none",
                "ai_pattern": "balanced",
                "weight": 20,
                "exp": 15,
                "drops": [
                    {"item": "none", "weight": 40},
                    {"item": "蜘蛛の糸", "weight": 25},
                    {"item": "毒の短剣", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [30, 50], "weight": 20}
                ]
            },
            {
                "name": "ゾンビ",
                "hp": 40,
                "atk": 7,
                "def": 3,
                "element": "dark",
                "ai_pattern": "balanced",
                "weight": 15,
                "exp": 18,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "腐った肉", "weight": 20},
                    {"item": "骨の剣", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "MP回復薬（小）", "weight": 5},
                    {"item": "coins", "amount": [25, 45], "weight": 10}
                ]
            },
            {
                "name": "スケルトン",
                "hp": 35,
                "atk": 8,
                "def": 4,
                "element": "dark",
                "ai_pattern": "balanced",
                "weight": 12,
                "exp": 20,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "骨の剣", "weight": 10},
                    {"item": "骨の盾", "weight": 10},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "MP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [30, 50], "weight": 10}
                ]
            }
        ]
    },
    "1001-2000": {
        "enemies": [
            {
                "name": "スケルトン",
                "hp": 35,
                "atk": 6,
                "def": 4,
                "attribute": "dark",
                "weight": 50,
                "exp": 22,
                "drops": [
                    {"item": "none", "weight": 60},
                    {"item": "骨の剣", "weight": 6},
                    {"item": "骨の盾", "weight": 6},
                    {"item": "HP回復薬（小）", "weight": 9},
                    {"item": "MP回復薬（小）", "weight": 9},
                    {"item": "coins", "amount": [20, 40], "weight": 10}
                ]
            },
            {
                "name": "ゾンビ",
                "hp": 45,
                "atk": 7,
                "def": 3,
                "attribute": "dark",
                "weight": 35,
                "exp": 25,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "腐った肉", "weight": 20},
                    {"item": "呪いの剣", "weight": 10},
                    {"item": "死者の兜", "weight": 5},
                    {"item": "鉄の盾", "weight": 5},
                    {"item": "coins", "amount": [25, 40], "weight": 10}
                ]
            },
            {
                "name": "ゴースト",
                "hp": 40,
                "atk": 8,
                "def": 5,
                "attribute": "dark",
                "weight": 15,
                "exp": 40,
                "drops": [
                    {"item": "none", "weight": 40},
                    {"item": "幽霊の布", "weight": 10},
                    {"item": "魔法の杖", "weight": 10},
                    {"item": "HP回復薬（小）", "weight": 10},
                    {"item": "MP回復薬（小）", "weight": 10},
                    {"item": "coins", "amount": [50, 70], "weight": 20}
                ]
            }
        ]
    },
    "2001-3000": {
        "enemies": [
            {
                "name": "デーモン",
                "hp": 70,
                "atk": 9,
                "def": 6,
                "attribute": "fire",
                "weight": 50,
                "exp": 32,
                "drops": [
                    {"item": "none", "weight": 45},
                    {"item": "悪魔の角", "weight": 15},
                    {"item": "炎の大剣", "weight": 5},
                    {"item": "地獄の鎧", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "MP回復薬（小）", "weight": 8},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [30, 50], "weight": 10}
                ]
            },
            {
                "name": "ダークナイト",
                "hp": 50,
                "atk": 10,
                "def": 7,
                "attribute": "dark",
                "weight": 40,
                "exp": 35,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "黒騎士の剣", "weight": 10},
                    {"item": "黒騎士の盾", "weight": 5},
                    {"item": "黒騎士の鎧", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "MP回復薬（小）", "weight": 8},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [35, 50], "weight": 10}
                ]
            },
            {
                "name": "ドラゴン",
                "hp": 80,
                "atk": 14,
                "def": 6,
                "attribute": "fire",
                "weight": 10,
                "exp": 60,
                "drops": [
                    {"item": "竜の牙", "weight": 40},
                    {"item": "ドラゴンソード", "weight": 20},
                    {"item": "竜の鱗", "weight": 5},
                    {"item": "HP回復薬（中）", "weight": 10},
                    {"item": "MP回復薬（中）", "weight": 10},
                    {"item": "coins", "amount": [60, 90], "weight": 15}
                ]
            }
        ]
    },
    "3001-4000": {
        "enemies": [
            {
                "name": "デスナイト",
                "hp": 100,
                "atk": 13,
                "def": 8,
                "attribute": "dark",
                "weight": 50,
                "exp": 48,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "死神の鎌", "weight": 10},
                    {"item": "冥界の盾", "weight": 9},
                    {"item": "死の鎧", "weight": 1},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "MP回復薬（小）", "weight": 8},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [50, 65], "weight": 10}
                ]
            },
            {
                "name": "アークデーモン",
                "hp": 80,
                "atk": 15,
                "def": 9,
                "attribute": "fire",
                "weight": 40,
                "exp": 50,
                "drops": [
                    {"item": "none", "weight": 45},
                    {"item": "魔界の結晶", "weight": 15},
                    {"item": "炎獄の剣", "weight": 5},
                    {"item": "悪魔の盾", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 8},
                    {"item": "MP回復薬（小）", "weight": 8},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [40, 60], "weight": 10}
                ]
            },
            {
                "name": "エンシェントドラゴン",
                "hp": 120,
                "atk": 17,
                "def": 7,
                "attribute": "fire",
                "weight": 10,
                "exp": 80,
                "drops": [
                    {"item": "竜王の牙", "weight": 40},
                    {"item": "古竜の心臓", "weight": 10},
                    {"item": "竜の鱗", "weight": 15},
                    {"item": "HP回復薬（中）", "weight": 10},
                    {"item": "MP回復薬（中）", "weight": 10},
                    {"item": "coins", "amount": [80, 100], "weight": 15}
                ]
            },
        ]
    },
    "4001-5000": {
        "enemies": [
            {
                "name": "ヘルハウンド",
                "hp": 130,
                "atk": 20,
                "def": 10,
                "attribute": "fire",
                "weight": 40,
                "exp": 60,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "地獄犬の牙", "weight": 20},
                    {"item": "業火の剣", "weight": 5},
                    {"item": "炎の鎧", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 3},
                    {"item": "MP回復薬（小）", "weight": 3},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [60, 90], "weight": 10}
                ]
            },
            {
                "name": "ヴァンパイアロード",
                "hp": 110,
                "atk": 19,
                "def": 11,
                "attribute": "dark",
                "weight": 30,
                "exp": 65,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "吸血鬼の牙", "weight": 20},
                    {"item": "血の剣", "weight": 2},
                    {"item": "夜の外套", "weight": 10},
                    {"item": "HP回復薬（小）", "weight": 2},
                    {"item": "MP回復薬（小）", "weight": 2},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [70, 90], "weight": 10}
                ]
            },
            {
                "name": "リッチ",
                "hp": 140,
                "atk": 22,
                "def": 10,
                "attribute": "dark",
                "weight": 30,
                "exp": 68,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "魔導書の欠片", "weight": 20},
                    {"item": "死霊の杖", "weight": 5},
                    {"item": "不死王の冠", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 3},
                    {"item": "MP回復薬（小）", "weight": 3},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [70, 100], "weight": 10}
                ]
            }
        ]
    },
    "5001-6000": {
        "enemies": [
            {
                "name": "ダークエルフ",
                "hp": 150,
                "atk": 24,
                "def": 12,
                "attribute": "dark",
                "weight": 35,
                "exp": 75,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "闇の宝石", "weight": 20},
                    {"item": "影の短剣", "weight": 8},
                    {"item": "暗黒の弓", "weight": 2},
                    {"item": "HP回復薬（小）", "weight": 3},
                    {"item": "MP回復薬（小）", "weight": 3},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [80, 120], "weight": 10}
                ]
            },
            {
                "name": "ベヒーモス",
                "hp": 190,
                "atk": 26,
                "def": 14,
                "attribute": "none",
                "weight": 35,
                "exp": 85,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "巨獣の皮", "weight": 20},
                    {"item": "破壊の斧", "weight": 8},
                    {"item": "巨人の鎧", "weight": 2},
                    {"item": "HP回復薬（小）", "weight": 3},
                    {"item": "MP回復薬（小）", "weight": 3},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [70, 135], "weight": 10}
                ]
            },
            {
                "name": "シャドウロード",
                "hp": 170,
                "atk": 25,
                "def": 13,
                "attribute": "dark",
                "weight": 30,
                "exp": 80,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "影の欠片", "weight": 20},
                    {"item": "虚無の剣", "weight": 5},
                    {"item": "幻影の鎧", "weight": 5},
                    {"item": "HP回復薬（小）", "weight": 3},
                    {"item": "MP回復薬（小）", "weight": 3},
                    {"item": "HP回復薬（中）", "weight": 2},
                    {"item": "MP回復薬（中）", "weight": 2},
                    {"item": "coins", "amount": [80, 130], "weight": 10}
                ]
            }
        ]
    },
    "6001-7000": {
        "enemies": [
            {
                "name": "カオスナイト",
                "hp": 190,
                "atk": 28,
                "def": 16,
                "attribute": "chaos",
                "weight": 35,
                "exp": 90,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "混沌の欠片", "weight": 20},
                    {"item": "カオスブレード", "weight": 1},
                    {"item": "混沌の鎧", "weight": 5},
                    {"item": "HP回復薬（中）", "weight": 5},
                    {"item": "MP回復薬（中）", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 2},
                    {"item": "MP回復薬（大）", "weight": 2},
                    {"item": "coins", "amount": [90, 120], "weight": 10}
                ]
            },
            {
                "name": "フェニックス",
                "hp": 225,
                "atk": 30,
                "def": 15,
                "attribute": "fire",
                "weight": 35,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "不死鳥の羽", "weight": 20},
                    {"item": "炎の剣", "weight": 5},
                    {"item": "再生の鎧", "weight": 5},
                    {"item": "HP回復薬（中）", "weight": 5},
                    {"item": "MP回復薬（中）", "weight": 5},
                    {"item": "coins", "amount": [100, 130], "weight": 10}
                ]
            },
            {
                "name": "デストロイヤー",
                "hp": 185,
                "atk": 32,
                "def": 14,
                "attribute": "none",
                "weight": 30,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "破壊の核", "weight": 20},
                    {"item": "滅びの剣", "weight": 5},
                    {"item": "終焉の盾", "weight": 5},
                    {"item": "HP回復薬（中）", "weight": 5},
                    {"item": "MP回復薬（中）", "weight": 5},
                    {"item": "coins", "amount": [100, 140], "weight": 10}
                ]
            }
        ]
    },
    "7001-8000": {
        "enemies": [
            {
                "name": "アビスウォーカー",
                "hp": 220,
                "atk": 34,
                "def": 19,
                "attribute": "dark",
                "weight": 35,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "深淵の結晶", "weight": 20},
                    {"item": "深淵の剣", "weight": 1},
                    {"item": "虚空の鎧", "weight": 5},
                    {"item": "HP回復薬（中）", "weight": 5},
                    {"item": "MP回復薬（中）", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 2},
                    {"item": "MP回復薬（大）", "weight": 2},
                    {"item": "coins", "amount": [110, 140], "weight": 10}
                ]
            },
            {
                "name": "エレメンタルロード",
                "hp": 240,
                "atk": 33,
                "def": 21,
                "attribute": "holy",
                "weight": 35,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "元素の核", "weight": 20},
                    {"item": "四元の剣", "weight": 5},
                    {"item": "精霊の盾", "weight": 5},
                    {"item": "HP回復薬（中）", "weight": 5},
                    {"item": "MP回復薬（中）", "weight": 5},
                    {"item": "coins", "amount": [110, 150], "weight": 10}
                ]
            },
            {
                "name": "タイタン",
                "hp": 300,
                "atk": 36,
                "def": 16,
                "attribute": "holy",
                "weight": 30,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "神の鉱石", "weight": 20},
                    {"item": "天の槌", "weight": 5},
                    {"item": "神の盾", "weight": 1},
                    {"item": "HP回復薬（中）", "weight": 5},
                    {"item": "MP回復薬（中）", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 2},
                    {"item": "MP回復薬（大）", "weight": 2},
                    {"item": "coins", "amount": [100, 160], "weight": 10}
                ]
            }
        ]
    },
    "8001-9000": {
        "enemies": [
            {
                "name": "ダークアーク",
                "hp": 260,
                "atk": 38,
                "def": 25,
                "attribute": "dark",
                "weight": 35,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "闇の聖典", "weight": 20},
                    {"item": "暗黒聖剣", "weight": 5},
                    {"item": "堕天の鎧", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 5},
                    {"item": "MP回復薬（大）", "weight": 5},
                    {"item": "coins", "amount": [120, 160], "weight": 10}
                ]
            },
            {
                "name": "リヴァイアサン",
                "hp": 300,
                "atk": 37,
                "def": 23,
                "attribute": "water",
                "weight": 35,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "海皇の鱗", "weight": 20},
                    {"item": "水神の槍", "weight": 5},
                    {"item": "深海の鎧", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 5},
                    {"item": "MP回復薬（大）", "weight": 5},
                    {"item": "coins", "amount": [110, 150], "weight": 10}
                ]
            },
            {
                "name": "ケルベロス",
                "hp": 350,
                "atk": 40,
                "def": 20,
                "attribute": "fire",
                "weight": 30,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "三首の牙", "weight": 20},
                    {"item": "獄炎の剣", "weight": 5},
                    {"item": "地獄門の鎧", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 5},
                    {"item": "MP回復薬（大）", "weight": 5},
                    {"item": "coins", "amount": [120, 170], "weight": 10}
                ]
            }
        ]
    },
    "9001-10000": {
        "enemies": [
            {
                "name": "ファントムキング",
                "hp": 400,
                "atk": 42,
                "def": 28,
                "attribute": "dark",
                "weight": 25,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "幻王の魂", "weight": 20},
                    {"item": "幻影剣", "weight": 5},
                    {"item": "幻王の鎧", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 4},
                    {"item": "MP回復薬（大）", "weight": 4},
                    {"item": "エリクサー", "weight": 2},
                    {"item": "coins", "amount": [130, 180], "weight": 10}
                ]
            },
            {
                "name": "ドラゴンロード",
                "hp": 340,
                "atk": 44,
                "def": 30,
                "attribute": "fire",
                "weight": 25,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "竜帝の心臓", "weight": 20},
                    {"item": "竜帝の剣", "weight": 2},
                    {"item": "竜帝の鎧", "weight": 2},
                    {"item": "HP回復薬（大）", "weight": 7},
                    {"item": "MP回復薬（大）", "weight": 7},
                    {"item": "エリクサー", "weight": 2},
                    {"item": "coins", "amount": [120, 190], "weight": 10}
                ]
            },
            {
                "name": "カオスゴッド",
                "hp": 360,
                "atk": 43,
                "def": 31,
                "attribute": "chaos",
                "weight": 25,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "神殺しの結晶", "weight": 20},
                    {"item": "混沌神剣", "weight": 5},
                    {"item": "創世の盾", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 4},
                    {"item": "MP回復薬（大）", "weight": 4},
                    {"item": "エリクサー", "weight": 2},
                    {"item": "coins", "amount": [140, 180], "weight": 10}
                ]
            },
            {
                "name": "デスエンペラー",
                "hp": 380,
                "atk": 45,
                "def": 30,
                "attribute": "dark",
                "weight": 25,
                "drops": [
                    {"item": "none", "weight": 50},
                    {"item": "死皇の冠", "weight": 20},
                    {"item": "死神の剣", "weight": 5},
                    {"item": "死帝の鎧", "weight": 5},
                    {"item": "HP回復薬（大）", "weight": 4},
                    {"item": "MP回復薬（大）", "weight": 4},
                    {"item": "エリクサー", "weight": 2},
                    {"item": "coins", "amount": [150, 200], "weight": 10}
                ]
            }
        ]
    }
}


def get_zone_from_distance(distance):
    if distance <= 1000:
        return "0-1000"
    elif distance <= 2000:
        return "1001-2000"
    elif distance <= 3000:
        return "2001-3000"
    elif distance <= 4000:
        return "3001-4000"
    elif distance <= 5000:
        return "4001-5000"
    elif distance <= 6000:
        return "5001-6000"
    elif distance <= 7000:
        return "6001-7000"
    elif distance <= 8000:
        return "7001-8000"
    elif distance <= 9000:
        return "8001-9000"
    elif distance <= 10000:
        return "9001-10000"
    else:
        return "9001-10000"


def get_random_enemy(distance):
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]

    weights = [enemy["weight"] for enemy in enemies]
    selected_enemy = random.choices(enemies, weights=weights, k=1)[0]

    return {
        "name": selected_enemy["name"],
        "hp": selected_enemy["hp"],
        "atk": selected_enemy["atk"],
        "def": selected_enemy["def"],
        "drops": selected_enemy["drops"],
        "attribute": selected_enemy.get("attribute", "none")
    }


def get_enemy_drop(enemy_name, distance):
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]

    enemy_data = None
    for enemy in enemies:
        if enemy["name"] == enemy_name:
            enemy_data = enemy
            break

    if not enemy_data or not enemy_data.get("drops"):
        return None

    drops = enemy_data["drops"]
    weights = [drop["weight"] for drop in drops]
    selected_drop = random.choices(drops, weights=weights, k=1)[0]

    if selected_drop["item"] == "coins":
        coin_amount = random.randint(selected_drop["amount"][0], selected_drop["amount"][1])
        return {"type": "coins", "amount": coin_amount}
    else:
        return {"type": "item", "name": selected_drop["item"]}


def get_treasure_box_equipment(distance):
    """宝箱から出る装備（武器・防具）のリストを返す"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]
    
    # そのゾーンの敵がドロップする装備を収集
    """レアドロップ品: 毒の短剣、魔法の杖、幽霊の布、竜の鱗、死の鎧、血の剣、暗黒の弓、巨人の鎧、カオスブレード、神の盾、深淵の剣"""
    equipment_list = []
    for enemy in enemies:
        drops = enemy.get("drops", [])
        for drop in drops:
            item_name = drop.get("item")
            if item_name and item_name != "none" and item_name != "coins" and item_name != "毒の短剣" and item_name != "魔法の杖" and item_name != "幽霊の布" and item_name != "竜の鱗" and item_name != "死の鎧" and item_name != "血の剣" and item_name != "暗黒の弓" and item_name != "巨人の鎧" and item_name != "カオスブレード" and item_name != "神の盾" and item_name != "深淵の剣":
                item_info = ITEMS_DATABASE.get(item_name)
                if item_info and item_info.get("type") in ["weapon", "armor"]:
                    if item_name not in equipment_list:
                        equipment_list.append(item_name)
    
    return equipment_list if equipment_list else ["木の剣"]


def get_treasure_box_weapons(distance):
    """宝箱から出る武器のみのリストを返す（階層に応じた武器のみ）"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]
    
    # そのゾーンの敵がドロップする武器のみを収集
    weapon_list = []
    for enemy in enemies:
        drops = enemy.get("drops", [])
        for drop in drops:
            item_name = drop.get("item")
            if item_name and item_name != "none" and item_name != "coins":
                item_info = ITEMS_DATABASE.get(item_name)
                if item_info and item_info.get("type") == "weapon":
                    if item_name not in weapon_list:
                        weapon_list.append(item_name)
    
    return weapon_list if weapon_list else ["木の剣"]


def get_item_info(item_name):
    return ITEMS_DATABASE.get(item_name, None)


def get_enemy_gold_drop(enemy_name, distance):
    """敵撃破時の確定ゴールドドロップ（ランダム範囲）を取得"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]
    
    # 敵データを検索
    for enemy in enemies:
        if enemy["name"] == enemy_name:
            # dropsリストからcoinsの範囲を取得
            drops = enemy.get("drops", [])
            for drop in drops:
                if drop.get("item") == "coins" and "amount" in drop:
                    min_gold = drop["amount"][0]
                    max_gold = drop["amount"][1]
                    return random.randint(min_gold, max_gold)
            # coinsが見つからない場合はデフォルト値
            return random.randint(5, 15)
    
    # 敵が見つからない場合はデフォルト値
    return random.randint(5, 15)


BOSS_DATA = {
    1: {
        "name": "スライムキング",
        "hp": 100,
        "atk": 10,
        "def": 5,
        "attribute": "none",
                "attribute": "none",
        "drops": [
            {"item": "王者の剣", "weight": 15},
            {"item": "スライムの王冠", "weight": 15},
            {"item": "HP回復薬（小）", "weight": 10},
            {"item": "HP回復薬（中）", "weight": 10},
            {"item": "MP回復薬（小）", "weight": 10},
            {"item": "MP回復薬（中）", "weight": 10},
            {"item": "coins", "amount": [100, 150], "weight": 30}
        ]
    },
    2: {
        "name": "デスロード",
        "hp": 150,
        "atk": 12,
        "def": 8,
        "attribute": "dark",
                "attribute": "dark",
        "drops": [
            {"item": "死神の鎌", "weight": 20},
            {"item": "不死の鎧", "weight": 20},
            {"item": "HP回復薬（中）", "weight": 15},
            {"item": "MP回復薬（中）", "weight": 15},
            {"item": "coins", "amount": [100, 200], "weight": 30}
        ]
    },
    3: {
        "name": "炎獄の魔竜", 
        "hp": 250,
        "atk": 16,
        "def": 10,
        "attribute": "fire",
                "attribute": "fire",
        "drops": [
            {"item": "竜の鱗", "weight": 15},
            {"item": "業火の剣", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 20},
            {"item": "MP回復薬（中）", "weight": 20},
            {"item": "coins", "amount": [150, 250], "weight": 30}
        ]
    },
    4: {
        "name": "影の王",
        "hp": 400,
        "atk": 20,
        "def": 12,
        "attribute": "dark",
                "attribute": "dark",
        "drops": [
            {"item": "影の短剣", "weight": 15},
            {"item": "死の鎧", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 20},
            {"item": "MP回復薬（中）", "weight": 20},
            {"item": "coins", "amount": [200, 300], "weight": 30}
        ]
    },
    5: {
        "name": "雷神",
        "hp": 600,
        "atk": 25,
        "def": 15,
        "attribute": "thunder",
                "attribute": "thunder",
        "drops": [
            {"item": "雷神の槍", "weight": 15},
            {"item": "祝福の盾", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 20},
            {"item": "MP回復薬（中）", "weight": 20},
            {"item": "coins", "amount": [250, 350], "weight": 30}
        ]
    },
    6: {
        "name": "氷の女王",
        "hp": 800,
        "atk": 30,
        "def": 18,
        "attribute": "ice",
                "attribute": "ice",
        "drops": [
            {"item": "氷結の杖", "weight": 15},
            {"item": "氷の鎧", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 15},
            {"item": "HP回復薬（大）", "weight": 5},
            {"item": "MP回復薬（中）", "weight": 15},
            {"item": "MP回復薬（大）", "weight": 5},
            {"item": "coins", "amount": [300, 400], "weight": 30}
        ]
    },
    7: {
        "name": "獄炎の巨人",
        "hp": 1000,
        "atk": 35,
        "def": 20,
        "attribute": "fire",
                "attribute": "fire",
        "drops": [
            {"item": "巨人の鎧", "weight": 15},
            {"item": "炎の大剣", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 10},
            {"item": "HP回復薬（大）", "weight": 10},
            {"item": "MP回復薬（中）", "weight": 10},
            {"item": "MP回復薬（大）", "weight": 10},
            {"item": "coins", "amount": [350, 450], "weight": 30}
        ]
    },
    8: {
        "name": "深淵の守護者",
        "hp": 1250,
        "atk": 40,
        "def": 24,
        "attribute": "dark",
                "attribute": "dark",
        "drops": [
            {"item": "深淵の剣", "weight": 15},
            {"item": "勇者の鎧", "weight": 15},
            {"item": "HP回復薬（中）", "weight": 5},
            {"item": "HP回復薬（大）", "weight": 15},
            {"item": "MP回復薬（中）", "weight": 5},
            {"item": "MP回復薬（大）", "weight": 15},
            {"item": "coins", "amount": [400, 500], "weight": 30}
        ]
    },
    9: {
        "name": "混沌の龍帝",
        "hp": 1500,
        "atk": 45,
        "def": 30,
        "attribute": "fire",
                "attribute": "fire",
        "drops": [
            {"item": "竜帝の剣", "weight": 15},
            {"item": "竜帝の鎧", "weight": 15},
            {"item": "HP回復薬（大）", "weight": 20},
            {"item": "MP回復薬（大）", "weight": 20},
            {"item": "coins", "amount": [450, 550], "weight": 30}
        ]
    },
    10: {
        "name": "終焉の魔王",
        "hp": 2000,
        "atk": 50,
        "def": 40,
        "attribute": "none",
                "attribute": "none",
        "drops": [
            {"item": "魔王の剣", "weight": 20},
            {"item": "魔王の鎧", "weight": 20},
            {"item": "魔王の指輪", "weight": 30},
            {"item": "coins", "amount": [500, 600], "weight": 30}
        ]
    }
}

SECRET_WEAPONS = [
    {"id": 1, "name": "シークレットソード#1", "attack": 100, "ability": "全能力+50%", "rarity": "伝説"},
    {"id": 2, "name": "シークレットソード#2", "attack": 95, "ability": "即死攻撃10%", "rarity": "伝説"},
    {"id": 3, "name": "シークレットソード#3", "attack": 90, "ability": "HP自動回復+30/ターン", "rarity": "伝説"},
    {"id": 4, "name": "シークレットソード#4", "attack": 105, "ability": "攻撃力+100%", "rarity": "神話"},
    {"id": 5, "name": "シークレットソード#5", "attack": 85, "ability": "防御無視攻撃", "rarity": "伝説"},
    {"id": 6, "name": "シークレットソード#6", "attack": 110, "ability": "全ステータス+80%", "rarity": "神話"},
    {"id": 7, "name": "シークレットソード#7", "attack": 88, "ability": "敵防御力無視", "rarity": "伝説"},
    {"id": 8, "name": "シークレットソード#8", "attack": 115, "ability": "クリティカル率100%", "rarity": "神話"},
    {"id": 9, "name": "シークレットソード#9", "attack": 92, "ability": "吸血50%", "rarity": "伝説"},
    {"id": 10, "name": "シークレットソード#10", "attack": 120, "ability": "真・無敵", "rarity": "超越"},
]

SPECIAL_EVENT_SHOP = [
    {"name": "魔力の剣", "type": "weapon", "price": 500, "attack": 25, "ability": "魔力+20%"},
    {"name": "聖なる盾", "type": "armor", "price": 450, "attack": 0, "defense": 18, "ability": "HP自動回復+5"},
    {"name": "破壊の斧", "type": "weapon", "price": 600, "attack": 30, "ability": "防御貫通30%"},
    {"name": "呪いの首輪", "type": "armor", "price": 300, "attack": 0, "defense": -10, "ability": "攻撃力+50%"},
    {"name": "狂戦士の鎧", "type": "armor", "price": 700, "attack": 0, "defense": -20, "ability": "攻撃力+100%"},
]

"""現在の素材27種類"""
MATERIAL_PRICES = {
    "蜘蛛の糸": 30,
    "腐った肉": 20,
    "悪魔の角": 40,
    "竜の牙": 60,
    "魔界の結晶": 60,
    "竜王の牙": 80,
    "古竜の心臓": 100,
    "闇の宝珠": 200,
    "地獄犬の牙": 100,
    "吸血鬼の牙": 90,
    "魔導書の欠片": 120,
    "闇の宝石": 120,
    "巨獣の皮": 130,
    "影の欠片": 150,
    "混沌の欠片": 150,
    "不死鳥の羽": 150,
    "破壊の核": 180,
    "深淵の結晶": 180,
    "元素の核": 190,
    "神の鉱石": 200,
    "闇の聖典": 200,
    "海皇の鱗": 210,
    "三首の牙": 220,
    "幻王の魂": 250,
    "竜帝の心臓": 270,
    "神殺しの結晶": 300,
    "死皇の冠": 1000
}

CRAFTING_RECIPES = {
    "蜘蛛の短剣": {
        "materials": {"蜘蛛の糸": 2},
        "result_type": "weapon",
        "attack": 7,
        "ability": "毒付与（10%の確率で追加ダメージ）",
        "description": "蜘蛛の糸から作られた短剣。強力な毒を持つ。"
    },
    "悪魔の剣": {
        "materials": {"悪魔の角": 2, "闇の宝珠": 1},
        "result_type": "weapon",
        "attack": 15,
        "ability": "闇属性（闇の敵に+60%ダメージ）",
        "description": "悪魔の角から鍛えられた剣。邪悪な力を宿す。"
    },
    "竜牙の剣": {
        "materials": {"竜の牙": 1, "悪魔の角": 2},
        "result_type": "weapon",
        "attack": 11,
        "ability": "竜の力（全ステータス+25%）",
        "description": "竜の牙から作られた伝説の剣。"
    },
    "闇の盾": {
        "materials": {"闇の宝珠": 1, "腐った肉": 3},
        "result_type": "armor",
        "defense": 15,
        "ability": "闇耐性+60%",
        "description": "闇の力が込められた盾。"
    },
    "蜘蛛の鎧": {
        "materials": {"蜘蛛の糸": 3, "悪魔の角": 1},
        "result_type": "armor",
        "defense": 11,
        "ability": "回避率+15%、毒耐性+50%",
        "description": "蜘蛛の糸で織られた鎧。軽くて頑丈。"
    },
    "竜鱗の鎧": {
        "materials": {"古龍の心臓": 1, "竜の牙": 2, "闇の宝珠": 1},
        "result_type": "armor",
        "defense": 13,
        "ability": "全属性耐性+30%、HP自動回復+5/ターン",
        "description": "竜の素材から作られた究極の鎧。"
    },
    "腐肉の兜": {
        "materials": {"腐った肉": 4},
        "result_type": "armor",
        "defense": 8,
        "ability": "毒無効、アンデッド特効+40%",
        "description": "腐った肉で作られた兜。アンデッドに強い。"
    }
}

def get_boss(stage):
    return BOSS_DATA.get(stage)

def should_spawn_boss(distance):
    if distance < 980:
        return False
    remainder = distance % 1000
    # 980-1020の範囲（1000の±20）でボス発生
    return remainder <= 20 or remainder >= 980

def get_boss_stage(distance):
    """ボス戦の正しいステージ番号を取得（範囲ベース）"""
    return round(distance / 1000)

def is_special_event_distance(distance):
    if distance < 480:
        return False
    remainder = distance % 500
    # 480-520の範囲（500の±20）で特殊イベント発生
    in_event_range = remainder <= 20 or remainder >= 480
    # ただしボス範囲は除外
    in_boss_range = should_spawn_boss(distance)
    return in_event_range and not in_boss_range

def get_special_event_stage(distance):
    """特殊イベントの正しいステージ番号を取得（範囲ベース）"""
    return round(distance / 500)

def get_random_secret_weapon():
    if random.random() < 0.001:
        return random.choice(SECRET_WEAPONS)
    return None

def parse_ability_bonuses(ability_text):
    """ability文字列から数値ボーナスを解析"""
    import re
    bonuses = {
        'hp_bonus': 0,
        'attack_percent': 0,
        'defense_percent': 0,
        'damage_reduction': 0,
        'hp_regen': 0,
        'lifesteal_percent': 0
    }

    if not ability_text or ability_text == "なし" or ability_text == "素材":
        return bonuses

    hp_match = re.search(r'HP\+(\d+)', ability_text)
    if hp_match:
        bonuses['hp_bonus'] = int(hp_match.group(1))

    atk_match = re.search(r'攻撃力\+(\d+)%', ability_text)
    if atk_match:
        bonuses['attack_percent'] = int(atk_match.group(1))

    def_match = re.search(r'防御力\+(\d+)%', ability_text)
    if def_match:
        bonuses['defense_percent'] = int(def_match.group(1))

    dmg_red_match = re.search(r'(?:全ダメージ|被ダメージ)-(\d+)%', ability_text)
    if dmg_red_match:
        bonuses['damage_reduction'] = int(dmg_red_match.group(1))

    regen_match = re.search(r'HP(?:自動)?回復\+(\d+)', ability_text)
    if regen_match:
        bonuses['hp_regen'] = int(regen_match.group(1))

    lifesteal_match = re.search(r'HP吸収(?:.*?)?(\d+)%', ability_text)
    if lifesteal_match:
        bonuses['lifesteal_percent'] = int(lifesteal_match.group(1))

    return bonuses

async def calculate_equipment_bonus(user_id):
    """装備中のアイテムから攻撃力・防御力ボーナスと特殊効果を計算"""
    import db
    equipped = await db.get_equipped_items(user_id)

    attack_bonus = 0
    defense_bonus = 0
    total_bonuses = {
        'hp_bonus': 0,
        'attack_percent': 0,
        'defense_percent': 0,
        'damage_reduction': 0,
        'hp_regen': 0,
        'lifesteal_percent': 0
    }

    weapon_ability = ""
    armor_ability = ""

    if equipped.get('weapon'):
        weapon_info = get_item_info(equipped['weapon'])
        if weapon_info:
            attack_bonus = weapon_info.get('attack', 0)
            weapon_ability = weapon_info.get('ability', '')
            weapon_bonuses = parse_ability_bonuses(weapon_ability)
            for key in total_bonuses:
                total_bonuses[key] += weapon_bonuses[key]

    if equipped.get('armor'):
        armor_info = get_item_info(equipped['armor'])
        if armor_info:
            defense_bonus = armor_info.get('defense', 0)
            armor_ability = armor_info.get('ability', '')
            armor_bonuses = parse_ability_bonuses(armor_ability)
            for key in total_bonuses:
                total_bonuses[key] += armor_bonuses[key]

    return {
        'attack_bonus': attack_bonus,
        'defense_bonus': defense_bonus,
        'weapon_ability': weapon_ability,
        'armor_ability': armor_ability,
        **total_bonuses
    }


STORY_TRIGGERS = [
    {"distance": 100, "story_id": "voice_1", "exact_match": False},
    {"distance": 777, "story_id": "lucky_777", "exact_match": True},
    {"distance": 250, "story_id": "story_250", "exact_match": False},
    {"distance": 750, "story_id": "story_750", "exact_match": False},
    {"distance": 1250, "story_id": "story_1250", "exact_match": False},
    {"distance": 1750, "story_id": "story_1750", "exact_match": False},
    {"distance": 2250, "story_id": "story_2250", "exact_match": False},
    {"distance": 2750, "story_id": "story_2750", "exact_match": False},
    {"distance": 3250, "story_id": "story_3250", "exact_match": False},
    {"distance": 3750, "story_id": "story_3750", "exact_match": False},
    {"distance": 4250, "story_id": "story_4250", "exact_match": False},
    {"distance": 4750, "story_id": "story_4750", "exact_match": False},
    {"distance": 5250, "story_id": "story_5250", "exact_match": False},
    {"distance": 5750, "story_id": "story_5750", "exact_match": False},
    {"distance": 6250, "story_id": "story_6250", "exact_match": False},
    {"distance": 6750, "story_id": "story_6750", "exact_match": False},
    {"distance": 7250, "story_id": "story_7250", "exact_match": False},
    {"distance": 7750, "story_id": "story_7750", "exact_match": False},
    {"distance": 8250, "story_id": "story_8250", "exact_match": False},
    {"distance": 8750, "story_id": "story_8750", "exact_match": False},
    {"distance": 9250, "story_id": "story_9250", "exact_match": False},
    {"distance": 9750, "story_id": "story_9750", "exact_match": False},
]


def get_enemy_type(enemy_name):
    """敵の名前からタイプを判定"""
    enemy_name_lower = enemy_name.lower()

    # アンデッド系
    undead_keywords = ["ゴースト", "スケルトン", "ゾンビ", "リッチ", "デスナイト", "デスロード", "デスエンペラー", "不死", "死神"]
    for keyword in undead_keywords:
        if keyword in enemy_name:
            return "undead"

    # ドラゴン系
    dragon_keywords = ["ドラゴン", "竜", "龍", "ワイバーン"]
    for keyword in dragon_keywords:
        if keyword in enemy_name:
            return "dragon"

    # 闇属性
    dark_keywords = ["ダーク", "闇", "シャドウ", "影", "黒騎士"]
    for keyword in dark_keywords:
        if keyword in enemy_name:
            return "dark"

    return "normal"


def apply_ability_effects(damage, ability_text, attacker_hp, target_type="normal"):
    """
    ability効果を適用してダメージと追加効果を計算

    Args:
        damage: 基本ダメージ
        ability_text: ability説明文
        attacker_hp: 攻撃者のHP（HP吸収用）
        target_type: 対象タイプ（"normal", "undead", "dragon"など）

    Returns:
        dict: {
            "damage": 最終ダメージ,
            "lifesteal": HP吸収量,
            "burn": 燃焼ダメージ（追加効果）,
            "poison": 毒ダメージ（追加効果）,
            "instant_kill": 即死判定,
            "effect_text": 効果説明テキスト
        }
    """
    import re

    result = {
        "damage": damage,
        "lifesteal": 0,
        "burn": 0,
        "poison": 0,
        "instant_kill": False,
        "effect_text": ""
    }

    if not ability_text or ability_text == "なし" or ability_text == "素材":
        return result

    # 炎ダメージ（追加で炎ダメージ+X）
    fire_match = re.search(r'炎ダメージ\+(\d+)', ability_text)
    if fire_match:
        fire_damage = int(fire_match.group(1))
        result["damage"] += fire_damage
        result["effect_text"] += f"🔥炎+{fire_damage} "

    # 燃焼状態（攻撃時X%で敵を燃焼）
    burn_match = re.search(r'攻撃時(\d+)%で(?:敵を)?燃焼.*?ダメージ(\d+)', ability_text)
    if burn_match:
        burn_chance = int(burn_match.group(1))
        burn_damage = int(burn_match.group(2))
        if random.randint(1, 100) <= burn_chance:
            result["burn"] = burn_damage
            result["effect_text"] += f"🔥燃焼付与! "

    # 毒付与
    poison_match = re.search(r'毒付与.*?(\d+)%', ability_text)
    if poison_match:
        poison_chance = int(poison_match.group(1))
        if random.randint(1, 100) <= poison_chance:
            result["poison"] = 10
            result["effect_text"] += f"☠️毒付与! "

    # HP吸収
    lifesteal_match = re.search(r'HP吸収.*?(\d+)%', ability_text)
    if lifesteal_match:
        lifesteal_percent = int(lifesteal_match.group(1))
        result["lifesteal"] = int(damage * lifesteal_percent / 100)
        result["effect_text"] += f"💉HP吸収{result['lifesteal']} "

    # 即死効果
    instant_kill_match = re.search(r'攻撃時(\d+)%で即死', ability_text)
    if instant_kill_match:
        kill_chance = int(instant_kill_match.group(1))
        if random.randint(1, 100) <= kill_chance:
            result["instant_kill"] = True
            result["effect_text"] += f"💀即死発動! "

    # アンデッド特効
    if target_type == "undead" and "アンデッド特効" in ability_text:
        undead_match = re.search(r'アンデッド.*?\+(\d+)%', ability_text)
        if undead_match:
            bonus_percent = int(undead_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"⚰️特効+{bonus_damage} "

    # ドラゴン特効
    if target_type == "dragon" and "ドラゴン特効" in ability_text:
        dragon_match = re.search(r'ドラゴン.*?\+(\d+)%', ability_text)
        if dragon_match:
            bonus_percent = int(dragon_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"🐉特効+{bonus_damage} "

    # 闇属性特効
    if target_type == "dark" and "闇" in ability_text:
        dark_match = re.search(r'闇.*?\+(\d+)%', ability_text)
        if dark_match:
            bonus_percent = int(dark_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"🌑特効+{bonus_damage} "

    # クリティカル率アップ
    if "クリティカル率" in ability_text:
        crit_match = re.search(r'クリティカル率\+(\d+)%', ability_text)
        if crit_match:
            crit_chance = int(crit_match.group(1))
            if random.randint(1, 100) <= crit_chance:
                crit_damage = int(damage * 0.5)
                result["damage"] += crit_damage
                result["effect_text"] += f"💥クリティカル+{crit_damage} "

    # クリティカル時ダメージ3倍
    if "クリティカル時ダメージ3倍" in ability_text:
        if random.randint(1, 100) <= 20:
            triple_damage = int(damage * 2)
            result["damage"] += triple_damage
            result["effect_text"] += f"💥💥クリティカル3倍+{triple_damage} "

    # 凍結効果（攻撃時X%で敵を凍結）
    freeze_match = re.search(r'攻撃時(\d+)%で(?:敵を)?凍結', ability_text)
    if freeze_match:
        freeze_chance = int(freeze_match.group(1))
        if random.randint(1, 100) <= freeze_chance:
            result["freeze"] = True
            result["effect_text"] += "❄️凍結! "

    # 麻痺効果（攻撃時X%で敵を麻痺）
    paralyze_match = re.search(r'攻撃時(\d+)%で(?:敵を)?麻痺', ability_text)
    if paralyze_match:
        paralyze_chance = int(paralyze_match.group(1))
        if random.randint(1, 100) <= paralyze_chance:
            result["paralyze"] = True
            result["effect_text"] += "⚡麻痺! "

    # 分身攻撃（2回攻撃）
    if "分身攻撃" in ability_text and "2回攻撃" in ability_text:
        result["double_attack"] = True
        result["damage"] = int(damage * 2)
        result["effect_text"] += f"👥分身攻撃×2! "

    # 3回攻撃
    if "3回攻撃" in ability_text:
        result["triple_attack"] = True
        result["damage"] = int(damage * 3)
        result["effect_text"] += f"👥👥3連撃! "

    # 防御力無視
    if "防御無視" in ability_text or "防御力無視" in ability_text:
        if "攻撃時" in ability_text:
            ignore_match = re.search(r'攻撃時(\d+)%で敵の防御力無視', ability_text)
            if ignore_match:
                ignore_chance = int(ignore_match.group(1))
                if random.randint(1, 100) <= ignore_chance:
                    result["defense_ignore"] = True
                    result["effect_text"] += "🔓防御無視! "
        else:
            result["defense_ignore"] = True
            result["effect_text"] += "🔓防御無視! "

    # MP吸収
    mp_drain_match = re.search(r'(?:攻撃時)?敵のMP-(\d+)', ability_text)
    if mp_drain_match:
        mp_drain = int(mp_drain_match.group(1))
        result["mp_drain"] = mp_drain
        result["effect_text"] += f"🔵MP吸収{mp_drain} "

    # MP吸収（パーセント版）
    mp_absorb_match = re.search(r'MP吸収(\d+)%', ability_text)
    if mp_absorb_match:
        mp_percent = int(mp_absorb_match.group(1))
        result["mp_absorb_percent"] = mp_percent
        result["effect_text"] += f"🔵MP吸収{mp_percent}% "

    # 敵の最大HP-X%
    max_hp_dmg_match = re.search(r'敵の最大HP-(\d+)%', ability_text)
    if max_hp_dmg_match:
        max_hp_percent = int(max_hp_dmg_match.group(1))
        if random.randint(1, 100) <= 20:
            result["max_hp_damage"] = max_hp_percent
            result["effect_text"] += f"💀最大HP-{max_hp_percent}%! "

    # アンデッド召喚
    if "アンデッド召喚" in ability_text:
        summon_match = re.search(r'攻撃時(\d+)%でアンデッド召喚.*?HP(\d+)回復', ability_text)
        if summon_match:
            summon_chance = int(summon_match.group(1))
            heal_amount = int(summon_match.group(2))
            if random.randint(1, 100) <= summon_chance:
                result["summon_heal"] = heal_amount
                result["effect_text"] += f"💀召喚HP+{heal_amount} "

    # 竜の咆哮（敵怯み）
    if "竜の咆哮" in ability_text:
        if random.randint(1, 100) <= 30:
            result["enemy_flinch"] = True
            result["effect_text"] += "🐉咆哮(怯み)! "

    # 呪い（攻撃時にHP-5、ダメージ+50%）
    if "呪い" in ability_text and "攻撃時にHP-" in ability_text:
        curse_match = re.search(r'HP-(\d+).*?ダメージ\+(\d+)%', ability_text)
        if curse_match:
            hp_loss = int(curse_match.group(1))
            dmg_bonus = int(curse_match.group(2))
            bonus_damage = int(damage * dmg_bonus / 100)
            result["damage"] += bonus_damage
            result["self_damage"] = hp_loss
            result["effect_text"] += f"😈呪い+{bonus_damage}(自傷-{hp_loss}) "

    # ランダム効果（燃焼・毒・防御無視・分身攻撃のいずれか）
    if "ランダム効果" in ability_text or "毎攻撃ランダム追加効果" in ability_text:
        random_effect = random.choice(["burn", "poison", "defense_ignore", "double_attack"])
        if random_effect == "burn":
            result["burn"] = 15
            result["effect_text"] += "🔥ランダム:燃焼! "
        elif random_effect == "poison":
            result["poison"] = 15
            result["effect_text"] += "☠️ランダム:毒! "
        elif random_effect == "defense_ignore":
            result["defense_ignore"] = True
            result["effect_text"] += "🔓防御無視! "
        elif random_effect == "double_attack":
            if random.randint(1, 100) <= 40:
                result["double_attack"] = True
                result["damage"] = int(damage * 2)
                result["effect_text"] += f"👥分身攻撃×2! "

    # ボス特効
    if "ボスに特効" in ability_text or "ボス特効" in ability_text:
        boss_match = re.search(r'ボス(?:に)?特効\+(\d+)%', ability_text)
        if boss_match and target_type == "boss":
            bonus_percent = int(boss_match.group(1))
            bonus_damage = int(damage * bonus_percent / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"👑ボス特効+{bonus_damage} "

    # 全ステータス+X%
    if "全ステータス" in ability_text:
        stats_match = re.search(r'全ステータス\+(\d+)%', ability_text)
        if stats_match:
            stats_bonus = int(stats_match.group(1))
            bonus_damage = int(damage * stats_bonus / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"✨全ステ+{stats_bonus}% "

    # 攻撃力+X%（デバフ防具）
    if "攻撃力+" in ability_text and "%" in ability_text:
        atk_match = re.search(r'攻撃力\+(\d+)%', ability_text)
        if atk_match:
            atk_bonus = int(atk_match.group(1))
            bonus_damage = int(damage * atk_bonus / 100)
            result["damage"] += bonus_damage
            result["effect_text"] += f"⚔️攻撃+{atk_bonus}% "

    # 初期化されていないフィールドを追加
    if "freeze" not in result:
        result["freeze"] = False
    if "double_attack" not in result:
        result["double_attack"] = False
    if "triple_attack" not in result:
        result["triple_attack"] = False
    if "defense_ignore" not in result:
        result["defense_ignore"] = False
    if "mp_drain" not in result:
        result["mp_drain"] = 0
    if "mp_absorb_percent" not in result:
        result["mp_absorb_percent"] = 0
    if "max_hp_damage" not in result:
        result["max_hp_damage"] = 0
    if "summon_heal" not in result:
        result["summon_heal"] = 0
    if "enemy_flinch" not in result:
        result["enemy_flinch"] = False
    if "self_damage" not in result:
        result["self_damage"] = 0
    if "paralyze" not in result:
        result["paralyze"] = False

    return result


def apply_armor_effects(incoming_damage, armor_ability, defender_hp, max_hp, attacker_damage=0, attack_attribute="none"):
    """
    防具のアビリティ効果を適用

    Args:
        incoming_damage: 受けるダメージ
        armor_ability: 防具のアビリティ文字列
        defender_hp: 防御者の現在HP
        max_hp: 防御者の最大HP
        attacker_damage: 攻撃者が与えたダメージ（反撃用）
        attack_attribute: 攻撃の属性 (none, fire, ice, thunder, dark, water, etc.)

    Returns:
        dict: {
            "damage": 最終ダメージ,
            "evaded": 回避したか,
            "counter_damage": 反撃ダメージ,
            "reflect_damage": 反射ダメージ,
            "hp_regen": HP回復量,
            "revived": 蘇生したか,
            "effect_text": 効果説明テキスト
        }
    """
    import re

    result = {
        "damage": incoming_damage,
        "evaded": False,
        "counter_damage": 0,
        "reflect_damage": 0,
        "hp_regen": 0,
        "revived": False,
        "effect_text": ""
    }

    if not armor_ability or armor_ability == "なし" or armor_ability == "素材":
        return result

    # 回避率
    evasion_match = re.search(r'回避率\+(\d+)%', armor_ability)
    if evasion_match:
        evasion_chance = int(evasion_match.group(1))
        if random.randint(1, 100) <= evasion_chance:
            result["evaded"] = True
            result["damage"] = 0
            result["effect_text"] += "💨回避! "
            return result

    # 幻影分身（被攻撃時X%で回避）
    phantom_match = re.search(r'被攻撃時(\d+)%で(?:完全)?回避', armor_ability)
    if phantom_match:
        phantom_chance = int(phantom_match.group(1))
        if random.randint(1, 100) <= phantom_chance:
            result["evaded"] = True
            result["damage"] = 0
            result["effect_text"] += "👻幻影回避! "
            return result

    # ダメージ軽減系
    if "全ダメージ" in armor_ability or "被ダメージ" in armor_ability:
        dmg_red_match = re.search(r'(?:全ダメージ|被ダメージ)-(\d+)%', armor_ability)
        if dmg_red_match:
            reduction = int(dmg_red_match.group(1))
            reduced_amount = int(incoming_damage * reduction / 100)
            result["damage"] -= reduced_amount
            result["effect_text"] += f"🛡️軽減-{reduced_amount} "

    # 物理ダメージ軽減
    if "物理ダメージ" in armor_ability:
        phys_match = re.search(r'物理ダメージ(?:軽減)?-(\d+)%', armor_ability)
        if phys_match:
            reduction = int(phys_match.group(1))
            reduced_amount = int(incoming_damage * reduction / 100)
            result["damage"] -= reduced_amount
            result["effect_text"] += f"🛡️物理軽減-{reduced_amount} "

    # 属性耐性（攻撃属性に応じて適用）
    if attack_attribute == "fire":
        if "炎耐性" in armor_ability or "炎無効" in armor_ability:
            if "無効" in armor_ability:
                result["damage"] = 0
                result["effect_text"] += "🔥炎無効! "
            else:
                fire_res_match = re.search(r'炎耐性\+(\d+)%', armor_ability)
                if fire_res_match:
                    resistance = int(fire_res_match.group(1))
                    reduced = int(incoming_damage * resistance / 100)
                    result["damage"] -= reduced
                    result["effect_text"] += f"🔥炎耐性-{reduced} "

    if attack_attribute == "dark":
        if "闇耐性" in armor_ability:
            dark_res_match = re.search(r'闇耐性\+(\d+)%', armor_ability)
            if dark_res_match:
                resistance = int(dark_res_match.group(1))
                reduced = int(incoming_damage * resistance / 100)
                result["damage"] -= reduced
                result["effect_text"] += f"🌑闇耐性-{reduced} "

    if attack_attribute in ["ice", "water"]:
        if "水・氷耐性" in armor_ability or "水耐性" in armor_ability or "氷耐性" in armor_ability:
            water_match = re.search(r'(?:水・氷耐性|水耐性|氷耐性)(\d+)%', armor_ability)
            if water_match:
                resistance = int(water_match.group(1))
                reduced = int(incoming_damage * resistance / 100)
                result["damage"] -= reduced
                result["effect_text"] += f"❄️水氷耐性-{reduced} "

    # 全属性耐性は常に適用（属性攻撃のみ）
    if attack_attribute != "none" and "全属性耐性" in armor_ability:
        all_res_match = re.search(r'全属性耐性\+(\d+)%', armor_ability)
        if all_res_match:
            resistance = int(all_res_match.group(1))
            reduced = int(incoming_damage * resistance / 100)
            result["damage"] -= reduced
            result["effect_text"] += f"✨全耐性-{reduced} "

    # ダメージ下限を0に
    result["damage"] = max(0, result["damage"])

    # 反撃（被ダメージのX%を返す）
    if "反撃" in armor_ability:
        counter_match = re.search(r'被ダメージの(\d+)%を返す', armor_ability)
        if counter_match:
            counter_percent = int(counter_match.group(1))
            result["counter_damage"] = int(incoming_damage * counter_percent / 100)
            result["effect_text"] += f"⚔️反撃{result['counter_damage']} "

    # 被攻撃時反撃ダメージ
    if "被攻撃時" in armor_ability and "反撃ダメージ" in armor_ability:
        reflect_match = re.search(r'反撃ダメージ(\d+)', armor_ability)
        if reflect_match:
            base_reflect = int(reflect_match.group(1))
            reflect_chance_match = re.search(r'被攻撃時(\d+)%', armor_ability)
            if reflect_chance_match:
                reflect_chance = int(reflect_chance_match.group(1))
                if random.randint(1, 100) <= reflect_chance:
                    result["reflect_damage"] = base_reflect
                    result["effect_text"] += f"⚡反撃{base_reflect} "

    # 反射ダメージ
    if "反射ダメージ" in armor_ability:
        reflect_dmg_match = re.search(r'反射ダメージ(\d+)', armor_ability)
        if reflect_dmg_match:
            result["reflect_damage"] = int(reflect_dmg_match.group(1))
            result["effect_text"] += f"⚡反射{result['reflect_damage']} "

    # HP自動回復
    hp_regen_match = re.search(r'HP(?:自動)?回復\+(\d+)', armor_ability)
    if hp_regen_match:
        result["hp_regen"] = int(hp_regen_match.group(1))
        result["effect_text"] += f"💚回復+{result['hp_regen']} "

    # 瀕死時HP回復
    if "瀕死時" in armor_ability and defender_hp <= max_hp * 0.3:
        critical_heal_match = re.search(r'瀕死時HP\+(\d+)', armor_ability)
        if critical_heal_match:
            critical_heal = int(critical_heal_match.group(1))
            result["hp_regen"] += critical_heal
            result["effect_text"] += f"💚瀕死回復+{critical_heal} "

    # HP30%以下で防御力1.5倍（神の加護）
    if "神の加護" in armor_ability and defender_hp <= max_hp * 0.3:
        if "防御力1.5倍" in armor_ability:
            halved = int(result["damage"] / 1.5)
            result["damage"] = halved
            result["effect_text"] += "✨神の加護(防御1.5倍)! "

    # 精霊加護（致死ダメージ時1回生存）
    if "精霊加護" in armor_ability and result["damage"] >= defender_hp:
        if "致死ダメージ時1回生存" in armor_ability:
            result["damage"] = defender_hp - 1
            result["revived"] = True
            result["effect_text"] += "🌟精霊加護(生存)! "

    # 竜鱗の守護（致死ダメージ無効1回）
    if "竜鱗の守護" in armor_ability and result["damage"] >= defender_hp:
        if "致死ダメージ無効" in armor_ability:
            result["damage"] = 0
            result["evaded"] = True
            result["effect_text"] += "🐉竜鱗の守護! "

    return result


async def check_story_trigger(previous_distance, current_distance, user_id):
    """
    ストーリートリガーをチェック

    Args:
        previous_distance: 移動前の距離
        current_distance: 移動後の距離
        user_id: ユーザーID

    Returns:
        トリガーされたストーリーID、またはNone
    """
    import db
    from story import STORY_DATA

    player = await db.get_player(user_id)
    if not player:
        return None

    loop_count = player.get("loop_count", 0)

    for trigger in STORY_TRIGGERS:
        trigger_distance = trigger["distance"]
        story_id = trigger["story_id"]
        exact_match = trigger.get("exact_match", False)

        triggered = False
        if exact_match:
            triggered = (current_distance == trigger_distance)
        else:
            triggered = (previous_distance < trigger_distance <= current_distance)

        if triggered:
            story = STORY_DATA.get(story_id)
            if not story:
                continue

            loop_requirement = story.get("loop_requirement")

            if loop_requirement is None:
                return story_id
            elif loop_requirement == 0 and loop_count == 0:
                if not await db.get_story_flag(user_id, story_id):
                    return story_id
            elif loop_requirement > 0 and loop_count >= loop_requirement:
                if not await db.get_story_flag(user_id, story_id):
                    return story_id

    return None

# スキルデータベース
SKILLS_DATABASE = {
    "体当たり": {
        "id": "体当たり",
        "name": "体当たり",
        "type": "attack",
        "mp_cost": 10,
        "power": 1.2,
        "description": "基本的な体当たり攻撃。威力1.2倍。",
        "unlock_distance": 0
    },
    "小火球": {
        "id": "小火球",
        "name": "小火球",
        "type": "attack",
        "mp_cost": 15,
        "power": 1.5,
        "description": "小さな火球を放つ。威力1.5倍。",
        "unlock_distance": 1000
    },
    "軽傷治癒": {
        "id": "軽傷治癒",
        "name": "軽傷治癒",
        "type": "heal",
        "mp_cost": 20,
        "heal_amount": 40,
        "description": "軽い傷を癒す。HP40回復。",
        "unlock_distance": 2000
    },
    "強攻撃": {
        "id": "強攻撃",
        "name": "強攻撃",
        "type": "attack",
        "mp_cost": 25,
        "power": 1.8,
        "description": "強力な一撃。威力1.8倍。",
        "unlock_distance": 3000
    },
    "ファイアボール": {
        "id": "ファイアボール",
        "name": "ファイアボール",
        "type": "attack",
        "mp_cost": 30,
        "power": 2.2,
        "description": "炎の球を放つ。威力2.2倍。",
        "unlock_distance": 4000
    },
    "中治癒": {
        "id": "中治癒",
        "name": "中治癒",
        "type": "heal",
        "mp_cost": 35,
        "heal_amount": 80,
        "description": "傷を治す。HP80回復。",
        "unlock_distance": 5000
    },
    "猛攻撃": {
        "id": "猛攻撃",
        "name": "猛攻撃",
        "type": "attack",
        "mp_cost": 40,
        "power": 2.5,
        "description": "猛烈な攻撃。威力2.5倍。",
        "unlock_distance": 6000
    },
    "爆炎": {
        "id": "爆炎",
        "name": "爆炎",
        "type": "attack",
        "mp_cost": 45,
        "power": 3.0,
        "description": "爆発する炎。威力3.0倍。",
        "unlock_distance": 7000
    },
    "完全治癒": {
        "id": "完全治癒",
        "name": "完全治癒",
        "type": "heal",
        "mp_cost": 50,
        "heal_amount": 150,
        "description": "完全に傷を癒す。HP150回復。",
        "unlock_distance": 8000
    },
    "神速の一閃": {
        "id": "神速の一閃",
        "name": "神速の一閃",
        "type": "attack",
        "mp_cost": 55,
        "power": 3.5,
        "description": "神速の斬撃。威力3.5倍。",
        "unlock_distance": 9000
    },
    "究極魔法": {
        "id": "究極魔法",
        "name": "究極魔法",
        "type": "attack",
        "mp_cost": 60,
        "power": 4.0,
        "description": "究極の魔法攻撃。威力4.0倍。",
        "unlock_distance": 10000
    }
}

def get_skill_info(skill_id):
    """スキル情報を取得"""
    return SKILLS_DATABASE.get(skill_id, None)

def get_exp_from_enemy(enemy_name, distance):
    """敵からのEXP獲得量を取得"""
    zone = get_zone_from_distance(distance)
    enemies = ENEMY_ZONES[zone]["enemies"]

    for enemy in enemies:
        if enemy["name"] == enemy_name:
            return enemy.get("exp", 10)

    return 10

def categorize_drops_by_zone(zones, items_db):
    """
    ENEMY_ZONESのドロップアイテムを、アイテムタイプ別に分類し、階層ごとに集計する。
    """
    drops_by_zone_and_type = {}

    for zone_key, zone_data in zones.items():
        "ゾーンごとに結果を初期化"
        drops_by_zone_and_type[zone_key] = {
            "weapon": set(),
            "armor": set(),
            "potion": set(),
            "material": set(),
            "other": set() # noneやcoinsなど、タイプがないものを格納
        }

        "ENEMIESがリストであることを前提"
        for enemy in zone_data.get("enemies", []): 
            "dropsがリストであることを前提"
            for drop in enemy.get("drops", []):
                item_name = drop.get("item")

                "'none' または 'coins' のような特殊ドロップはスキップまたは'other'に追加"
                if item_name == "none" or item_name == "coins":
                    if item_name == "coins":
                        # 'none'は無視、'coins'は'other'に記録
                        drops_by_zone_and_type[zone_key]["other"].add(item_name)
                    continue

                "ITEMS_DATABASEからアイテムタイプを取得"
                item_info = items_db.get(item_name)

                if item_info:
                    item_type = item_info.get("type")
                    if item_type in drops_by_zone_and_type[zone_key]:
                        "該当するタイプセットにアイテム名を追加"
                        drops_by_zone_and_type[zone_key][item_type].add(item_name)
                    else:
                        "定義されていないタイプは 'other' に追加"
                        drops_by_zone_and_type[zone_key]["other"].add(item_name)
                else:
                    "ITEMS_DATABASEに見つからない場合は 'other' に追加"
                    drops_by_zone_and_type[zone_key]["other"].add(item_name)

        "setをリストに変換して、ソートする"
        for item_type in drops_by_zone_and_type[zone_key]:
            drops_by_zone_and_type[zone_key][item_type] = sorted(list(drops_by_zone_and_type[zone_key][item_type]))

    return drops_by_zone_and_type

"階層ごとにタイプ別ドロップアイテムを格納する新しい変数"
"ENEMY_ZONESとITEMS_DATABASEが定義された後に実行されます。"
DROPS_BY_ZONE_AND_TYPE = categorize_drops_by_zone(ENEMY_ZONES, ITEMS_DATABASE)

"0-1000mのエリアでドロップする武器のリストを取得"
weapon_drops_1 = DROPS_BY_ZONE_AND_TYPE["0-1000"]["weapon"]
"['木の剣', '石の剣', '毒の短剣', '鉄の剣']"

"0-1000mのエリアでドロップする防具のリストを取得"
armor_drops_1 = DROPS_BY_ZONE_AND_TYPE["0-1000"]["armor"]
"['木の盾', '石の盾', '鉄の盾']"

"1001-2000mのエリアでドロップする武器のリストを取得"
weapon_drops_2 = DROPS_BY_ZONE_AND_TYPE["1001-2000"]["weapon"]
"['骨の剣', '呪いの剣', '魔法の杖']"

"1001-2000mのエリアでドロップする防具のリストを取得"
armor_drops_2 = DROPS_BY_ZONE_AND_TYPE["1001-2000"]["armor"]
"['骨の盾', '死者の兜', '不死の鎧','幽霊の布']"

"2001-3000mのエリアでドロップする武器のリストを取得"
weapon_drops_3 = DROPS_BY_ZONE_AND_TYPE["2001-3000"]["weapon"]
"['炎の大剣', 'ドラゴンソード', '黒騎士の剣']"

"2001-3000mのエリアでドロップする防具のリストを取得"
armor_drops_3 = DROPS_BY_ZONE_AND_TYPE["2001-3000"]["armor"]
"['地獄の鎧', '龍の鱗', '黒騎士の盾','黒騎士の鎧']"

"3001-4000mのエリアでドロップする武器のリストを取得"
weapon_drops_4 = DROPS_BY_ZONE_AND_TYPE["3001-4000"]["weapon"]
"['炎獄の剣', '死神の鎌']"

"3001-4000mのエリアでドロップする防具のリストを取得"
armor_drops_4 = DROPS_BY_ZONE_AND_TYPE["3001-4000"]["armor"]
"['魔王の盾', '龍鱗の鎧', '冥界の盾','死の鎧']"

"4001-5000mのエリアでドロップする武器のリストを取得"
weapon_drops_5 = DROPS_BY_ZONE_AND_TYPE["4001-5000"]["weapon"]
"['業火の剣', '血の剣', '死霊の杖']"

"4001-5000mのエリアでドロップする防具のリストを取得"
armor_drops_5 = DROPS_BY_ZONE_AND_TYPE["4001-5000"]["armor"]
"['炎の鎧', '夜の外套', '不死王の兜']"

"5001-6000mのエリアでドロップする武器のリストを取得"
weapon_drops_6 = DROPS_BY_ZONE_AND_TYPE["5001-6000"]["weapon"]
"['影の短剣', '暗黒の弓', '破壊の斧', '虚無の剣']"

"5001-6000mのエリアでドロップする防具のリストを取得"
armor_drops_6 = DROPS_BY_ZONE_AND_TYPE["5001-6000"]["armor"]
"['巨人の鎧', '幻影の鎧']"

"6001-7000mのエリアでドロップする武器のリストを取得"
weapon_drops_7 = DROPS_BY_ZONE_AND_TYPE["6001-7000"]["weapon"]
"['カオスブレード', '炎の剣', '滅びの剣']"

"6001-7000mのエリアでドロップする防具のリストを取得"
armor_drops_7 = DROPS_BY_ZONE_AND_TYPE["6001-7000"]["armor"]
"['混沌の鎧', '再生の鎧', '終焉の盾']"

"7001-8000mのエリアでドロップする武器のリストを取得"
weapon_drops_8 = DROPS_BY_ZONE_AND_TYPE["7001-8000"]["weapon"]
"['深淵の剣', '四元の剣', '天の槌']"

"7001-8000mのエリアでドロップする防具のリストを取得"
armor_drops_8 = DROPS_BY_ZONE_AND_TYPE["7001-8000"]["armor"]
"['虚空の鎧', '精霊の盾', '神の盾']"

"8001-9000mのエリアでドロップする武器のリストを取得"
weapon_drops_9 = DROPS_BY_ZONE_AND_TYPE["8001-9000"]["weapon"]
"['暗黒聖剣', '水神の槍', '獄炎の剣']"

"8001-9000mのエリアでドロップする防具のリストを取得"
armor_drops_9 = DROPS_BY_ZONE_AND_TYPE["8001-9000"]["armor"]
"['堕天の鎧', '深海の鎧', '地獄門の鎧']"

"9001-10000mのエリアでドロップする武器のリストを取得"
weapon_drops_10 = DROPS_BY_ZONE_AND_TYPE["9001-10000"]["weapon"]
"['幻影剣', '竜帝剣', '混沌神剣', '死神大鎌']"

"9001-10000mのエリアでドロップする防具のリストを取得"
armor_drops_10 = DROPS_BY_ZONE_AND_TYPE["9001-10000"]["armor"]
"['幻王の鎧', '竜帝の鎧', '創世の盾', '死帝の鎧']"


# ========================================
# 敵の行動AIシステム
# ========================================

ENEMY_AI_PATTERNS = {
    "aggressive": {
        "attack": 70,
        "skill": 20,
        "wait": 5,
        "flee": 5
    },
    "balanced": {
        "attack": 50,
        "skill": 30,
        "wait": 15,
        "flee": 5
    },
    "defensive": {
        "attack": 30,
        "skill": 20,
        "wait": 40,
        "flee": 10
    },
    "coward": {
        "attack": 20,
        "skill": 10,
        "wait": 30,
        "flee": 40
    },
    "boss": {
        "attack": 40,
        "skill": 50,
        "wait": 10,
        "flee": 0
    }
}

ENEMY_SKILLS = {
    "スライム": [
        {"name": "体当たり", "power": 1.2, "description": "体当たり攻撃"},
        {"name": "溶解液", "power": 1.5, "description": "防御力-20%"}
    ],
    "バット": [
        {"name": "急降下", "power": 1.5, "description": "急降下攻撃"},
        {"name": "超音波", "power": 1.3, "description": "混乱付与"}
    ],
    "ゴブリン": [
        {"name": "連続攻撃", "power": 1.8, "description": "2回攻撃"},
        {"name": "投石", "power": 1.4, "description": "遠距離攻撃"}
    ],
    "スパイダー": [
        {"name": "毒針", "power": 1.3, "description": "毒付与（3ターン、5ダメージ）"},
        {"name": "糸縛り", "power": 1.0, "description": "行動不能1ターン"}
    ],
    "ゾンビ": [
        {"name": "噛みつき", "power": 1.4, "description": "HP吸収"},
        {"name": "腐敗ガス", "power": 1.2, "description": "毒付与"}
    ],
    "スケルトン": [
        {"name": "骨の剣", "power": 1.6, "description": "斬撃攻撃"},
        {"name": "呪いの眼光", "power": 1.3, "description": "攻撃力-20%"}
    ],
    "ゴールデンスライム": [
        {"name": "黄金の輝き", "power": 2.0, "description": "全能力+50%"},
        {"name": "財宝の守り", "power": 1.0, "description": "防御力+100%"}
    ],
    "ミミック": [
        {"name": "噛み砕き", "power": 3.0, "description": "強力な噛みつき"},
        {"name": "丸呑み", "power": 5.0, "description": "即死攻撃（50%確率）"}
    ]
}

def get_enemy_action(enemy_name: str, ai_pattern: str = "balanced"):
    """敵の行動を決定"""
    pattern = ENEMY_AI_PATTERNS.get(ai_pattern, ENEMY_AI_PATTERNS["balanced"])
    
    actions = ["attack", "skill", "wait", "flee"]
    weights = [pattern["attack"], pattern["skill"], pattern["wait"], pattern["flee"]]
    
    action = random.choices(actions, weights=weights, k=1)[0]
    
    if action == "skill":
        skills = ENEMY_SKILLS.get(enemy_name, [])
        if skills:
            skill = random.choice(skills)
            return {"type": "skill", "skill": skill}
        else:
            return {"type": "attack"}
    
    return {"type": action}

# ========================================
# 属性攻撃システム
# ========================================

ELEMENT_SYSTEM = {
    "fire": {
        "weak_against": ["ice", "water"],
        "strong_against": ["dark", "earth"],
        "damage_bonus": 1.5
    },
    "ice": {
        "weak_against": ["fire"],
        "strong_against": ["water"],
        "damage_bonus": 1.5
    },
    "lightning": {
        "weak_against": ["earth"],
        "strong_against": ["water", "ice"],
        "damage_bonus": 1.5
    },
    "dark": {
        "weak_against": ["holy", "light"],
        "strong_against": ["none"],
        "damage_bonus": 1.3
    },
    "holy": {
        "weak_against": ["dark"],
        "strong_against": ["dark", "undead"],
        "damage_bonus": 1.5
    },
    "none": {
        "weak_against": [],
        "strong_against": [],
        "damage_bonus": 1.0
    }
}

def calculate_element_damage(base_damage: int, attacker_element: str, defender_element: str):
    """属性相性によるダメージ計算"""
    attacker_data = ELEMENT_SYSTEM.get(attacker_element, ELEMENT_SYSTEM["none"])
    
    if defender_element in attacker_data["strong_against"]:
        return int(base_damage * attacker_data["damage_bonus"])
    elif defender_element in attacker_data["weak_against"]:
        return int(base_damage * 0.7)
    else:
        return base_damage

# ========================================
# レイドボスデータ
# ========================================

RAID_BOSSES = {
    "raid_500": {
        "id": "raid_500",
        "name": "巨大スライムキング",
        "distance": 500,
        "hp": 5000,
        "atk": 20,
        "def": 10,
        "element": "none",
        "ai_pattern": "boss",
        "rewards": [
            {"item": "スライムの王冠", "weight": 100},
            {"item": "HP回復薬（大）", "weight": 50},
            {"item": "MP回復薬（大）", "weight": 50},
            {"item": "coins", "amount": [500, 1000], "weight": 100}
        ],
        "description": "500m地点に現れる巨大なスライムの王"
    },
    "raid_1000": {
        "id": "raid_1000",
        "name": "洞窟の守護者ゴーレム",
        "distance": 1000,
        "hp": 8000,
        "atk": 30,
        "def": 20,
        "element": "earth",
        "ai_pattern": "boss",
        "rewards": [
            {"item": "ゴーレムの核", "weight": 100},
            {"item": "石の大盾", "weight": 80},
            {"item": "HP回復薬（大）", "weight": 60},
            {"item": "MP回復薬（大）", "weight": 60},
            {"item": "coins", "amount": [800, 1500], "weight": 100}
        ],
        "description": "1000m地点を守る強大な石の巨人"
    },
    "raid_1500": {
        "id": "raid_1500",
        "name": "闇を纏いし者",
        "distance": 1500,
        "hp": 12000,
        "atk": 40,
        "def": 15,
        "element": "dark",
        "ai_pattern": "boss",
        "rewards": [
            {"item": "闇の結晶", "weight": 100},
            {"item": "黒騎士の剣", "weight": 70},
            {"item": "黒騎士の鎧", "weight": 70},
            {"item": "HP回復薬（大）", "weight": 80},
            {"item": "MP回復薬（大）", "weight": 80},
            {"item": "coins", "amount": [1000, 2000], "weight": 100}
        ],
        "description": "1500m地点に潜む闇の化身"
    }
}

def get_raid_boss_data(distance: int):
    """距離に基づいてレイドボスデータを取得"""
    for boss_id, boss_data in RAID_BOSSES.items():
        if boss_data["distance"] == distance:
            return boss_data
    return None

# ========================================
# 特殊敵データ
# ========================================

SPECIAL_ENEMIES = {
    "ゴールデンスライム": {
        "name": "ゴールデンスライム",
        "hp": 100,
        "atk": 10,
        "def": 5,
        "element": "holy",
        "ai_pattern": "coward",
        "spawn_rate": 0.001,
        "exp": 500,
        "drops": [
            {"item": "黄金のスライムゼリー", "weight": 100},
            {"item": "王者の剣", "weight": 50},
            {"item": "エリクサー", "weight": 30},
            {"item": "coins", "amount": [1000, 3000], "weight": 100}
        ],
        "description": "極めて稀に出現する黄金のスライム。倒せば莫大な富を得る"
    },
    "ミミック": {
        "name": "ミミック",
        "hp": 150,
        "atk": 35,
        "def": 8,
        "element": "dark",
        "ai_pattern": "aggressive",
        "spawn_rate": 0.15,
        "exp": 200,
        "drops": [
            {"item": "宝箱の破片", "weight": 100},
            {"item": "業火の剣", "weight": 30},
            {"item": "死神の鎌", "weight": 20},
            {"item": "HP回復薬（大）", "weight": 50},
            {"item": "MP回復薬（大）", "weight": 50},
            {"item": "coins", "amount": [500, 1500], "weight": 80}
        ],
        "description": "宝箱に擬態した危険なモンスター。即死攻撃を持つ"
    }
}

# ========================================
# 商人システム
# ========================================

MERCHANT_ITEMS_POOL = {
    "weapons": [
        {"name": "鉄の剣", "price": 150},
        {"name": "骨の剣", "price": 200},
        {"name": "毒の短剣", "price": 250},
        {"name": "魔法の杖", "price": 300},
        {"name": "炎の大剣", "price": 400},
        {"name": "ドラゴンソード", "price": 500},
        {"name": "死神の鎌", "price": 600}
    ],
    "armors": [
        {"name": "鉄の盾", "price": 150},
        {"name": "骨の盾", "price": 200},
        {"name": "死者の兜", "price": 250},
        {"name": "不死の鎧", "price": 350},
        {"name": "地獄の鎧", "price": 450},
        {"name": "黒騎士の盾", "price": 500}
    ],
    "potions": [
        {"name": "HP回復薬（小）", "price": 30},
        {"name": "HP回復薬（中）", "price": 80},
        {"name": "HP回復薬（大）", "price": 200},
        {"name": "MP回復薬（小）", "price": 30},
        {"name": "MP回復薬（中）", "price": 80},
        {"name": "MP回復薬（大）", "price": 200},
        {"name": "エリクサー", "price": 500}
    ],
    "materials": [
        {"name": "蜘蛛の糸", "price": 50},
        {"name": "腐った肉", "price": 40},
        {"name": "悪魔の角", "price": 100},
        {"name": "竜の牙", "price": 150},
        {"name": "幽霊の布", "price": 120}
    ]
}

def generate_merchant_inventory():
    """商人の在庫をランダム生成（5個）"""
    inventory = []
    
    categories = list(MERCHANT_ITEMS_POOL.keys())
    selected_items = set()
    
    while len(inventory) < 5:
        category = random.choice(categories)
        items = MERCHANT_ITEMS_POOL[category]
        item = random.choice(items)
        
        if item["name"] not in selected_items:
            inventory.append({
                "name": item["name"],
                "type": category.rstrip('s'),
                "price": item["price"]
            })
            selected_items.add(item["name"])
    
    return inventory

def calculate_sell_price(item_name: str):
    """アイテムの売却価格を計算（購入価格の50%）"""
    for category in MERCHANT_ITEMS_POOL.values():
        for item in category:
            if item["name"] == item_name:
                return int(item["price"] * 0.5)
    
    item_info = ITEMS_DATABASE.get(item_name)
    if item_info:
        if item_info.get("type") == "weapon":
            attack = item_info.get("attack", 0)
            return attack * 10
        elif item_info.get("type") == "armor":
            defense = item_info.get("defense", 0)
            return defense * 10
    
    return 10
