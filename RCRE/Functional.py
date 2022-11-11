def neni(value, default=None):
    if isinstance(value, None) or isinstance(value, Ellipsis) or isinstance(value, NotImplemented):
        return default
    return value

def ntd(value, default=-1):
    if value < 0:
        return default
    return value