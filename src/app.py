from flask import Flask, render_template, request, session
from src.models.user import User


# tell python we are creating a flask application
# create a class of Flask
app = Flask(__name__) # __main__

# define the first end-point
@app.route('/')
def hello_world():
    # return 'Hello, world'
    return render_template('login.html')


# define another end-point
@app.route('/login')
def login_user():
    email = request.form['email']
    password = request.form['password']

    # check if email,and password match
    if User.login_valid(email, password):
        # if matched save the email in session
        User.login(email)

    # redirect the user on a profile.html page, with email on the session saved
    return render_template('profile.html', email = session['email'])



# in order to work this app
if __name__ == '__main__':
    app.run()
    # we could other port
    # app.run(port=4000)

