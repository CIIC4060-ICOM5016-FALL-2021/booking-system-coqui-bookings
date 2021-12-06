from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.controller.booking import BaseBooking
from backend.controller.booking_invitee import BaseBookingInvitee
from backend.controller.user import BaseUser
from backend.controller.room import BaseRoom

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
        return BaseUser().deleteUserbyUser(user_id)
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


@app.route('/coqui-bookings/User/users/login', methods=['POST'])
def verifyUserLogin():
    if request.method == 'POST':
        return BaseUser().verifyLogin(request.json)
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


@app.route('/coqui-bookings/User/users/free-time-for-users', methods=['POST'])
def handleFreeTimeForUsers():
    if request.method == 'POST':
        return BaseUser().getFreeTimeForUsers(request.json)
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


@app.route('/coqui-bookings/Room/rooms/verifytimeframe', methods=['POST'])
def handleRoomVerifications():
    if request.method == 'POST':
        return BaseRoom().getAllAvailableRoomsAtTimeFrame(request.json)
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


@app.route('/coqui-bookings/Room/rooms/<int:room_id>/schedule', methods=['GET'])
def handleRoomSchedule(room_id):
    if request.method == 'GET':
        return BaseRoom().getRoomDaySchedule(room_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Booking
# --------------------------------------------------------------------------------------
@app.route('/coqui-bookings/Booking/bookings/all/user/<int:user_id>', methods=['GET'])
def handleGetAllBookings(user_id):
    if request.method == 'GET':
        return BaseBooking().getAllBookings(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/User/<int:user_id>/Booking/bookings/<int:booking_id>', methods=['DELETE'])
def handleBookingById(booking_id, user_id):
    if request.method == 'DELETE':
        return BaseBooking().deleteBookingByHost(booking_id, user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>/User/<int:user_id>/update', methods=['PUT'])
def handleBookingByIdWithRole(booking_id, user_id):
    if request.method == 'PUT':
        return BaseBooking().updateBooking(booking_id, user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>/updateName', methods=['PUT'])
def handleBookingByName(booking_id):
    if request.method == 'PUT':
        return BaseBooking().updateBookingName(booking_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>/User/<int:user_id>/get', methods=['GET'])
def handleGetBookingById(booking_id, user_id):
    if request.method == 'GET':
        return BaseBooking().getBookingById(booking_id, user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/user/<int:user_id>/create', methods=['POST'])
def handleBookingByUserId(user_id):
    if request.method == 'POST':
        return BaseBooking().createNewBooking(user_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/User/TimeFrame/<int:room_id>', methods=['POST'])
def handleWhoAppointedRoom(room_id):
    if request.method == 'POST':
        return BaseBooking().getUserBookedRoomAtTimeFrame(room_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/busiest-times', methods=['GET'])
def handleBusiestTimes():
    if request.method == 'GET':
        return BaseBooking().getTop5BusiestTimes()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/most-booked-users', methods=['GET'])
def handleMostBookedUsers():
    if request.method == 'GET':
        return BaseBooking().getTop10MostBookedUsers()
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


@app.route('/coqui-bookings/User/<int:user_id>/Booking/<int:booking_id>/BookingInvitee/bookingInvitees/delete/<int:invitee_id>',
           methods=['DELETE'])
def handleBookingInviteeDeletion(booking_id, invitee_id, user_id):
    if request.method == 'DELETE':
        return BaseBookingInvitee().deleteInviteebyHost(booking_id, invitee_id, user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/<int:booking_id>/user/<int:user_id>/BookingInvitee/information',
           methods=['GET'])
def handleBookingInviteesByUserID(booking_id, user_id):
    if request.method == 'GET':
        return BaseBookingInvitee().getInviteesByBookingId(booking_id, user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/Booking/bookings/all/user/<int:user_id>/BookingInvitee/information', methods=['GET'])
def handleAllBookingInviteesByUserId(user_id):
    if request.method == 'GET':
        return BaseBookingInvitee().getAllInviteesOfAllBooking(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/coqui-bookings/User/users/<int:user_id>/invitee-most-booked-with', methods=['GET'])
def handleInviteeUserHasBeenMostBookedWith(user_id):
    if request.method == 'GET':
        return BaseUser().getInviteUserHasBeenMostBookedWith(user_id)
    else:
        return jsonify("Method Not Allowed"), 405


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------
if __name__ == 'main':
    app.run()
