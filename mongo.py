from pymongo import Connection


def conn():
    connection = Connection('mongo2.stuycs.org')
    db = connection.admin
    res = db.authenticate('ml7','ml7')
    db = connection['pd7-poem']
    return db

def clearDB():
    db = conn()
    db.users.remove()
    db.poems.remove()

def addUser(user,password):
    db = conn()
    d = {'user':user, 'pass':password, 'poems':[]}
    r = db.users.find({'user':user})
    if r != None:
        db.users.insert(d)
        return user
    else:
        return None

def exists(user,password):
    db.conn()
    r = db.users.find({'user':user})
    if len(r) == 0:
        return False
    else:
        return True

def addPoem(user,poem):
    db = conn()
    d = db.users.find({'user':user})
    f = db.poems.find()
    d = d[0]
    li = d['poems']
    li.append(poem)

    r = [x for x in f]
    r.append(poem)
    k = {'poems':r}
    if f != None:
        db.poems.insert(k)
    else:
        db.poems.update({'poems':r},k)
    db.users.update({'user':user},d)

def getPoems(user):
    db = conn()
    d = db.users.find({'user':user})
    d = d[0]
    return d['poems']

def getAllPoems():
    db = conn()
    d = {'poems':[]}
    l = db.poems
    return l

if __name__ == '__main__':
    addPoem("Batya","this is a poem")
    addPoem("D","poem2")
    addPoem("Batya","poem3")
    addPoem("Batya","poem4")
    addPoem("D","poem5")
    
