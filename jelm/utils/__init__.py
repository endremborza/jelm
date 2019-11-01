def dict_subset(d, keys):
    return {k: v for k, v in d.items() if k in keys}
