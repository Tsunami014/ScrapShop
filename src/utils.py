import re
_reg = re.compile("\033\\[[0-9;]+.")
def stripAnsi(txt):
    return re.sub(_reg, "", txt)
def strlen(txt):
    return len(re.sub(_reg, "", txt))


def itertxt(txt: str, max_width):
    i = 0
    ln = len(txt)
    ansi = []
    while i < ln:
        end = -1
        idx = i
        sln = 0
        afterSpacesSln = 0
        ansi_part = ""
        in_ansi = False
        using_spaces = False
        using_newline = False
        skip1 = False
        while idx < ln:
            c = txt[idx]
            if c == '\033':
                in_ansi = True
                ansi_part = ""
                idx += 1
                continue
            if in_ansi:
                if c not in '0123456789;[':
                    if ansi_part:
                        ansi.append(ansi_part)
                    in_ansi = False
                    idx += 1
                    continue
                elif c == ';':
                    if ansi_part:
                        ansi.append(ansi_part)
                        ansi_part = ""
                elif c != '[':
                    ansi_part += c
            else:
                if c == ' ':
                    end = idx
                    skip1 = True
                    using_spaces = True
                    afterSpacesSln = 0
                elif c == '\n':
                    end = idx
                    skip1 = True
                    using_spaces = False
                    using_newline = True
                    break
                else:
                    afterSpacesSln += 1
                sln += 1
                if sln > max_width:
                    break
            idx += 1
        else:
            using_spaces = False
            end = idx
        if end == -1:
            end = idx
        if using_spaces:
            sln -= afterSpacesSln + 1

        if '0' in ansi:
            ansi = ansi[1-ansi[::-1].index('0'):]
        pref = ""
        if ansi:
            pref = "\033["+';'.join(ansi)+"m"
        yield pref + txt[i:end] + "\033[27;39m" + " "*(max_width-sln)
        if skip1:
            i = end+1
        else:
            i = end
        if using_newline:
            ansi = []
    spaces = " "*max_width
    while True:
        yield spaces
