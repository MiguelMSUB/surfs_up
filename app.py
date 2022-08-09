#To import the Flask dependency
from flask import Flask

#create a new Flask app instance
#"Instance" is a general term in programming to refer to a singular version of something
app = Flask(__name__)

#First, we need to define the starting point, also known as the root
@app.route('/')
def hello_world():
    return 'Hello world'
