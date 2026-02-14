from . import inp
from .shop import COIN
from .utils import itertxt
import shutil

HELP = """
\033[93;1mScrapShop\033[0m
(press down/up to scroll the help)

\033[95;1mMain keys\033[0m (works on every screen)
  1 - go to choose items
  2 - go to see odds

  0 - go to help
  ctrl+c - quit

\033[95;1mIcons\033[0m
  x - Amount left
  ↑ or + - Upgrades
  % - Percent chance of getting the item
  {COIN} - Scraps
  hr - Amount of hours required for an average (tier 2) project, based on scraps requirement
  ♥ - Amount of people who've hearted the item

\033[95;1mChoose items screen\033[0m (1)
Each item section is coloured green/orange/red where red are harder to get due to the requirements (e.g. not many left, many people wanting it)
  Arrow keys to look at different items
  Space to toggle item selection
  Backspace to unselect everything

\033[95;1mOdds screen\033[0m (2)
  Up/down arrow keys to change selection
  = to +1 upgrade, - to -1 upgrade
  + to set to full upgrades, _ to set to no upgrades
"""[1:-1].replace("{COIN}", COIN)
def _get_help_newlines():
    li = []
    i = 0
    init = False
    while i != 0 or not init:
        init = True
        li.append(i)
        i = HELP.find('\n', i)+1
    return li
_help_newline_locs = _get_help_newlines()
_helpLn = len(_help_newline_locs)

def print_help(offs):
    print("\033[2J\033[0;0H", end="")
    size = shutil.get_terminal_size()
    itr = itertxt(HELP[_help_newline_locs[offs]:], size.columns)
    for _ in range(offs, min(offs+size.lines, _helpLn)-1):
        print(next(itr), flush=False)
    print(next(itr), end='\033[0;0H', flush=True)

def get_help():
    offs = 0
    while True:
        print_help(offs)
        k = inp.read()
        if k is None:
            return
        if k == inp.key.UP:
            offs -= 1
        if k == inp.key.DOWN:
            offs += 1
        offs = max(min(offs, _helpLn-1), 0)
