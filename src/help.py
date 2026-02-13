from . import inp

def get_help():
    while True:
        print("\033[2J\033[0;0H", end="")
        print("""
\033[1mScrapShop\033[0m
  1 - go to help
  2 - go to choose items
  ctrl+c - quit
See readme for further usage instructions
"""[1:-1])
        if inp.read() is None:
            return
