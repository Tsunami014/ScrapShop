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
    # amount left, (scraps, %), (upgrade scraps, upgrade %)
    return [
        Item("Stickers", 40,
             (8, 79), (1, 4)),
        Item("Daydream shirt", 13,
             (43, 61), (10, 8)),
        Item("applefork.mp4.mp3.mp3 cd", 10,
             (33, 50), (11, 10)),
    ]

def print_screen(shop):
    print("\033[2J", end="")
    size = shutil.get_terminal_size()
    strs = [str(i).split("\n") for i in shop]

    cols = []
    tmp = []
    hei = 1
    mxhei = size.lines
    for it in strs:
        h = len(it)
        if hei + h > mxhei:
            hei = h+1
            if tmp: cols.append(tmp)
            tmp = [it]
        else:
            hei += h + 1
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
