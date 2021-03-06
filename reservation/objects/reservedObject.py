from bdd.dbMethods import addReservedObject, findAllReservationByObject, findAllReservationByObjectAndByTime, addReservation
from datetime import date, time, datetime, timedelta


class ReservedObject ():

    def __init__(self, id, baseLabel):
        self.index = str(id)
        self.label = baseLabel + str(id)
        addReservedObject(self.label)

    def findAll(self):
        return findAllReservationByObject(self.label)

    def checkDate(self, d):
        startDate = datetime.combine(d, time())
        endDate = startDate + timedelta(days=1)
        return findAllReservationByObjectAndByTime(self.label, startDate, endDate)

    def hasReservation(self, dtStart, dtEnd):
        return findAllReservationByObjectAndByTime(self.label, dtStart, dtEnd) != []

    def reserve(self, dtStart, duration, user):
        dtEnd = dtStart + duration
        if self.hasReservation(dtStart, dtEnd):
            print("déjà réservé")
            return False
        else:
            if dtEnd.date() != dtStart.date():
                current = dtStart
                while current.date() != dtEnd.date():
                    addReservation("automatic reservation",
                                   current, datetime.combine(current.date(), time(hour=23, minute=59)), self.label, user)
                    current += timedelta(days=1)
                    current = datetime.combine(current.date(), time(hour=0, minute=0))
                addReservation("automatic reservation", current, dtEnd, self.label, user)
            else:
                addReservation("automatic reservation",
                               dtStart, dtEnd, self.label, user)
            print(self.label + " réservé de " + dtStart.strftime("%d-%b-%Y (%H:%M:%S.%f)") +
                  " à " + dtEnd.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            return True
