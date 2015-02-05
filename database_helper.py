__author__ = 'KarlFredrik'

import sqlite3
from flask import g
from contextlib import closing


DATABASE = 'database.db'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = str
    return conn

def init_db(app):
    with closing(connect_db()) as db:
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def getUsers():
    cur = get_db().cursor()
    query = 'SELECT * FROM users'
    cur.execute(query)
    result = cur.fetchall()
    return result

def testUserAdd():
    cur = get_db().cursor()
    query = 'INSERT INTO users (email, password, firstname, familyname, gender, city, country) VALUES("marre@lol.se", "123456", "lol", "lol", "male", "lol", "lol");'
    cur.execute(query)
    get_db().commit()


def addUser(email, password, firstname, familyname, gender, city, country):
    cur = get_db().cursor()
    query = 'INSERT INTO users (email, password, firstname, familyname, gender, city, country) VALUES(?, ?, ?, ?, ?, ?, ?);'
    cur.execute(query, [email, password, firstname, familyname, gender, city, country])
    get_db().commit()


def getUser(email):
    cur = get_db().cursor()
    query = 'SELECT * FROM USER AS U WHERE U.email = ?'
    cur.execute(query, [email])
    userInfo = cur.fetchone()
    return userInfo


def existsUser(email):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM user WHERE user.EMAIL = ?', [email])
    result = cur.fetchone()
    print result
    return (result != None)


def addMessage(toEmail, fromEmail, message):
    cur = get_db().cursor()
    query = 'INSERT INTO MESSAGE(toemail, fromemail, message) VALUES(?, ?, ?);'
    cur.execute(query, [toEmail, fromEmail, message])
    get_db().commit()


def changePassword(email, newPass):
    cur = get_db().cursor()
    query = 'UPDATE USER SET password = ? WHERE USER.EMAIL = ?;'
    cur.execute(query, [newPass, email])
    get_db().commit()


def getMessages(email):
    cur = get_db().cursor()
    query = 'SELECT * FROM MESSAGE WHERE MESSAGE.toemail=?;'
    cur.execute(query, [email])
    messages = cur.fetchall()
    return messages