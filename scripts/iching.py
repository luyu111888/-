# -*- coding: utf-8 -*-
"""深情猫的易学铺子 - 周易数字起卦脚本

用法:
    python iching.py 3 5 7        # 三个数字: 第一个数定下卦、第二个数定上卦、第三个数定动爻
    python iching.py 3 5          # 两个数字: 第一个数定下卦、第二个数定上卦, 两数之和定动爻
    python iching.py              # 交互模式

数字遵循先天八卦数: 乾1 兑2 离3 震4 巽5 坎6 艮7 坤8
第一个数字定下卦, 第二个数字定上卦; 除8余数定卦(余0取8=坤), 除6余数定动爻(余0取6=上爻动)。
"""
import re
import sys
from pathlib import Path

# 尽量以 UTF-8 输出，避免 Windows 中文控制台把卦象字符打乱或报错
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 数据目录(本文件位于 skills/iching-divination/scripts/ 下)
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
if str(_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(_DATA_DIR))

try:
    from trigrams import TRIGRAMS
    from hexagrams_a import HEXAGRAMS_A
    from hexagrams_b import HEXAGRAMS_B
except ImportError as exc:
    print(f"[铺子告急] 数据文件加载失败: {exc}")
    sys.exit(1)

HEXAGRAMS = {}
HEXAGRAMS.update(HEXAGRAMS_A)
HEXAGRAMS.update(HEXAGRAMS_B)

# 爻位爻题: (位置, 阴阳) -> 爻题, 如 (1,阳)->"初九", (6,阴)->"上六"
def yaoti(pos, yang):
    if pos == 1:
        return "初" + ("九" if yang else "六")
    if pos == 6:
        return "上" + ("九" if yang else "六")
    return ("九" if yang else "六") + str(pos)

def trig_id(bits):
    """三爻(自下而上) -> 先天八卦数"""
    for tid, info in TRIGRAMS.items():
        if info["bits"] == bits:
            return tid
    return None

def trig_img(tid):
    return TRIGRAMS[tid]["image"]

def n_to_trigram(n):
    """数字除8取余定卦, 余0取8(坤)"""
    return ((n - 1) % 8) + 1

def n_to_yao(n):
    """数字除6取余定动爻, 余0取6(上爻)"""
    return ((n - 1) % 6) + 1

def hex_bits(upper_id, lower_id):
    """由上下卦先天数生成六爻(自下而上)"""
    return TRIGRAMS[lower_id]["bits"] + TRIGRAMS[upper_id]["bits"]

def hex_info(bits):
    lower_id = trig_id(bits[0:3])
    upper_id = trig_id(bits[3:6])
    rec = HEXAGRAMS[f"{upper_id}{lower_id}"]
    return upper_id, lower_id, rec

def draw_hex(bits):
    """画卦象, 上爻在顶部"""
    lines = []
    for b in reversed(bits):
        lines.append("     " + ("━━━━━━━" if b else "━━━   ━━━"))
    return "\n".join(lines)

def mutua_bits(bits):
    """互卦六爻(本卦第2、3、4爻为下互卦, 第3、4、5爻为上互卦)"""
    return [bits[1], bits[2], bits[3], bits[2], bits[3], bits[4]]

def change_bits(bits, move_pos):
    """变卦: 动爻阴阳互变"""
    nb = list(bits)
    nb[move_pos - 1] = 1 - nb[move_pos - 1]
    return nb

def show_hex(title, bits):
    upper_id, lower_id, rec = hex_info(bits)
    upper_img = trig_img(upper_id)
    lower_img = trig_img(lower_id)
    print(f"\n【{title}】{rec['full']}（上{upper_img}下{lower_img}）")
    print(draw_hex(bits))
    print(f"  卦辞：{rec['judgment']}")
    return rec

def parse_numbers(text):
    return [int(x) for x in re.findall(r"\d+", text)]

def run(nums):
    if len(nums) == 3:
        a, b, c = nums
        note = f"三个数字 {a} {b} {c}：{a}定下卦，{b}定上卦，{c}定动爻"
    elif len(nums) == 2:
        a, b = nums
        c = a + b
        note = f"两个数字 {a} {b}：{a}定下卦，{b}定上卦，两数之和 {a}+{b}={c} 定动爻"
    else:
        print("小铺子听不懂这报数，请您报两个或三个数字。")
        return

    lower_id = n_to_trigram(a)
    upper_id = n_to_trigram(b)
    move_pos = n_to_yao(c)

    print("=" * 46)
    print("深情猫的易学铺子 · 起卦")
    print("=" * 46)
    print(f"起卦依据：{note}")
    print(f"下卦取余：{a} ÷ 8 余{a % 8} → 数{lower_id}（{TRIGRAMS[lower_id]['image']}）")
    print(f"上卦取余：{b} ÷ 8 余{b % 8} → 数{upper_id}（{TRIGRAMS[upper_id]['image']}）")
    print(f"动爻取余：{c} ÷ 6 余{c % 6} → 第{move_pos}爻")

    base_bits = hex_bits(upper_id, lower_id)
    base = show_hex("本卦", base_bits)

    # 动爻
    move_yang = base_bits[move_pos - 1] == 1
    print(f"\n【动爻】第{move_pos}爻（{yaoti(move_pos, move_yang)}）")
    print(f"  爻辞：{base['lines'][move_pos - 1]}")

    # 互卦
    show_hex("互卦", mutua_bits(base_bits))

    # 变卦
    changed = change_bits(base_bits, move_pos)
    show_hex("变卦", changed)

    print("\n" + "=" * 46)
    print("卦已排定，请您据此向铺主问询吉凶进退。")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(parse_numbers(" ".join(sys.argv[1:])))
    else:
        print("官人，请报上几个数字（空格或逗号隔开皆可，两个或三个）：")
        text = sys.stdin.read() if not sys.stdin.isatty() else input("> ")
        run(parse_numbers(text))
