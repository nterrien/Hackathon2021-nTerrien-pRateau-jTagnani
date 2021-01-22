import requests
from datetime import datetime


API_URL = "https://mockgrrapi.osc-fr1.scalingo.io"


def datetimeToString (dt):
    return dt.strftime ('%Y-%m-%d %H:%M')

def datetimeFromString (text):
    return datetime.strptime (text, '%Y-%m-%d %H:%M')

def getRooms ():
    url = API_URL + "/rooms"
    r = requests.get(url)
    result = r.json()
    return result['room_ids']

def getPlanning(room_id):
    url = API_URL + "/room/" + room_id + "/planning"
    r = requests.get(url)
    if r.status_code == 404:
        return False
    result = r.json()[room_id]
    for reservation in result :
        reservation['start_date'] =datetimeFromString (reservation['start_date'])
        reservation['end_date'] =datetimeFromString (reservation['end_date'])
    return result

def addPlanning (room):
    room_id = room.index
    reservationsToAdd = getPlanning(room_id)
    if (reservationsToAdd == False): return False
    for r in reservationsToAdd:
        dtStart = r['start_date']
        duration = r['end_date'] - dtStart
        room.reserve (dtStart, duration, r['user'])
    return True

def reserveRoom (room_id, startDate, endDate, user):
    data = {'start_date': datetimeToString (startDate), 'end_date': datetimeToString (endDate), 'user': user}
    url = API_URL + "/room/" + room_id + "/reserve"
    r = requests.get(url, data=data)
    if r.status_code == 404:
        return False
    return True
