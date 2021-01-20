from bdd.objects.reservedObject import ReservedObject

BASE_LABEL = "Room_"


class Room (ReservedObject):

    def __init__ (self, id):
        super().__init__(id, BASE_LABEL)