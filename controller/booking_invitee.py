from flask import jsonify

from model.booking import BookingDAO
from model.booking_invitee import BookingInviteeDAO
from model.user import UserDAO


class BaseBookingInvitee:
    def build_booking_invitee_attr_dict(self, booking_id, user_id):
        result = {'booking_id': booking_id, 'user_id': user_id}
        return result

    def createNewInvitee(self, json):
        booking_id = json['booking_id']
        user_id = json['user_id']
        booking_dao = BookingDAO()
        existentBooking = booking_dao.getBookingById(booking_id)
        user_dao = UserDAO()
        existentUser = user_dao.getUserById(user_id)
        invitee_dao = BookingInviteeDAO()
        existentInvitee = invitee_dao.verifyInviteeInBooking(booking_id, user_id)

        if not existentBooking:
            return jsonify("Booking Not Found"), 404
        elif not existentUser:
            return jsonify("User Not Found"), 404
        elif not existentInvitee:
            invitee_dao.createNewInvitee(booking_id, user_id)
            result = self.build_booking_invitee_attr_dict(booking_id, user_id)
            return jsonify(result), 201
        else:
            return jsonify("Invitee is already in the Booking"), 409

