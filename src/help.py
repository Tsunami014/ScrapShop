from . import inp
import shutil

HELP = """
\033[93;1mScrapShop\033[0m
(press down/up to scroll the help)

\033[95;1mMain keys\033[0m (works on every screen)
  1 - go to choose items
  2 - go to see odds

  0 - go to help
  ctrl+c - quit

\033[95;1mChoose items screen\033[0m (1)
  Arrow keys to look at different items
  Space to toggle 'wanting'

\033[95;1mOdds screen\033[0m (2)
"""[1:-1].split("\n")
_helpLn = len(HELP)

def print_help(offs):
    print("\033[2J\033[0;0H", end="")
    size = shutil.get_terminal_size()
    mx = min(offs+size.lines, _helpLn)-1
    for i in range(offs, mx):
        print(HELP[i])
    print(HELP[mx], end='\033[0;0H', flush=True)

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
