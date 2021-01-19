from bdd.database import db
from bdd.models import Reservation, ReservedObject, User



## Create
def addReservation (name, start, end, label):
    reservation = Reservation (name=name, start=start, end=end, object=label)
    db.session.add (reservation)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter de réservation "
                "a cause de : %s" % e)
        db.session.rollback()

def addReservedObject (label):
    object = ReservedObject (label=label)
    db.session.add (object)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter d'object à réserver "
                "a cause de : %s" % e)
        db.session.rollback()

def addUser (username, password):
    user = User (username=username, password=password)
    db.session.add (user)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter d'utilisateur "
                "a cause de : %s" % e)
        db.session.rollback()


## Read
def findReservation (id):
    return Reservation.query.filter_by(id = id).first()

def findAllReservation ():
    return Reservation.query.all()

def findAllReservationByObject (object):
    return Reservation.query.filter_by(object = object).all()

def findAllReservationByObjectAndByTime (object, timeStart, timeEnd):
    return Reservation.query.filter_by(object = object).filter(Reservation.end > timeStart, Reservation.start < timeEnd).all()

def findUser (username):
    return User.query.filter_by(username = username).first()


## Update
def updateReservation (id, name, start, end):
    reservation = findReservation (id)
    reservation.name = name
    reservation.start = start
    reservation.end = end
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas update une Reservation "
                "a cause de : %s" % e)
        db.session.rollback()

def updateUser (user, username, password):
    user.username = username
    user.password = password
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas update un Utilisateur "
                "a cause de : %s" % e)
        db.session.rollback()


## Delete
def deleteReservation (id):
    Reservation.query.filter_by(id = id).delete()
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas supprimer une Reservation "
                "a cause de : %s" % e)
        db.session.rollback()
