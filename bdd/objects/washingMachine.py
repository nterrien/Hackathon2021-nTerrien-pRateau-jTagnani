from bdd.objects.reservedObject import ReservedObject
from datetime import timedelta
from flask import abort

BASE_LABEL = "WashingMachine_"
DURATION = 45


machineList = []

def initWashingMachineList ():
    global machineList
    machineList = []
    for id in range (4):
        machineList.append (WashingMachine (id))

def addWashingMachine (id):
    ''' Ajoute une machine à laver à la liste et la renvoie. Renvoie la machine correspondante si elle existe déjà'''
    try :
        return findMachine (id)
    except Exception as e:
        machine = WashingMachine (id)
        machineList.append (machine)
        return machine

def findMachine (id):
    ''' Trouve la machine correspondant à l'id et cause une erreur si non trouvée '''
    id = int (id)
    l = filter (lambda m : m.index == id, machineList)
    return next(l)

def findMachineWith404 (id):
    ''' Trouve la machine correspondant à l'id et renvoie un 404 si non trouvée'''
    try :
        return findMachine (id)
    except Exception as e:
        print(e)
        abort(404)

def getMachineList ():
    return machineList


class WashingMachine (ReservedObject):

    def __init__ (self, id):
        super().__init__(id, BASE_LABEL)
        self.duration = timedelta(minutes=DURATION)

    def reserve (self, dtStart):
        dtEnd = dtStart + self.duration
        return super().reserve (dtStart, dtEnd)
