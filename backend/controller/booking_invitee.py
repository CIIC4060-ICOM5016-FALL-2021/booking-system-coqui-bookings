import datetime as dt
from flask import jsonify

from backend.controller.user import BaseUser
from backend.model.booking import BookingDAO
from backend.model.booking_invitee import BookingInviteeDAO
from backend.model.user import UserDAO

# CONSTANT VALUES IN DATABASE
PROFESSOR_ROLE = 1
STUDENT_ROLE = 2
STAFF_ROLE = 3

LAB_TYPE = 1
CLASSROOM_TYPE = 2
STUDY_SPACE_TYPE = 3


class BaseBookingInvitee:
    def build_booking_invitee_attr_dict(self, booking_id, user_id):
        result = {'booking_id': booking_id, 'user_id': user_id}
        return result

    def build_booking_invitee_list_attr_dict(self, booking_id, user_id):
        result = {'booking_id': booking_id, 'user_id': []}
        for uid in user_id:
            result['user_id'].append(uid)
        return result

    def build_invitee_full_attr_dict(self, booking_id, user_id, user_email, user_password, user_first_name,
                                     user_last_name, role_id):
        result = {'booking_id': booking_id, 'user_id': user_id, 'user_email': user_email,
                  'user_password': user_password,
                  'user_first_name': user_first_name, 'user_last_name': user_last_name, 'role_id': role_id}
        return result

    def build_invitee_full_stud_attr_dict(self, booking_id, user_email, user_first_name, user_last_name):
        result = {'booking_id': booking_id, 'user_email': user_email, 'user_first_name': user_first_name,
                  'user_last_name': user_last_name}
        return result

    def createNewInvitee(self, booking_id, json):
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

        if not BaseUser().verifyAvailableUserAtTimeFrame(user_id,
                                                         dt.datetime.strftime(bookingTimes[0], '%Y-%m-%d %H:%M'),
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

    def getAllInviteesOfAllBooking(self, user_id):
        user_dao = UserDAO()
        if not user_dao.getUserById(user_id):
            return jsonify("User Not Found"), 404
        role = user_dao.getUserRoleById(user_id)[0]
        invitee_dao = BookingInviteeDAO()
        booking_dao = BookingDAO()
        all_bookings = booking_dao.getAllBookings()
        result_list = []
        for booking in all_bookings:
            booking_id = booking[0]
            room_type = booking_dao.getBookingRoomTypeFromId(booking_id)[0]
            if role == STAFF_ROLE or (role == PROFESSOR_ROLE and room_type == CLASSROOM_TYPE):
                invitee_list = invitee_dao.getInviteesByBookingIdAdminLevel(booking_id)
                for invitee in invitee_list:
                    obj = self.build_invitee_full_attr_dict(booking_id, invitee[0], invitee[1], invitee[2], invitee[3],
                                                            invitee[4], invitee[5])
                    result_list.append(obj)
            elif role == STUDENT_ROLE and room_type == STUDY_SPACE_TYPE:
                invitee_list = invitee_dao.getInviteesByBookingIdStudentLevel(booking_id)
                for invitee in invitee_list:
                    obj = self.build_invitee_full_stud_attr_dict(booking_id, invitee[0], invitee[1], invitee[2])
                    result_list.append(obj)
            else:
                continue
        if role == PROFESSOR_ROLE or role == STUDENT_ROLE:
            return jsonify("Some information can't be shown because you do not have permission to access",
                           result_list), 200
        else:
            return jsonify(result_list), 200

    def getInviteesByBookingId(self, booking_id, user_id):
        booking_dao = BookingDAO()
        invitee_dao = BookingInviteeDAO()
        user_dao = UserDAO()

        if not booking_dao.getBookingById(booking_id):
            return jsonify("Booking Not Found"), 404
        if not user_dao.getUserById(user_id):
            return jsonify("User Not Found"), 404

        role = user_dao.getUserRoleById(user_id)[0]
        room_type = booking_dao.getBookingRoomTypeFromId(booking_id)[0]

        if role == STAFF_ROLE or (role == PROFESSOR_ROLE and room_type == CLASSROOM_TYPE):
            invitee_list = invitee_dao.getInviteesByBookingIdAdminLevel(booking_id)
            result_list = []
            for invitee in invitee_list:
                obj = BaseUser().build_user_map_dict(invitee)
                result_list.append(obj)
            if len(result_list) == 0:
                return jsonify("Invitees Not Found"), 404
            else:
                return jsonify(result_list), 200
        elif role == STUDENT_ROLE and room_type == STUDY_SPACE_TYPE:
            invitee_list = invitee_dao.getInviteesByBookingIdStudentLevel(booking_id)
            result_list = []
            for invitee in invitee_list:
                obj = BaseUser().build_user_student_map_dict(invitee)
                result_list.append(obj)
            if len(result_list) == 0:
                return jsonify("Invitees Not Found"), 404
            else:
                return jsonify("Some information can't be shown because you do not have permission to access",
                               result_list), 200
        else:
            return jsonify(
                f"User with role {role} does not have permission to view information about room type {room_type}"), 403

    def getInviteUserHasBeenMostBookedWith(self, user_id):
        dao = UserDAO()
        booked_invitees = dao.getInviteeUserHasBeenMostBookedWith(user_id)
        if len(booked_invitees) == 0:
            return jsonify("User has not been booked with any invitee "), 404
        else:
            most_booked_invitee = dao.getUserById(booked_invitees[0][1])
            return jsonify(BaseUser().build_user_map_dict(most_booked_invitee)), 200

    def updateInvitees(self, booking_id, json):
        user_id_list = json['invitee_id_list']
        user_dao = UserDAO()
        booking_dao = BookingDAO()
        invitee_dao = BookingInviteeDAO()
        bookingTime = booking_dao.getBookingStartFinishTime(booking_id)  # Returns a tuple with start and finish
        current_invitees = invitee_dao.getInviteesByBookingIdAdminLevel(
            booking_id)  # Returns a list of current invitees

        for user_id in user_id_list:
            if not user_dao.getUserById(user_id):
                return jsonify("User Not Found"), 404

        for current_id in current_invitees:
            invitee_dao.deleteInvitee(booking_id, current_id[0])
            user_dao.deleteUnavailableUserTimeFrame(current_id[0], bookingTime[0], bookingTime[1])

        for user_id in user_id_list:  # Verify all users exist
            if not BaseUser().verifyAvailableUserAtTimeFrame(user_id,
                                                             dt.datetime.strftime(bookingTime[0], '%Y-%m-%d %H:%M'),
                                                             dt.datetime.strftime(bookingTime[1], '%Y-%m-%d %H:%M')):
                for current_id in current_invitees:  # Rollback
                    invitee_dao.createNewInvitee(booking_id, current_id[0])
                    user_dao.createUnavailableUserTimeFrame(current_id[0], bookingTime[0], bookingTime[1])
                return jsonify("One or more Invitees are not available during Booking Time"), 409

        for user_id in user_id_list:
            invitee_dao.createNewInvitee(booking_id, user_id)
            user_dao.createUnavailableUserTimeFrame(user_id, bookingTime[0], bookingTime[1])

        result = self.build_booking_invitee_list_attr_dict(booking_id, user_id_list)
        return jsonify(result), 200

    def deleteInvitee(self, booking_id, invitee_id):
        invitee_dao = BookingInviteeDAO()
        booking_dao = BookingDAO()
        user_dao = UserDAO()
        if not booking_dao.getBookingById(booking_id):
            return jsonify("Booking Not Found"), 404
        if not user_dao.getUserById(invitee_id):
            return jsonify("Invitee Not Found"), 404
        if not invitee_dao.verifyInviteeInBooking(booking_id, invitee_id):
            return jsonify("Invitee is not in the Booking"), 409
        invitee_dao.deleteInvitee(booking_id, invitee_id)
        bookingTime = booking_dao.getBookingStartFinishTime(booking_id)
        user_dao.deleteUnavailableUserTimeFrame(invitee_id, bookingTime[0], bookingTime[1])
        return jsonify("Invitee Deleted Successfully"), 200
