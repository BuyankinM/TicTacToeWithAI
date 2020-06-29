def unpack(input_tuple):
    unpacked = tuple()
    for elem in input_tuple:
        if isinstance(elem, tuple):
            unpacked += elem
        else:
            unpacked += (elem, )

    return unpacked