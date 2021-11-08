from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.user import BaseUser

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello World"


@app.route('/User/users', methods=['GET'])
def handleUsers():
    return BaseUser().getAllUsers()


if __name__ == 'main':
    app.run()
