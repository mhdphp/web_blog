from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User
from src.models.post import Post


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


# list the blogs belonging to an user or author
@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):

    # find the user either by user_id given or by email
    # stored in session
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    # get all the blogs associated with this user
    blogs = user.get_blogs()

    return render_template('user_blogs.html', blogs=blogs, email=user.email)


# list all the posts that are in a blog
@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', blog_title=blog.title, posts=posts)


# in order to work this app
if __name__ == '__main__':
    app.run(port=4995)
    # we could set other port
    # app.run(port=4000)

