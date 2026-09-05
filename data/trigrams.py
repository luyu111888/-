# -*- coding: utf-8 -*-
"""先天八卦基础表：卦序编号、卦名、象名、三爻（自下而上）。"""

TRIGRAMS = {
    1: {"name": "乾", "image": "天", "bits": [1, 1, 1]},
    2: {"name": "兑", "image": "泽", "bits": [1, 1, 0]},
    3: {"name": "离", "image": "火", "bits": [1, 0, 1]},
    4: {"name": "震", "image": "雷", "bits": [1, 0, 0]},
    5: {"name": "巽", "image": "风", "bits": [0, 1, 1]},
    6: {"name": "坎", "image": "水", "bits": [0, 1, 0]},
    7: {"name": "艮", "image": "山", "bits": [0, 0, 1]},
    8: {"name": "坤", "image": "地", "bits": [0, 0, 0]},
}
