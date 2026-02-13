def itertxt(txt: str, max_width):
    i = 0
    ln = len(txt)
    while i < ln:
        end = txt.find("\n", i, i+max_width)
        found = end != -1
        if not found:
            if i+max_width >= ln:
                end = ln
            else:
                end = txt.rfind(" ", i, i+max_width)
                found = end != -1
                if not found:
                    end = i+max_width
        yield txt[i:end].ljust(max_width)
        if found:
            i = end+1
        else:
            i = end
    spaces = " "*max_width
    while True:
        yield spaces
