__author__ = 'KarlFredrik'

import random
import string
import json
import hashlib
from flask import request, jsonify, render_template, Flask
import database_helper
app = Flask(__name__)
db = 'database_helper(app)'

loggedInUsers = {}


@app.route('/')
def hello_world():
    return 'Hello World!'
#def home():
#   database_helper.get_db()
#  database_helper.init_db(app)
#    return render_template('client.html')


@app.route('/signin', methods=["POST"])
def signIn():
    # Authenticates user, returns string containing random generated token
    email = request.form['email']
    password = request.form['password']
    user = database_helper.getUser(email)
    if user == None:
        return 'User does not exist!'
    elif verifyPass(password, user[1]):
        token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        loggedInUsers[token] = email
        return json.dumps({'success': True, 'message': 'you logged in', 'data': token})
    else:
        return 'Wrong Password'


@app.route('/users')
def showUsers():
    # Logfunction, shows all users
    users = database_helper.getUsers()
    for row in users:
        print row
    return 'done'


@app.route('/signup', methods=["POST"])
# Registers user in database
def signUp():
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    if db.user_xist(email):
        return jsonify(
            sucess=False,
            message="User already exists!")

    db.add_user(email, password, firstname, familyname, gender, city, country)
    return jsonify(
        success=True,
        message="User successfully created!")


@app.route('/signout', methods=["POST"])
def signOut():
    # Signs you out!
    token = request.form['token']
    try:
        if loggedInUsers[token] != None:
            del loggedInUsers[token]
            return json.dumps({'success': True, 'message': "User signed out!"})
    except Exception, e:
        return json.dumps({'success': False, 'message': 'you are not signed in'})


@app.route('/changepassword', methods=["POST"])
def changePassword():
    # Changes a users password
    token = request.form['token']
    oldPass = request.form['oldpassword']
    newPass = request.form['newpassword']
    try:
        email = loggedInUsers[token]
    except Exception, e:
        return json.dumps({'success': False, 'message': 'you are not signed in'})
    info = database_helper.getUser(email)
    if verifyPass(oldPass, info[1]):
        hashPass = hashPassword(newPass)
        database_helper.changePassword(email, hashPass)
        return json.dumps({'success': True, 'message': 'password changed'})
    else:
        return json.dumps({'success': False, 'message': 'wrong password'})


@app.route('/getuserdata')
def getUserDataByToken():
    # Retrieves userdata from token
    token = request.args.get('token')
    try:
        email = loggedInUsers[token]
    except Exception, e:
        return 'you are not signed in'
    info = database_helper.getUser(email)
    return json.dumps({'user: ': info})


@app.route('/getuserdataemail')
def getUserDataByEmail():
    # Returns a user object
    token = request.args.get('token')
    email = request.args.get('email')
    try:
        loggedInUser = loggedInUsers[token]
    except Exception, e:
        return 'you are not signed in'
    if database_helper.existsUser(email):
        user = database_helper.getUser(email)
        return json.dumps({'user:': user})
    else:
        return 'no such user'


@app.route('/getmessagetoken')
def getUserMessagesByToken():
    # Returns an array containing all messages sent to user
    token = request.args.get('token')
    try:
        email = loggedInUsers[token]
    except Exception, e:
        return 'you are not signed in'
    messages = database_helper.getMessages(email)
    return json.dumps({'messages': messages})


@app.route('/getmessageemail')
def getUserMessagesByEmail():
    # Same as above for the email-user
    token = request.args.get('token')
    email = request.args.get('email')
    try:
        loggedInUser = loggedInUsers[token]
    except Exception, e:
        return 'you are not signed in'
    if database_helper.existsUser(email):
        messages = database_helper.getMessages(email)
        return json.dumps({'messages:': messages})
    else:
        return 'no such user'


@app.route('/postmessage', methods=["POST"])
def postMessage():
    # Post a message
    token = request.form['token']
    message = request.form['message']
    email = request.form['email']
    try:
        fromEmail = loggedInUsers[token]
    except Exception, e:
        return json.dumps({'success': False, 'message': 'you are not signed in'})
    if email == None:
        toEmail = fromEmail
    else:
        toEmail = email
    if database_helper.existsUser(toEmail):
        database_helper.addMessage(toEmail, fromEmail, message)
        return json.dumps({'success': True, 'message': 'message posted'})
    else:
        return json.dumps({'success': False, 'message': 'no such user'})


def hashPassword(password):
    hashedPass = hashlib.sha512(password).hexdigest()
    return hashedPass


def verifyPass(password, hashedPass):
    reHashed = hashPassword(password)
    return reHashed == hashedPass


if __name__ == '__main__':
    app.run(debug=True)