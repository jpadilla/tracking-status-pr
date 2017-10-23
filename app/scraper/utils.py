import unicodedata


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def is_float(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


def is_blank(s):
    blank = False

    if not s:
        blank = True

    try:
        if s.isspace():
            blank = True
    except AttributeError:
        pass

    return blank
