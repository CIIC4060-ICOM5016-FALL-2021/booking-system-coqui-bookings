from flask import Flask, request, jsonify
from flask_cors import CORS

from controller.booking import BaseBooking
from controller.booking_invitee import BaseBookingInvitee
from controller.user import BaseUser
from controller.room import BaseRoom

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Welcome to the Coqui Booking Calendar App Homepage"


# --------------------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------------------
@app.route('/coqui-bookings/User/users', methods=['GET', 'POST'])
def handleUsers():
    if request.method == 'POST':
        return BaseUser().createNewUser(request.json)
    elif request.method == 'GET':
        return BaseUser().getAllUsers()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/User/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handleUserById(user_id):
    if request.method == 'GET':
        return BaseUser().getUserById(user_id)
    elif request.method == 'PUT':
        return BaseUser().updateUser(user_id, request.json)
    elif request.method == 'DELETE':
        return BaseUser().deleteUser(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/User/role/<int:user_id>', methods=['GET'])
def handleUserRoleById(user_id):
    if request.method == 'GET':
        return BaseUser().getUserRoleById(user_id)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/coqui-bookings/User/users/<int:user_id>/schedule', methods=['GET'])
def handleUserSchedule(user_id):
    if request.method == 'GET':
        return BaseUser().getUserDaySchedule(user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/coqui-bookings/User/users/<int:user_id>/most_used_room', methods=['GET'])
def handleUserMostUsedRoom(user_id):
    if request.method == 'GET':
        return BaseUser().getMostUsedRoomByUserId(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Unavailable User
# --------------------------------------------------------------------------------------
@app.route('/coqui-bookings/User/unavailable-time-users', methods=['GET'])
def handleUnavailableTimeOfUsers():
    if request.method == 'GET':
        return BaseUser().getAllUnavailableTimeOfUsers()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/User/unavailable-time-users/<int:user_id>', methods=['GET'])
def handleUnavailableTimeOfUsersById(user_id):
    if request.method == 'GET':
        return BaseUser().getUnavailableTimeOfUserById(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/User/<int:user_id>/unavailable-time-slot/', methods=['POST'])
def handleUserAvailability(user_id):
    if request.method == 'POST':
        return BaseUser().createUserUnavailableTimeFrame(user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Room
# --------------------------------------------------------------------------------------
@app.route('/coqui-bookings/Room/rooms', methods=['GET', 'POST'])
def handleRooms():
    if request.method == 'POST':
        return BaseRoom().createNewRoom(request.json)
    elif request.method == 'GET':
        return BaseRoom().getAllRooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Room/rooms/verify', methods=['GET'])
def handleRoomVerifications():
    if request.method == 'GET':
        return BaseRoom().getAllAvailableRooms(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


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


@app.route('/coqui-bookings/Room/unavailable-time-rooms', methods=['GET'])
def handleUnavailableTimeOfRooms():
    if request.method == 'GET':
        return BaseRoom().getAllUnavailableTimeOfRooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Room/unavailable-time-rooms/<int:room_id>', methods=['GET'])
def handleUnavailableTimeOfRoomById(room_id):
    if request.method == 'GET':
        return BaseRoom().getUnavailableTimeOfRoomById(room_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Room/type/<int:room_id>', methods=['GET'])
def handleRoomType(room_id):
    if request.method == 'GET':
        return BaseRoom().getRoomTypeById(room_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Room/<int:room_id>/unavailable-time-slot/User/<int:user_id>', methods=['POST'])
def handleRoomAvailability(room_id, user_id):
    if request.method == 'POST':
        return BaseRoom().createRoomUnavailableTimeFrame(user_id, room_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Room/rooms/most_used_room', methods=['GET'])
def handleMostUsedRoom():
    if request.method == 'GET':
        return BaseRoom().getMostUsedRoom()
    else:
        return jsonify("Method Not Allowed"), 405

# --------------------------------------------------------------------------------------
# Booking
# --------------------------------------------------------------------------------------
@app.route('/coqui-bookings/Booking/bookings', methods=['GET'])
def handleBookings():
    if request.method == 'GET':
        return BaseBooking().getAllBookings()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def handleBookingById(booking_id):
    if request.method == 'GET':
        return BaseBooking().getBookingById(booking_id)
    elif request.method == 'PUT':
        return BaseBooking().updateBooking(booking_id, request.json)
    elif request.method == 'DELETE':
        return BaseBooking().deleteBooking(booking_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/user/<int:user_id>/create', methods=['POST'])
def handleBookingByUserId(user_id):
    if request.method == 'POST':
        return BaseBooking().createNewBooking(user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>/user/<int:user_id>/update', methods=['PUT'])
def handleBookingUpdate(booking_id, user_id):
    if request.method == 'PUT':
        return BaseBooking().updateBooking(booking_id, user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/coqui-bookings/Booking/bookings/busiest-times', methods=['GET'])
def handleBusiestTimes():
    if request.method == 'GET':
        return BaseBooking().getBusiestTimes()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/most-booked-users', methods=['GET'])
def handleMostBookedUsers():
    if request.method == 'GET':
        return BaseBooking().getMostBookedUsers()
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/coqui-bookings/Booking/bookings/most-booked-rooms', methods=['GET'])
def handleMostBookedRooms():
    if request.method == 'GET':
        return BaseBooking().getTop10MostBookedRooms()
    else:
        return jsonify("Method Not Allowed"), 405

# --------------------------------------------------------------------------------------
# Booking Invitee
# --------------------------------------------------------------------------------------
@app.route('/coqui-bookings/Booking/<int:booking_id>/BookingInvitee/bookingInvitees', methods=['POST', 'PUT'])
def handleBookingInviteesByBookingId(booking_id):
    if request.method == 'POST':
        return BaseBookingInvitee().createNewInvitee(booking_id, request.json)
    elif request.method == 'PUT':
        return BaseBookingInvitee().updateInvitees(booking_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/coqui-bookings/Booking/<int:booking_id>/BookingInvitee/bookingInvitees/delete/<int:invitee_id>',
           methods=['DELETE'])
def handleBookingInviteeDeletion(booking_id, invitee_id):
    if request.method == 'DELETE':
        return BaseBookingInvitee().deleteInvitee(booking_id, invitee_id)
    else:
        return jsonify("Method Not Allowed"), 405

# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
