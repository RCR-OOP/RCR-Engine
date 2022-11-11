def neni(value, default=None):
    if isinstance(value, None) or isinstance(value, Ellipsis) or isinstance(value, NotImplemented):
        return default
    else:
        return value