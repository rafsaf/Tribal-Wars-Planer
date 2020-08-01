from tribal_wars.wioska import Village


def zbiorka_grubych_z_obrony(tekst):
    if tekst == "":
        return {}
    result = {}
    n = 0
    for i in tekst.split("\r"):

        if n % 2 == 0:
            n += 1
            continue

        else:
            n += 1


        i = i.split(",")

        wioska = Village(i[0])
        number = int(i[10])
        result[wioska.coord] = number
    return result


def zbiorka_grubych_z_ankiety(text_ankieta, text_obrona):
    if text_ankieta == "":
        return zbiorka_grubych_z_obrony(text_obrona)

    result = zbiorka_grubych_z_obrony(text_obrona)
    for line in text_ankieta.split("\r"):
        line = line.split()
        width = len(line)
        for i in range(width-1):
            if len(line[i].strip()) == 7 and line[i + 1].isnumeric():
                try:
                    result[line[i]] = int(line[i + 1])
                except Exception:
                    raise Exception("zbiorka grubych z ankiety - blad line 40")

    return result
