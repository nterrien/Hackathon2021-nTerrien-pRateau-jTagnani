from bdd.database import db
from bdd.models import Reservation, ReservedObject, User



## Create
def addReservation (name, start, end, object, user):
    reservation = Reservation (name=name, start=start, end=end, object=object, user=user)
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

def findReservationByUser (user):
    return Reservation.query.filter_by(user = user).all()

def findAllReservationByObject (object):
    return Reservation.query.filter_by(object = object).order_by(Reservation.start).all()

def findAllReservationByObjectAndByTime (object, timeStart, timeEnd):
    return Reservation.query.filter_by(object = object).filter(Reservation.end > timeStart, Reservation.start < timeEnd).order_by(Reservation.start).all()

def findUser (username):
    return User.query.filter_by(username = username).first()


## Update
def updateReservation (reservation,name=None, start=None, end=None, object=None, user=None):
    if name != None: reservation.name = name
    if start != None: reservation.start = start
    if end != None: reservation.end = end
    if object != None: reservation.object = object
    if user != None: reservation.user = user
    print ("l'utilisateur est maintenant " + user)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas update une Reservation "
                "a cause de : %s" % e)
        db.session.rollback()

def updateUser (user, username=None, password=None):
    if username != None:
        for reservation in findReservationByUser (user.username):
            updateReservation (reservation, user=username)
        user.username = username
    if password != None: user.password = password
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
