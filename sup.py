def sup(data, by):
    a = 0
    b = 0
    c = []
    for i in data:
        if i == by:
            c.append(data[a:b])
            a = b + 1
        elif b == len(data) - 1 and i != by:
            c.append(data[a:b + 1])
        b += 1
    return c
