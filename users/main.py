from sqlalchemy.engine import create_engine
from passlib.hash import sha256_crypt
import random

def dbconnect():
    engine = create_engine('mysql://drbalaji:password@localhost:3306/yourdb')
    connection = engine.connect()
    return connection


def dbclose(connection):
    connection.close()
    return


def getUser(token):
    connection = dbconnect()
    query = "SELECT * FROM sessiontable WHERE token=%s"
    args =(token)
    result = connection.execute(query,args)
    for row in result:
        username = row['username']
    query = "SELECT * FROM users WHERE username=%s"
    args = (username)
    result = connection.execute(query,args)
    if result:
        userObj = {}
        for row in result:
            userObj['username'] = row['username']
            userObj['email'] = row['email']
            userObj['mobile'] = row ['mobile']
        print(userObj)
        return userObj
    else:
        return -1


def getToken(username):
    connection= dbconnect()

    query = "SELECT * FROM sessiontable WHERE username=%s"
    args = (username)
    result = connection.execute(query,args)
    if result:
        query = "DELETE from sessiontable WHERE username=%s"
        args = (username)
        connection.execute(query, args)
    token = ''.join(random.choice("123456789abcdefghi") for i in range (5))
    print(token)
    query = "INSERT INTO sessiontable(username,token) VALUES (%s,%s)"
    args = (username,token)
    connection.execute(query,args)
    return token

def registerUser(username,email,mobile,password):
    connection = dbconnect()

    query = "SELECT * FROM users"
    result = connection.execute(query)
    for row in result:
        if username==row['username'] or email==row['email'] or mobile==row['mobile']:
            return -1
    query = "INSERT into users(username,email,mobile,password) VALUES (%s,%s,%s,%s)"
    hashpass = sha256_crypt.encrypt(password)
    args = (username,email,mobile,hashpass)
    connection.execute(query,args)
    dbclose(connection)
    return 1


def login(username,password):
    connection = dbconnect()
    query = "SELECT password from users WHERE username=%s"
    args = (username)
    result = connection.execute(query,args)
    for each in result:
        hashpass = each['password']
    check = sha256_crypt.verify(password, hashpass)
    if check == True:
        return getToken(username)
    else:
        return 0


def logout(token):
    connection = dbconnect()
    check = False
    query = "SELECT * FROM sessiontable"
    result = connection.execute(query)
    for each in result:
        if each['token'] == token:
            check = True
    if check == True:
        query = "DELETE from sessiontable WHERE token=%s"
        args = (token)
        connection.execute(query,args)
        return 1
    else:
        return -1

