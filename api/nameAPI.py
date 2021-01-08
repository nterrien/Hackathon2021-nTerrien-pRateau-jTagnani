import requests
from bdd.dbMethods import findNameUsage, addVisitor

API_KEY = "ha856565906"
API_URL = "https://www.behindthename.com/api/lookup.json?key=" + API_KEY

# ici la méthode doit retourner l'id du visiteur

def saveNameInfo (name):
    bddResult = findNameUsage(name)
    usages = []
    if not bddResult:
        usages = requestNameInfo(name)
    return addVisitor (name, usages)


def requestNameInfo (name):
    url = API_URL + "&name=" + name
    r = requests.get(url)
    result = r.json()
    if type(result) == type([]):
        return result[0]['usages']
    else:
        return []