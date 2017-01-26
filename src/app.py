from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.user import User


# tell python we are creating a flask application
# create a class of Flask
app = Flask(__name__)
# create a secret_key for session to be able to work
app.secret_key = "adfaDSADFa233r423sdfa"


# define the first end-point
@app.route('/')
def hello_world():
    # return 'Hello, world'
    return render_template('login.html')


# we have to initialize the database
# use Flask dec
@app.before_first_request
def initialize_database():
    Database.initialize()


# define another end-point
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    # check if email,and password match
    if User.login_valid(email, password):
        # if matched save the email in session
        User.login(email)

    # redirect the user on a profile.html page, with email on the session saved
    return render_template('profile.html', email=session['email'])


# in order to work this app
if __name__ == '__main__':
    app.run(port=4995)
    # we could set other port
    # app.run(port=4000)

