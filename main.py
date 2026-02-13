from src import get_help, inp

if __name__ == '__main__':
    get_help()
    while inp.nxt is not None:
        inp.nxt()
    print("\033[2J\033[0;0H", end="", flush=True)
