NENI_TYPES = (..., None, NotImplemented)

def neni(value, default=None):
    if (type(value) in NENI_TYPES) or (value in NENI_TYPES):
        return default
    return value

def ntd(value, default=-1):
    if value < 0:
        return default
    return value