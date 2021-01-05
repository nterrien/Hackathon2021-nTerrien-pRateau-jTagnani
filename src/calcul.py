from random import choice

wordList = ["Bonjour","Plante","Bonsoir","Chat","Tapis","Mot","Aléatoire"]

def randomWords(nb):
    result = []
    for i in range(0,nb):
        result.append(choice(wordList))
    return result