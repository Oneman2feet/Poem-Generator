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

def addUser(user,password):
    db = conn()
    d = {'user':user, 'pass':password, 'poems':[]}
    db.users.insert(d)

def addPoem(user,poem):
    db = conn()
    d = db.users.find({'user':user})
    d = d[0]
    li = d['poems']
    li.append(poem)
    db.users.update({'user':user},d)

def getPoems(user):
    db = conn()
    d = db.users.find({'user':user})
    d = d[0]
    return d['poems']


if __name__ == '__main__':
    addUser("batya","batya")
    getPoems("batya")
    addPoem("batya","this is a poem")
    print getPoems("batya")
