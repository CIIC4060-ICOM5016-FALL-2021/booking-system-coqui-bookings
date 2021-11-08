from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.user import BaseUser

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello World"


if __name__ == 'main':
    app.run()


@app.route('/User/user', methods=['GET'])
def handleUsers():
    return BaseUser().getAllUsers()
