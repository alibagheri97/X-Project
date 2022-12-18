class Value:
    dic = dict()
    key = ""
    go = ""
    path = "/etc/x-ui/x-ui.db"


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


def write(fname, content):
    file = open(fname, "w", encoding="utf8")
    byt = file.write(content)
    file.close()


def read(fname):
    file = open(fname, "r", encoding="utf8")
    f = file.read()
    file.close()
    return f


def findElement(data, find):
    step = find.__len__()
    lstStp = 0
    outLst = []
    for i in range(data.__len__() - step + 1):
        if find in data[i:i + step]:
            outLst.append((i, i + step))
    return outLst


def tagChange(data, id, element, value):
    tag = pickTag(data, id)
    if tag[0]:
        tg = pickTag(tag[0], element, symbol=(" ", " ", ">"))
        loc = [0, 0]
        if tg[0][0] == " ":
            loc[0] = tg[1][0] + 1
        else:
            loc[0] = tg[1][0]
        if tg[0][-1] in [" ", ">"]:
            loc[1] = tg[1][1] - 1
        else:
            loc[1] = tg[1][1]
        realoc = [loc[0] + tag[1][0], loc[1] + tag[1][0]]
        if "=" in element:
            element = sup(element, "=")[0]
        return data[:realoc[0]] + f'{element}="{value}"' + data[realoc[1]:]
    else:
        return None


def add2Tag(data, id, element, value):
    pt = pickTag(data, id)
    if pt[0]:
        tag = pt[0]
        idx = pt[-1]
        if tag[-1] == ">":
            return data[:idx[0]] + tag[:-1] + f' {element}="{value}">' + data[idx[1]:]
        else:
            return None
    else:
        return None


def insert2Tag(data, id, tag, mode="all"):
    pt = pickTag(data, id, mode=mode)
    if pt[0]:
        idx = pt[-1]
        if data[idx[-1] - 1] == ">":
            return data[:idx[-1]] + tag + data[idx[-1]:]
        else:
            return None
    else:
        return None


def deleteTag(data, id):
    pt = pickTag(data, id)
    if pt[0]:
        idx = pt[-1]
        if data[idx[-1] - 1] == ">":
            return data[:idx[0]] + data[idx[-1]:]
        else:
            return None
    else:
        return None


def pickTag(data, id, symbol=("<", ">"), mode="all"):
    cond = False
    if data[0] == "<":
        data = " " + data
        cond = True
    if type(symbol) != type(tuple()):
        symbol = (symbol, symbol)
    if mode == "all":
        if symbol.__len__() > 2:
            firstSymbol, lastSymbol, lstOr = symbol
        else:
            firstSymbol, lastSymbol = symbol
            lstOr = None
        lst = findElement(data, id)
        if not lst.__len__() == 1:
            return None, None
        lst = lst[0]
        first = 0
        last = 0
        count = 0
        while True:
            if firstSymbol == data[lst[0] - count - firstSymbol.__len__():lst[0] - count] and not first:
                first = lst[0] - count - firstSymbol.__len__()
            if (data[lst[1] + count:lst[1] + count + lastSymbol.__len__()] in [lastSymbol, lstOr]) and not last:
                last = lst[1] + count + lastSymbol.__len__()
            if first and last:
                break
            if (lst[1] + count > data.__len__() and not last) or (lst[0] - count < 0 and not first):
                first = None
                last = None
                break
            count += 1
        if first and last:
            if not cond:
                return data[first:last], (first, last)
            else:
                return data[first:last], (first - 1, last - 1)
        else:
            return None, None
    elif mode == "+":
        if symbol.__len__() != 1:
            lastSymbol = symbol[1]
        else:
            lastSymbol = symbol[0]
        lst = findElement(data, id)
        if not lst.__len__() == 1:
            return None, None
        lst = lst[0]
        last = 0
        count = 0
        while True:
            if data[lst[1] + count:lst[1] + count + lastSymbol.__len__()] == lastSymbol and not last:
                last = lst[1] + count + lastSymbol.__len__()
                break
            if lst[1] + count > data.__len__():
                last = None
                break
            count += 1
        if last:
            if not cond:
                return data[last - lastSymbol.__len__():last], (last - lastSymbol.__len__(), last)
            else:
                return data[last - lastSymbol.__len__():last], (last - lastSymbol.__len__() - 1, last - 1)
        else:
            return None, None
    elif mode == "-":
        firstSymbol = symbol[0]
        lst = findElement(data, id)
        if not lst.__len__() == 1:
            return None, None
        lst = lst[0]
        first = 0
        count = 0
        while True:
            if firstSymbol == data[lst[0] - count - firstSymbol.__len__():lst[0] - count] and not first:
                first = lst[0] - count - firstSymbol.__len__()
                break
            if lst[0] - count < 0:
                first = None
                break
            count += 1
        if first:
            if not cond:
                return data[first:first + firstSymbol.__len__()], (first, first + firstSymbol.__len__())
            else:
                return data[first:first + firstSymbol.__len__()], (first - 1, first + firstSymbol.__len__() - 1)
        else:
            return None, None
