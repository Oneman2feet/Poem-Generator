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
    d = {'user':user, 'pass':password, 'poems':[""]}
    r = db.users.find({'user':user})
    if r != None:
        db.users.insert(d)
        return user
    else:
        return None

def exists(user,password):
    db = conn()
    r = db.users.find({'user':user})
    if r == None:
        return False
    else:
        return True

def addPoem(user,poem):
    db = conn()
    d = [x for x in db.users.find({'user':user})]
    f = [x for x in db.poems.find()]
    if len(d) > 0:
        d = d[0]
        li = d['poems']
        li.append(poem)
        db.users.update({'user':user},d)
    else:
        d = {'user':user,'poems':[poem]}
        db.users.insert(d)

    
    db.poems.insert({'user':user,'poem':poem})


def getPoems(user):
    db = conn()
    d = [x for x in db.users.find({'user':user})]
    if len(d) > 0:
        return d[0]['poems']
    else:
        return [""]

def getAllPoems():
    db = conn()
    d = {'poems':[]}
    l = [x for x in db.poems.find()]
    r = [x['poem'] for x in l]
    return r

if __name__ == '__main__':
    clearDB()
    
