import readchar
import requests
import shutil
import math
import json
import os
import re

CACHE = "cache.json" # str file path or None
SIDEBAR_WIDTH = 1/3 # Ratio for the sidebar width compared to the screen width
COIN = "⧖"

_reg = re.compile("\033\\[[0-9;]+.")
def stripAnsi(txt):
    return re.sub(_reg, "", txt)
def strlen(txt):
    return len(re.sub(_reg, "", txt))

class Item:
    def __init__(self, dat):
        self.name = dat['name'].capitalize()
        self._desc = dat['description'].capitalize()
        self.heart = dat['heartCount']
        self.category = dat['category']
        self.count = dat['count']
        self.upgrCost = dat['nextUpgradeCost']
        self.upgrProb = dat['boostAmount']

        self.data = dat
        self.title() # Also updates self.score

        self.upgrades = 0
        self.want = False

    def title(self):
        if self.soldout:
            self.score = 0
            return f"\033[90m{self.name}\n\033[90mSold out"

        # cols - 0 good, 1 warn, 2 bad
        def convColour(col):
            return \
                "92" if col < 1 else \
                "93" if col < 2 else \
                "91"
        countnorm = max((20-self.count)/5, 0)
        probnorm = (100-self.probability)/30
        heartnorm = self.heart/7
        costnorm = self.cost/12
        upgrprobnorm = (20-self.upgrProb)/7
        upgrcostnorm = self.upgrCost/6
        allcols = [countnorm, probnorm, heartnorm, costnorm, upgrprobnorm, upgrcostnorm]
        self.score = sum(min(i, 3) for i in allcols)/len(allcols) - 0.3
        return (
            f"\033[{convColour(self.score)}m{self.name}"
            "\033[39m "
            f"\033[1;{convColour(countnorm)}mx{self.count}\n"

            f"\033[1;{convColour(probnorm)}m{self.probability}%"
            "\033[39m "
            f"\033[1;{convColour(heartnorm)}m{self.heart}♥"
            "\033[39m "
            f"\033[1;{convColour(costnorm)}m{COIN}{self.cost}"
            "\033[39m(↑"
                f"\033[1;{convColour(upgrprobnorm)}m{self.upgrProb}% "
                f"\033[1;{convColour(upgrcostnorm)}m{COIN}{self.upgrCost}"
            "\033[39m)"
        )

    @property
    def probability(self):
        return self.data['effectiveProbability']
    @property
    def cost(self):
        return max(1, round(self.data['price'] * (self.data['baseProbability'] / 100)))
    @property
    def soldout(self):
        return self.count == 0

    def sort(self):
        return (self.soldout, self.score, -self.probability)

    def __repr__(self): return self.name
    def __str__(self): return self.name

    def desc(self):
        if self.soldout:
            return "Sold out\n\n"+\
                f"{self._desc}"
        return f"{self.name} ({self.category})\n"+\
            f"Only {self.count} left, {self.heart} ppl hearted\n"+\
            f"Next upgrade: {COIN}{self.upgrCost} (+{self.upgrProb}%)\n"+\
            "\n"+\
            f"{self._desc}"


def get_shop():
    print("Loading the shop...")
    if CACHE and os.path.exists(CACHE):
        with open(CACHE) as f:
            dat = json.load(f)
    else:
        req = requests.get("https://api.scraps.hackclub.com/shop/items")
        req.raise_for_status()
        dat = req.json()
        if CACHE:
            with open(CACHE, "w+") as f:
                json.dump(dat, f)
    li = [Item(d) for d in dat]
    li.sort(key=lambda it: it.sort())
    return li

def iterSidebar(sidebar: str, max_width):
    mxwid = max_width-2
    i = 0
    ln = len(sidebar)
    while i < ln:
        end = sidebar.find("\n", i, i+mxwid)
        found = end != -1
        if not found:
            if i+mxwid >= ln:
                end = ln
            else:
                end = sidebar.rfind(" ", i, i+mxwid)
                found = end != -1
                if not found:
                    end = i+mxwid
        yield " \033[100m"+sidebar[i:end].ljust(mxwid)+"\033[0m "
        if found:
            i = end+1
        else:
            i = end
    spaces = " \033[100m" + " "*mxwid + "\033[0m "
    while True:
        yield spaces

def print_screen(shop, sel, sidebar):
    print("\033[2J\033[0;0H", end="")
    size = shutil.get_terminal_size()
    strs = [i.title().split("\n") for i in shop]

    itwids = [max(strlen(j) for j in i)+2 for i in strs]
    mostwid = max(itwids)
    sbwidth = round(size.columns * SIDEBAR_WIDTH)
    colamnt = math.floor((size.columns-1-sbwidth) / mostwid)
    if colamnt <= 0:
        print("Screen too small")
        return 1
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
                hl = "7" if i*colamnt+idx == sel else "0"
                prefix = f"\033[{hl}m"
                if len(c) <= i or len(c[i]) <= j:
                    print("│"+prefix+" "*colwids[idx], end='\033[0m')
                else:
                    txt = c[i][j]
                    spaces = colwids[idx] - strlen(txt)
                    prevspaces = math.floor(spaces/2)
                    print("│"+prefix+" "*prevspaces+txt+"\033[0m"+prefix+" "*(spaces-prevspaces), end='\033[0m')
            print("│")

        if i < end-1:
            print(next(sbiter), end="")
            print("├", end='')
            for cw in colwids[:-1]:
                print("─"*cw+"┼", end='')
            print("─"*colwids[-1]+"┤")

    moreRows = mxhei - rowhei
    if moreRows < 0:
        print(sbspaces, end='')
    else:
        print(next(sbiter), end="")

    print("╰", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┴", end='')
    print("─"*colwids[-1]+"╯", end="")

    for _ in range(moreRows):
        print("\n"+next(sbiter), end="")
    print(end='\033[0;0H', flush=True)

    return colamnt

shop = get_shop()
item = 0
while True:
    cols = print_screen(shop, item, shop[item].desc())
    try:
        k = readchar.readkey()
    except (KeyboardInterrupt, EOFError):
        print("\033[2J", end="", flush=True)
        break
    if k == readchar.key.UP:
        item -= cols
    if k == readchar.key.DOWN:
        item += cols
    if k == readchar.key.LEFT:
        item -= 1
    if k == readchar.key.RIGHT:
        item += 1
    item = max(min(item, len(shop)-1), 0)
