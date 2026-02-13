import readchar
import requests
import shutil
import math
import json
import os

CACHE = "cache.json" # str file path or None

class Item:
    def __init__(self, dat):
        self.data = dat
        self.got = 0
        self.want = [0, 0]

    def __getitem__(self, it):
        return self.data[it]

    def __repr__(self): return str(self)
    def __str__(self):
        return f"{self['name']}\n{self['count']}"


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
    return [Item(d) for d in dat]

def print_screen(shop, sel):
    print("\033[2J\033[0;0H", end="")
    size = shutil.get_terminal_size()
    strs = [str(i).split("\n") for i in shop]

    itwids = [max(len(j) for j in i)+2 for i in strs]
    mostwid = max(itwids)
    colamnt = math.floor((size.columns-1) / mostwid)
    cols = [
        [] for _ in range(colamnt)
    ]
    for idx, it in enumerate(strs):
        cols[idx%colamnt].append(it)

    colwids = [max(itwids[c::colamnt]) for c in range(colamnt)]
    mxrows = max(len(c) for c in cols)
    rowheis = [max(len(c[i]) for c in cols if i < len(c)) for i in range(mxrows)]

    mxhei = size.lines-1
    startrow = math.floor(sel / colamnt)
    lastrow = 0
    lrhei = 0
    for r in rowheis[::-1]:
        if lrhei + r + 1 > mxhei:
            break
        lrhei += r + 1
        lastrow += 1
    viewstartrow = min(startrow, mxrows - lastrow)

    rowamnt = 0
    rowhei = 0
    for r in rowheis[viewstartrow:]:
        if rowhei + r + 1 > mxhei:
            break
        rowhei += r + 1
        rowamnt += 1
    
    print("╭", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┬", end='')
    print("─"*colwids[-1]+"╮")

    start, end = viewstartrow, viewstartrow+rowamnt
    for i in range(start, end):
        for j in range(rowheis[i]):
            for idx, c in enumerate(cols):
                hl = "7" if i*colamnt+idx == sel else "0"
                if len(c) <= i or len(c[i]) <= j:
                    print(f"│\033[{hl}m"+" "*colwids[idx], end='\033[0m')
                else:
                    txt = c[i][j]
                    spaces = colwids[idx] - len(txt)
                    prevspaces = math.floor(spaces/2)
                    print(f"│\033[{hl}m"+" "*prevspaces+txt+" "*(spaces-prevspaces), end='\033[0m')
            print("│")

        if i < end-1:
            print("├", end='')
            for cw in colwids[:-1]:
                print("─"*cw+"┼", end='')
            print("─"*colwids[-1]+"┤")

    print("╰", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┴", end='')
    print("─"*colwids[-1]+"╯", end='\033[0;0H', flush=True)

    return colamnt

shop = get_shop()
item = 0
while True:
    cols = print_screen(shop, item)
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
