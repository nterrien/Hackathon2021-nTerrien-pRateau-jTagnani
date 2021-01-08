from random import randrange


def random_line():
    list_francais = open('src/liste_francais.txt', 'r', encoding="ISO-8859-1")
    line = next(list_francais)
    for num, aline in enumerate(list_francais, 2):
        if randrange(num):
            continue
        line = aline
    return line


def randomWords(nb):
    result = []
    for i in range(0, nb):
        result.append(random_line())
    return result
