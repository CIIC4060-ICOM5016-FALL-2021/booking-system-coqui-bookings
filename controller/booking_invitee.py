import datetime as dt
from flask import jsonify

from controller.user import BaseUser
from model.booking import BookingDAO
from model.booking_invitee import BookingInviteeDAO
from model.user import UserDAO


class BaseBookingInvitee:
    def build_booking_invitee_attr_dict(self, booking_id, user_id):
        result = {'booking_id': booking_id, 'user_id': user_id}
        return result

    def build_booking_invitee_list_attr_dict(self, booking_id, user_id):
        result = {'booking_id': booking_id, 'user_id': []}
        for uid in user_id:
            result['user_id'].append(uid)
        return result

    def createNewInvitee(self, booking_id, json):  # TODO Verify Conflicting Time and add unavailable time
        user_id = json['invitee_id']
        booking_dao = BookingDAO()
        existentBooking = booking_dao.getBookingById(booking_id)
        if not existentBooking:
            return jsonify("Booking Not Found"), 404
        bookingTimes = booking_dao.getBookingStartFinishTime(booking_id)
        user_dao = UserDAO()
        existentUser = user_dao.getUserById(user_id)
        if not existentUser:
            return jsonify("User Not Found"), 404

        if not BaseUser().verifyAvailableUserAtTimeFrame(user_id, dt.datetime.strftime(bookingTimes[0], '%Y-%m-%d %H:%M'),
                                                         dt.datetime.strftime(bookingTimes[1], '%Y-%m-%d %H:%M')):
            return jsonify("Invitee is not available during Booking Time"), 409

        invitee_dao = BookingInviteeDAO()
        if not invitee_dao.verifyInviteeInBooking(booking_id, user_id):
            invitee_dao.createNewInvitee(booking_id, user_id)
            user_dao.createUnavailableUserTimeFrame(user_id, bookingTimes[0], bookingTimes[1])
            result = self.build_booking_invitee_attr_dict(booking_id, user_id)
            return jsonify(result), 201
        else:
            return jsonify("Invitee is already in the Booking"), 409

    def updateInvitees(self, booking_id, json):
        user_id_list = json['invitee_id_list']
        user_dao = UserDAO()
        booking_dao = BookingDAO()
        invitee_dao = BookingInviteeDAO()
        bookingTime = booking_dao.getBookingStartFinishTime(booking_id)  # Returns a tuple with start and finish
        current_invitees = invitee_dao.getInviteesByBookingId(booking_id)  # Returns a list of current invitees

        for user_id in user_id_list:
            if not user_dao.getUserById(user_id):
                return jsonify("User Not Found"), 404

        for current_id in current_invitees:
            invitee_dao.deleteInvitee(booking_id, current_id)
            user_dao.deleteUnavailableUserTimeFrame(current_id, bookingTime[0], bookingTime[1])

        for user_id in user_id_list:  # Verify all users exist
            if not BaseUser().verifyAvailableUserAtTimeFrame(user_id, dt.datetime.strftime(bookingTime[0], '%Y-%m-%d %H:%M'),
                                                         dt.datetime.strftime(bookingTime[1], '%Y-%m-%d %H:%M')):
                for current_id in current_invitees:  # Rollback
                    invitee_dao.createNewInvitee(booking_id, current_id)
                    user_dao.createUnavailableUserTimeFrame(current_id, bookingTime[0], bookingTime[1])
                return jsonify("One or more Invitees are not available during Booking Time"), 409

        for user_id in user_id_list:
            invitee_dao.createNewInvitee(booking_id, user_id)
            user_dao.createUnavailableUserTimeFrame(user_id, bookingTime[0], bookingTime[1])

        result = self.build_booking_invitee_list_attr_dict(booking_id, user_id_list)
        return jsonify(result), 200
