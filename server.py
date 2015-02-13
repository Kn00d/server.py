__author__ = 'KarlFredrik'

import random
import string
import json
import hashlib
from flask import request, jsonify, render_template, Flask
import database_helper
app = Flask(__name__)
database_helper.init_db(app)


logged_in_user = {}


@app.route('/')
def hello_world():
    return 'Hello World!'
#def home():
#   database_helper.get_db()
#  database_helper.init_db(app)
#    return render_template('client.html')


@app.route('/sign_in', methods=["POST"])
def signIn():
    # Signs in the user and gives them a string containing random generated token
    email = request.form['email']
    password = request.form['password']
    user = database_helper.get_user(email)
    print(user[1])
    print(user)
    if user == None:
        return 'User does not exist!'
    elif verifyPass(password, user[1]):
        token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
        logged_in_user[token] = email
        return json.dumps({'success': True, 'message': 'you logged in', 'data': token})
    else:
        return 'Wrong Password'


@app.route('/users')
def showUsers():
    #Fuction for showing all the users in the database
    users = database_helper.get_users()
    for row in users:
        print row
    return 'done'


@app.route('/sign_up', methods=["POST"])
# Registers user in database
def signUp():
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    if database_helper.user_exist(email):
        return jsonify(
            sucess=False,
            message="User already exists!")

    database_helper.add_user(email, password, firstname, familyname, gender, city, country)
    return jsonify(
        success=True,
        message="User successfully created!")


@app.route('/sign_out', methods=["POST"])
def signOut():
    # Signs you out
    token = request.form['token']
    try:
        if logged_in_user[token] != None:
            del logged_in_user[token]
            return json.dumps({'success': True, 'message': "User signed out!"})
    except Exception, e:
        return json.dumps({'success': False, 'message': 'you are not signed in'})


@app.route('/change_password', methods=["POST"])
def changePassword():
    # Changes a users password
    token = request.form['token']
    old_pass = request.form['oldpassword']
    new_pass = request.form['newpassword']
    try:
        email = logged_in_user[token]
    except Exception, e:
        return json.dumps({'success': False, 'message': 'you are not signed in'})
    info = database_helper.get_user(email)
    if verifyPass(old_pass, info[1]):
        hash_pass = hashPassword(new_pass)
        database_helper.change_password(email, hash_pass)
        return json.dumps({'success': True, 'message': 'password changed'})
    else:
        return json.dumps({'success': False, 'message': 'wrong password'})


@app.route('/get_user_data')
def getUserDataByToken():
    # Retrieves userdata from token
    token = request.args.get('token')
    try:
        email = logged_in_user[token]
    except Exception, e:
        return 'you are not signed in'
    info = database_helper.get_user(email)
    return json.dumps({'user: ': info})


@app.route('/get_user_data_email')
def getUserDataByEmail():
    # Returns a user object
    token = request.args.get('token')
    email = request.args.get('email')
    try:
        loggedInUser = logged_in_user[token]
    except Exception, e:
        return 'you are not signed in'
    if database_helper.user_exist(email):
        user = database_helper.get_user(email)
        return json.dumps({'user:': user})
    else:
        return 'no such user'


@app.route('/get_message_token')
def getUserMessagesByToken():
    # Returns an array containing all messages sent to user
    token = request.args.get('token')
    try:
        email = logged_in_user[token]
    except Exception, e:
        return 'you are not signed in'
    messages = database_helper.get_messages(email)
    return json.dumps({'messages': messages})


@app.route('/get_user_messages_by_email')
def getUserMessagesByEmail():
    # Same as above for the email-user
    token = request.args.get('token')
    email = request.args.get('email')
    try:
        logged_in_user = logged_in_user[token]
    except Exception, e:
        return 'you are not signed in'
    if database_helper.user_exist(email):
        messages = database_helper.get_messages(email)
        return json.dumps({'messages:': messages})
    else:
        return 'no such user'


@app.route('/post_message', methods=["POST"])
def postMessage():
    # Post a message
    token = request.form['token']
    message = request.form['message']
    to_email = request.form['email']
    try:
        from_email = logged_in_user[token]
    except Exception, e:
        return json.dumps({'success': False, 'message': 'you are not signed in'})
    if database_helper.user_exist(to_email):
        database_helper.add_message(to_email, from_email, message)
        return json.dumps({'success': True, 'message': 'message posted'})
    else:
        return json.dumps({'success': False, 'message': 'no such user'})


#def hashPassword(password):
#   hashedPass = hashlib.sha512(password).hexdigest()
#    return hashedPass



def verifyPass(password, hashedpass):
    return password == hashedpass

if __name__ == '__main__':
    app.run(debug=True)