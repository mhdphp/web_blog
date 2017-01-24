from flask import Flask

# tell python we are creating a flask application
# create a class of Flask
app = Flask(__name__) # __main__

# the end point will the forward slash after the api/
@app.route('/') # www.mysite/api/

# define a method that executes this end poit
def hello_world():
    return "Hello World...Romania"

# in order to work this app
if __name__ == '__main__':
    app.run()
    # we could other port
    # app.run(port=4000)

