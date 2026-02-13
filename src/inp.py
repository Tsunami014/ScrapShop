import readchar
from readchar import key

def read():
    try:
        k = readchar.readkey()
    except (KeyboardInterrupt, EOFError):
        return None
    if k == '1':
        from .help import get_help
        get_help()
        return
    if k == '2':
        from .choose import choose
        choose()
        return
    return k
