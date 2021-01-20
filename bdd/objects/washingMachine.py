from bdd.dbMethods import addReservedObject, findAllReservationByObject, findAllReservationByObjectAndByTime, addReservation
from datetime import date, time, datetime, timedelta

class WashingMachine ():

    def __init__ (self, id):
        self.label = "WashingMachine_" + id
        self.duration = timedelta(minutes=45)
        addReservedObject (self.label)

    def findAll (self):
        return findAllReservationByObject(self.label)

    def checkDate (self, d):
        startDate = datetime.combine (d, time())
        endDate = startDate + timedelta(days=1)
        return findAllReservationByObjectAndByTime (self.label, startDate, endDate)

    def hasReservation (self, dtStart, dtEnd):
        return findAllReservationByObjectAndByTime (self.label, dtStart, dtEnd) != []

    def reserve (self, dtStart):
        dtEnd = dtStart + self.duration
        if self.hasReservation (dtStart, dtEnd):
            print ("déjà réservé")
        else :
            addReservation ("automatic reservation", dtStart, dtEnd, self.label)
            print ("réservé !")

