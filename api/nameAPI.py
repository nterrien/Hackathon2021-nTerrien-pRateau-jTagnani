import requests

API_KEY = "ha856565906"
API_URL = "https://www.behindthename.com/api/lookup.json?key=" + API_KEY

def getNameInfos (name):
    url = API_URL + "&name=" + name
    result = requests.get(url)
    return result