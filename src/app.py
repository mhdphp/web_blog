from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.user import User


# tell python we are creating a flask application
# create a class of Flask
app = Flask(__name__)
# create a secret_key for session to be able to work
app.secret_key = "Mike is great"


# define the first end-point -- www/mysite.con/api/
@app.route('/')
def home_template():
    return render_template('home.html')


# define the second end-point -- www/mysite.com/api/login
@app.route('/login')
def login_template():
    # return 'Hello, world'
    return render_template('login.html')


# define another end-point -- www/mysite.com/api/register
@app.route('/register')
def registe_template():
    # return 'Hello, world'
    return render_template('register.html')



# we have to initialize the database
# use Flask dec
@app.before_first_request
def initialize_database():
    Database.initialize()


# define another end-point
# login user
@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    # check if email,and password match
    if User.login_valid(email, password):
        # if matched save the email in session
        User.login(email)
    else:
        session['email'] = None

    # redirect the user on a profile.html page, with email on the session saved
    return render_template('profile.html', email=session['email'], password=password)


# register user
@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('profile.html', email=session['email'])


# in order to work this app
if __name__ == '__main__':
    app.run(port=4995)
    # we could set other port
    # app.run(port=4000)

