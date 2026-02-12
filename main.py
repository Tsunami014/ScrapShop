import shutil
import math

class Item:
    def __init__(self, name, left, base, upgr):
        self.name: str = name
        self.left: int = left
        self.base = base
        self.upgr = upgr
        self.got = 0
        self.want = [0, 0]

    def __repr__(self): return str(self)
    def __str__(self):
        return f"{self.name}\n{self.left}"


def get_shop():
    return [
        Item("Stickers", 40,
             (8, 79), (1, 4)),
    ]

def print_screen(shop):
    print("\033[2J", end="")
    size = shutil.get_terminal_size()
    strs = [str(i).split("\n") for i in shop]

    cols = []
    tmp = []
    wid = 0
    mxwid = size.columns-1
    for it in strs:
        w = max(len(j) for j in it)+3
        if wid + w > mxwid:
            wid = w
            if tmp: cols.append(tmp)
            tmp = [it]
        else:
            wid += w
            tmp.append(it)
    if tmp: cols.append(tmp)

    colwids = [max(max(len(i) for i in j) for j in c)+2 for c in cols]
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
                    txt = c[idx][j]
                    spaces = colwids[idx] - len(txt)
                    prevspaces = math.floor(spaces/2)
                    print("│"+" "*prevspaces+txt+" "*(spaces-prevspaces), end='')
            print("│")

        if i < mxrows-1:
            print("│", end='')
            for cw in colwids[:-1]:
                print("─"*cw+"┼", end='')
            print("─"*colwids[-1]+"│")

    print("╰", end='')
    for cw in colwids[:-1]:
        print("─"*cw+"┴", end='')
    print("─"*colwids[-1]+"╯")

shop = get_shop()
print_screen(shop)
