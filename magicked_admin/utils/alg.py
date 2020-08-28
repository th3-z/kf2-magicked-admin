def uuid(obj):
    h = hash(obj)
    return str(h % (1 << h.bit_length()))
