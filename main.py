import requests
import shutil
import math

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
    req = requests.get("https://api.scraps.hackclub.com/shop/items")
    req.raise_for_status()
    return [Item(d) for d in req.json()]

def print_screen(shop):
    print("\033[2J", end="")
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
    
    print("╭", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┬", end='')
    print("─"*colwids[-1]+"╮")

    for i in range(mxrows):
        for j in range(rowheis[i]):
            for idx, c in enumerate(cols):
                if len(c) <= i:
                    print("│"+" "*colwids[idx], end='')
                else:
                    txt = c[i][j]
                    spaces = colwids[idx] - len(txt)
                    prevspaces = math.floor(spaces/2)
                    print("│"+" "*prevspaces+txt+" "*(spaces-prevspaces), end='')
            print("│")

        if i < mxrows-1:
            print("├", end='')
            for cw in colwids[:-1]:
                print("─"*cw+"┼", end='')
            print("─"*colwids[-1]+"┤")

    print("╰", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┴", end='')
    print("─"*colwids[-1]+"╯")

shop = get_shop()
print_screen(shop)
