from . import inp, SHOP
from .utils import itertxt
from .shop import COIN
import shutil
import math

def combine_probs(probs):
    return round(math.prod([p/100 for p in probs]) * 100, 3)

def iterSide(sidebar, max_width):
    mxwid = max_width-4
    yield " \033[90m▟\033[0;100m"+" "*mxwid+"\033[0;90m▙ "
    yield " \033[90m▜\033[0;100m"+" "*mxwid+"\033[0;90m▛ "
    for t in itertxt(sidebar, mxwid):
        yield " \033[100m "+t+" \033[0m "

def get_title(it):
    return (
        f"{it.name}  "
        f"\033[95m↑{it.upgrades}  "
        f"\033[93m{it.upgradedProb}%(+{it.upgrProb}%) "
        f"\033[96m {COIN}{it.upgradedCost}(+{COIN}{it.upgrCost}) "
        f"\033[92m {it.upgradedHours}hr(+{it.upgrHours}hr)"
    )

def get_desc(it, wants):
    totBaseCost = sum(i.cost for i in wants)
    totBaseProb = combine_probs(i.probability for i in wants)
    totBaseHrs = sum(i.hours for i in wants)
    totCost = sum(i.upgradedCost for i in wants)
    totProb = combine_probs(i.upgradedProb for i in wants)
    totHrs = round(sum(i.upgradedHours for i in wants), 2)
    return (
        f"\033[1;97mTotal:\n"
        f"\033[95mBase: "
            f"\033[93m{totBaseProb}% "
            f"\033[96m {COIN}{totBaseCost} "
            f"\033[92m {totBaseHrs}hr\n"
        f"\033[95mUpgraded stats: "
            f"\033[93m{totProb}% "
            f"\033[96m {COIN}{totCost} "
            f"\033[92m {totHrs}hr\n"

        f"\033[1;97m{it.name}:\n"
        f"\033[95mBase: "
            f"\033[93m{it.probability}% "
            f"\033[96m {COIN}{it.cost} "
            f"\033[92m {it.hours}hr\n"
        f"\033[95mTo upgrade: "
            f"\033[93m+{it.upgrProb}% "
            f"\033[96m +{COIN}{it.upgrCost} "
            f"\033[92m +{it.upgrHours}hr\n"
        f"\033[95mWith {it.upgrades} upgrades: "
            f"\033[93m{it.upgradedProb}% "
            f"\033[96m {COIN}{it.upgradedCost} "
            f"\033[92m {it.upgradedHours}hr\n"
    )

def get_screen(sel):
    wants = [i for i in SHOP if i.want]
    if len(wants) == 0:
        return "Nothing selected!", ""
    return "\n".join(
            "\033[31"+(";7;1" if idx == sel else "")+"m"+get_title(i) for idx, i in enumerate(wants)
        ), get_desc(wants[sel], wants)

def print_screen(sel):
    print("\033[0;0H\033[2K")
    size = shutil.get_terminal_size()
    wid = math.floor(size.columns/2)
    gap = "\033[0m"+" "*(size.columns%2)

    txt1, txt2 = get_screen(sel)
    sect1 = iterSide(txt1, wid)
    sect2 = iterSide(txt2, wid)

    def prt():
        return "\033[0m" + next(sect1) + gap + next(sect2) + "\033[0m"
    print(prt())
    end = prt()
    for _ in range(size.lines-4):
        print(prt())
    print(end+"\n\033[2K", end='\033[0;0H', flush=True)

sel = 0
def see_odds():
    global sel
    wants = [i for i in SHOP if i.want]
    while True:
        print_screen(sel)
        k = inp.read()
        if k is None:
            return
        if k == '=':
            if wants[sel].upgradedProb < 100:
                wants[sel].upgrades += 1
        if k == '-':
            wants[sel].upgrades = max(wants[sel].upgrades-1, 0)
        if k == '+':
            while wants[sel].upgradedProb < 100:
                wants[sel].upgrades += 1
        if k == '_':
            wants[sel].upgrades = 0
        if k == inp.key.UP:
            sel -= 1
        if k == inp.key.DOWN:
            sel += 1
        sel = max(min(sel, len(wants)-1), 0)

