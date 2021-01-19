from bdd.database import db
from bdd.models import Test, Category, Visitor, NameUsage



## Create
def addTest (name, category):
    test = Test(name=name, category=category)
    db.session.add(test)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter un test "
                "a cause de : %s" % e)
        db.session.rollback()
        return
    existCategory = findCategory (category)
    if (not existCategory):
        addCategory (category)

def addCategory (name):
    category = Category(name=name)
    db.session.add(category)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter une catégorie "
                "a cause de : %s" % e)
        db.session.rollback()

def addVisitor (name, usages):
    visitor = Visitor(name=name)
    db.session.add(visitor)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter un visiteur "
                "a cause de : %s" % e)
        db.session.rollback()
        return
    if not findNameUsage(name):
        for usage in usages:
            addNameUsage (name, usage['usage_full'], usage['usage_gender'])
    return visitor.id

def addNameUsage (name, usage, gender):
    nameUsage = NameUsage(name=name, usage=usage, gender=gender)
    db.session.add(nameUsage)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter un usage "
                "a cause de : %s" % e)
        db.session.rollback()


## Read
def findCategory (name):
    return Category.query.filter_by(name = name).first()

def findTest (id):
    return Test.query.filter_by(id = id).first()

def findAllCategories ():
    return Category.query.all()

def findTestsByCategory (categoryName):
    return Test.query.filter_by(category = categoryName).all()

def findVisitorById (id):
    return Visitor.query.filter_by(id = id).first()

def findAllVisitor ():
    return Visitor.query.all()

def findNameUsage (name):
    return NameUsage.query.filter_by(name=name).all()


## Update
def updateTest (id, name, category):
    test = findTest (id)
    test.name = name
    test.category = category
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas update un Test "
                "a cause de : %s" % e)
        db.session.rollback()


## Delete
def deleteTest (name):
    Test.query.filter_by(name = name).delete()
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas supprimer un Test "
                "a cause de : %s" % e)
        db.session.rollback()