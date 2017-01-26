from flask import Flask, render_template
from src.common.database import Database
from src.models.user import User

app = Flask(__name__)

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/profile')
def get_profile():
    user = User.get_by_email('test')
    password = user.password
    return render_template('profile.html', password=password)
    # return render_template('profile.html')


# in order to work this app
if __name__ == '__main__':
    app.run(port=5000)
    # we could set other port
    # app.run(port=4000)
