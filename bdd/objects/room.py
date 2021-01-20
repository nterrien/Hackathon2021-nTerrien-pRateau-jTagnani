from bdd.objects.reservedObject import ReservedObject
from api.grrAPI import getRooms, addPlanning, reserveRoom

BASE_LABEL = "Room_"


roomList = []

def initRoomList ():
    global roomList
    roomList = []
    for id in range (4):
        roomList.append (Room (id))
    for id in getRooms():
        room = Room (id, external=True)
        roomList.append (room)
        addPlanning (room)


def addRoom (id):
    ''' Ajoute une salle à la liste et la renvoie. Renvois la salle correspondante si elle existe déjà'''
    try :
        return findRoom (id)
    except Exception as e:
        room = Room (id)
        roomList.append (room)
        return room

def findRoom (id):
    ''' Trouve la salle correspondant à l'id et cause une erreur si non trouvée '''
    id = int (id)
    l = filter (lambda r : r.index == id, roomList)
    return next(l)

def findRoomWith404 (id):
    ''' Trouve la salle correspondant à l'id et renvoie un 404 si non trouvée'''
    try :
        return findRoom (id)
    except Exception as e:
        print(e)
        abort(404)

class Room (ReservedObject):

    def __init__ (self, id, external=False):
        super().__init__(id, BASE_LABEL)
        self.external = external

    def reserve(self, dtStart, dtEnd):
        success = super().reserve(dtStart, dtEnd)
        if (success and self.external):
            return reserveRoom (self.index, dtStart, dtEnd)
        return success