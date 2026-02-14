import readchar
from readchar import key

nxt = None
def read():
    global nxt
    try:
        k = readchar.readkey()
    except (KeyboardInterrupt, EOFError):
        nxt = None
        return None
    if k == '0':
        from .help import get_help
        nxt = get_help
        return
    if k == '1':
        from .choose import choose
        nxt = choose
        return
    if k == '2':
        from .odds import see_odds
        nxt = see_odds
        return
    return k
