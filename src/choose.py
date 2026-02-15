from . import inp, SHOP
from .utils import itertxt, strlen
from .shop import COIN
import shutil
import math

SIDEBAR_WIDTH = 1/3 # Ratio for the sidebar width compared to the screen width

def iterSidebar(sidebar, max_width):
    for t in itertxt(sidebar, max_width-2):
        yield " \033[100m"+t+"\033[0m "

def print_screen(sel, sidebar):
    print("\033[0;0H", end="")
    size = shutil.get_terminal_size()
    strs = [i.title().split("\n") for i in SHOP]

    itwids = [max(strlen(j) for j in i)+2 for i in strs]
    mostwid = max(itwids)
    sbwidth = round(size.columns * SIDEBAR_WIDTH)
    colamnt = math.floor((size.columns-1-sbwidth) / mostwid)
    if colamnt <= 0:
        sbwidth = 0
        colamnt = math.floor((size.columns-1) / mostwid)
    cols = [
        [] for _ in range(colamnt)
    ]
    for idx, it in enumerate(strs):
        cols[idx%colamnt].append(it)

    colwids = [max(itwids[c::colamnt]) for c in range(colamnt)]
    mxrows = max(len(c) for c in cols)
    rowheis = [max(len(c[i]) for c in cols if i < len(c)) for i in range(mxrows)]
    sbwidth = size.columns - sum(i+1 for i in colwids) - 2

    mxhei = size.lines-1
    startrow = math.floor(sel / colamnt)
    lastrow = 0
    lrhei = 1
    for r in rowheis[::-1]:
        if lrhei + r + 1 > mxhei:
            break
        lrhei += r + 1
        lastrow += 1
    viewstartrow = min(startrow, mxrows - lastrow)

    rowamnt = 0
    rowhei = 1
    for r in rowheis[viewstartrow:]:
        if rowhei + r + 1 > mxhei:
            break
        rowhei += r + 1
        rowamnt += 1
    
    sbiter = iterSidebar(sidebar, sbwidth)
    sbspaces = " "*sbwidth
    print(sbspaces, end="")
    print("╭", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┬", end='')
    print("─"*colwids[-1]+"╮")

    start, end = viewstartrow, viewstartrow+rowamnt
    for i in range(start, end):
        for j in range(rowheis[i]):
            print(next(sbiter), end="")
            for idx, c in enumerate(cols):
                trueidx = i*colamnt+idx
                if trueidx == sel:
                    hl = "7"
                else:
                    hl = "0"
                item = SHOP[trueidx]
                if item.want:
                    hl += ";100;36"
                prefix = f"\033[{hl}m"
                if len(c) <= i or len(c[i]) <= j:
                    print("│"+prefix+" "*colwids[idx], end='\033[0m')
                else:
                    txt = c[i][j]
                    spaces = colwids[idx] - strlen(txt)
                    prevspaces = math.floor(spaces/2)
                    print("│"+prefix+" "*prevspaces+"\033[39m"+txt+"\033[0m"+prefix+" "*(spaces-prevspaces), end='\033[0m')
            print("│")

        if i < end-1:
            print(next(sbiter), end="")
            print("├", end='')
            for cw in colwids[:-1]:
                print("─"*cw+"┼", end='')
            print("─"*colwids[-1]+"┤")

    moreRows = mxhei - rowhei + 1
    if moreRows < 0:
        print(sbspaces, end='')
    else:
        print(next(sbiter), end="")

    print("╰", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┴", end='')
    print("─"*colwids[-1]+"╯", end="")

    for _ in range(moreRows):
        print("\n"+next(sbiter), end="\033[2K")
    print(end='\033[0;0H', flush=True)

    return colamnt

def desc(it):
    if it.soldout:
        return "Sold out\n\n"+it._desc
    return (
        f"\033[95;1m{it.name}\033[22;96m ({it.category})\n"
        f"\033[93m{it.count} left, {it.bought} bought, {it.heart} hearts\n"
        f"\033[93mEach upgrade: +{it.upgrProb}%, +{COIN}{it.upgrCost} (+{it.upgrHours}hr)\n"
        "\n"+it._desc
    )

item = 0
def choose():
    global item
    while True:
        it = SHOP[item]
        cols = print_screen(item, desc(it))
        k = inp.read()
        if k is None:
            return
        if k == " " and not it.soldout:
            it.want = not it.want
        if k == inp.key.BACKSPACE:
            for i in SHOP:
                i.want = False
        if k == "b":
            it.bought += 1
        if k == "B" and it.bought > 0:
            it.bought -= 1
        if k == inp.key.UP:
            item -= cols
        if k == inp.key.DOWN:
            item += cols
        if k == inp.key.LEFT:
            item -= 1
        if k == inp.key.RIGHT:
            item += 1
        item = max(min(item, len(SHOP)-1), 0)

