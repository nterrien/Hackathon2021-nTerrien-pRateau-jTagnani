import requests
from bdd.dbMethods import findNameUsage, addVisitor

API_KEY = "ha856565906"
API_URL = "https://www.behindthename.com/api/lookup.json?key=" + API_KEY

def getNameInfo (name):
    url = API_URL + "&name=" + name
    r = requests.get(url)
    result = r.json()
    if not result:
        name = result['name']
        usages = result['usages']
    else:
        usages = []
    addVisitor (name, usages)
    return findNameUsage(name)