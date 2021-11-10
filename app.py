from flask import Flask, request, jsonify
from flask_cors import CORS

from controller.booking import BaseBooking
from controller.user import BaseUser
from controller.room import BaseRoom

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello World"


# User
@app.route('/coqui-bookings/User/users', methods=['GET', 'POST'])
def handleUsers():
    if request.method == 'POST':
        return BaseUser().createNewUser(request.json)
    else:
        return BaseUser().getAllUsers()


@app.route('/coqui-bookings/User/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handleUserById(user_id):
    if request.method == 'GET':
        return BaseUser().getUserById(user_id)
    elif request.method == 'PUT':
        return BaseUser().updateUser(request.json)
    elif request.method == 'DELETE':
        return BaseUser().deleteUser(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


# Room
@app.route('/coqui-bookings/Room/rooms', methods=['GET', 'POST'])
def handleRooms():
    if request.method == 'POST':
        return BaseRoom().createNewRoom(request.json)
    else:
        return BaseRoom().getAllRooms()


@app.route('/coqui-bookings/Room/rooms/<int:room_id>', methods=['GET', 'PUT', 'DELETE'])
def handleRoomById(room_id):
    if request.method == 'GET':
        return BaseRoom().getRoomById(room_id)
    elif request.method == 'PUT':
        return BaseRoom().updateRoom(room_id, request.json)
    elif request.method == 'DELETE':
        return BaseRoom().deleteRoom(room_id)
    else:
        return jsonify("Method Not Allowed"), 405


# Booking
@app.route('/coqui-bookings/Booking/bookings', methods=['GET', 'POST'])
def handleBookings():
    if request.method == 'POST':
        return BaseBooking().createNewBooking(request.json)
    else:
        return BaseBooking().getAllBookings()


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>', methods=['GET', 'PUT', 'DELETE'])
def handleBookingById(booking_id):
    if request.method == 'GET':
        return BaseBooking().getBookingById(booking_id)
    elif request.method == 'PUT':
        return BaseBooking().updateBooking(booking_id, request.json)
    elif request.method == 'DELETE':
        return BaseBooking().deleteBooking(booking_id)
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == 'main':
    app.run()
