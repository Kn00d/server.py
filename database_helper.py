from contextlib import closing
import sqlite3

__author__ = 'KarlFredrik'

import flask

DATABASE = 'database.db'


def get_db():
    db = getattr(flask.g, 'db', None)
    if db is None:
        db = flask.g.db = connect_db()
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

def get_users():
    cur = get_db().cursor()
    query = 'SELECT * FROM users'
    cur.execute(query)
    result = cur.fetchall()
    return result


def add_user(email, password, firstname, familyname, gender, city, country):
    cur = get_db().cursor()
    query = 'INSERT INTO users (email, password, firstname, familyname, gender, city, country) VALUES(?, ?, ?, ?, ?, ?, ?);'
    cur.execute(query, [email, password, firstname, familyname, gender, city, country])
    get_db().commit()


def get_user(email):
    cur = get_db().cursor()
    query = 'SELECT * FROM USER AS U WHERE U.email = ?'
    cur.execute(query, [email])
    userInfo = cur.fetchone()
    return userInfo


def user_exist(email):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM user WHERE user.EMAIL = ?', [email])
    result = cur.fetchone()
    print result
    return (result != None)


def add_message(toEmail, fromEmail, message):
    cur = get_db().cursor()
    query = 'INSERT INTO MESSAGE(toemail, fromemail, message) VALUES(?, ?, ?);'
    cur.execute(query, [toEmail, fromEmail, message])
    get_db().commit()


def change_password(email, newPass):
    cur = get_db().cursor()
    query = 'UPDATE USER SET password = ? WHERE USER.EMAIL = ?;'
    cur.execute(query, [newPass, email])
    get_db().commit()


def get_messages(email):
    cur = get_db().cursor()
    query = 'SELECT * FROM MESSAGE WHERE MESSAGE.toemail=?;'
    cur.execute(query, [email])
    messages = cur.fetchall()
    return messages