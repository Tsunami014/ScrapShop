from . import inp, SHOP
from .utils import itertxt
import shutil
import math

def iterSide(sidebar, max_width):
    mxwid = max_width-4
    yield " \033[90m▟\033[0;100m"+" "*mxwid+"\033[0;90m▙ "
    yield " \033[90m▜\033[0;100m"+" "*mxwid+"\033[0;90m▛ "
    for t in itertxt(sidebar, mxwid):
        yield " \033[100m "+t+" \033[0m "

def get_title(it):
    return it.name

def get_desc(it):
    return it.desc()

def get_screen(sel):
    wants = [i for i in SHOP if i.want]
    if len(wants) == 0:
        return "Nothing wanted!", "", 0
    return "\n".join(
            ("\033[7;1m" if idx == sel else "")+get_title(i)+"\033[27m" for idx, i in enumerate(wants)
        ), get_desc(wants[sel]), len(wants)

def print_screen(sel):
    print("\033[2J\033[0;0H")
    size = shutil.get_terminal_size()
    wid = math.floor(size.columns/2)
    gap = "\033[0m"+" "*(size.columns%2)

    txt1, txt2, mx = get_screen(sel)
    sect1 = iterSide(txt1, wid)
    sect2 = iterSide(txt2, wid)

    def prt():
        return "\033[0m" + next(sect1) + gap + next(sect2) + "\033[0m"
    print(prt())
    end = prt()
    for _ in range(size.lines-4):
        print(prt())
    print(end, end='\033[0;0H', flush=True)
    return mx

sel = 0
def see_odds():
    global sel
    while True:
        mx = print_screen(sel)
        k = inp.read()
        if k is None:
            return
        if k == inp.key.UP:
            sel -= 1
        if k == inp.key.DOWN:
            sel += 1
        sel = max(min(sel, mx-1), 0)

