import requests
from bdd.dbMethods import findNameUsage, addVisitor

API_KEY = "ha856565906"
API_URL = "https://www.behindthename.com/api/lookup.json?key=" + API_KEY

def saveNameInfo (name):
    bddResult = findNameUsage(name)
    if not bddResult:
        requestNameInfo(name)


def requestNameInfo (name):
    url = API_URL + "&name=" + name
    r = requests.get(url)
    result = r.json()
    if type(result) == type([]):
        usages = result[0]['usages']
    else:
        usages = []
    addVisitor (name, usages)