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

def get_screen():
    wants = [i for i in SHOP if i.want]
    if len(wants) == 0:
        return "Nothing wanted!", ""
    return "\n".join(i.name for i in wants), ""

def print_screen():
    print("\033[2J\033[0;0H")
    size = shutil.get_terminal_size()
    wid = math.floor(size.columns/2)
    gap = "\033[0m"+" "*(size.columns%2)

    txt1, txt2 = get_screen()
    sect1 = iterSide(txt1, wid)
    sect2 = iterSide(txt2, wid)

    def prt():
        return "\033[0m" + next(sect1) + gap + next(sect2) + "\033[0m"
    print(prt())
    end = prt()
    for _ in range(size.lines-4):
        print(prt())
    print(end, end='\033[0;0H', flush=True)

def see_odds():
    while True:
        print_screen()
        k = inp.read()
        if k is None:
            return

