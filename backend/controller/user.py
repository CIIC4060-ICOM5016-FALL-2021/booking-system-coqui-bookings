import datetime as dt
from flask import jsonify

from backend.controller.room import BaseRoom
from backend.model.booking import BookingDAO
from backend.model.booking_invitee import BookingInviteeDAO
from backend.model.room import RoomDAO
from backend.model.user import UserDAO


class BaseUser:
    def build_user_map_dict(self, row):
        result = {'user_id': row[0], 'user_email': row[1], 'user_password': row[2], 'user_first_name': row[3],
                  'user_last_name': row[4], 'role_id': row[5]}
        return result

    def build_user_student_map_dict(self, row):
        result = {'user_email': row[0], 'user_first_name': row[1], 'user_last_name': row[2]}
        return result

    def build_user_attr_dict(self, user_id, user_email, user_password, user_first_name, user_last_name, role_id):
        result = {'user_id': user_id, 'user_email': user_email, 'user_password': user_password,
                  'user_first_name': user_first_name, 'user_last_name': user_last_name, 'role_id': role_id}
        return result

    def build_role_map_dict(self, user_role):
        result = {'role_id': user_role}
        return result

    def build_unavailable_time_user_map_dict(self, row):
        result = {'unavailable_time_user_id': row[0],
                  'unavailable_time_user_start': dt.datetime.strftime(row[1], '%Y-%m-%d %H:%M') + " AST",
                  'unavailable_time_user_finish': dt.datetime.strftime(row[2], '%Y-%m-%d %H:%M') + " AST",
                  'user_id': row[3]}
        return result

    def build_time_slot_attr_dict(self, start_time, finish_time):
        result = {'start_time': dt.datetime.strftime(start_time, '%Y-%m-%d %H:%M') + " AST",
                  'finish_time': dt.datetime.strftime(finish_time, '%Y-%m-%d %H:%M') + " AST"}
        return result

    def build_time_slot_marked_as_busy(self, start_time, finish_time):
        result = {'start_time': dt.datetime.strftime(start_time, '%Y-%m-%d %H:%M') + " AST",
                  'finish_time': dt.datetime.strftime(finish_time, '%Y-%m-%d %H:%M') + " AST",
                  'reason': "Marked as busy by User"}
        return result

    def build_booking_map_dict_with_room(self, row):
        result = {'booking_id': row[0], 'booking_name': row[1],
                  'booking_start': dt.datetime.strftime(row[2], '%Y-%m-%d %H:%M') + " AST",
                  'booking_finish': dt.datetime.strftime(row[3], '%Y-%m-%d %H:%M') + " AST",
                  'organizer_id': row[4], 'room_id': row[5], 'room_name': row[6]}
        return result

    # Create
    def createNewUser(self, json):
        user_email = json['user_email']
        user_password = json['user_password']
        user_first_name = json['user_first_name']
        user_last_name = json['user_last_name']
        role_id = json['role_id']
        dao = UserDAO()
        existing_user = dao.getUserByEmail(user_email)
        if not existing_user:  # User with that email does not exists
            user_id = dao.createNewUser(user_email, user_password, user_first_name, user_last_name, role_id)
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name,
                                               role_id)
            return jsonify(result), 201
        else:
            return jsonify("An user with that email address already exists"), 409

    def createUserUnavailableTimeFrame(self, user_id, json):
        unavailable_time_user_start = json['start_date'] + " " + json['start_time']
        unavailable_time_user_finish = json['finish_date'] + " " + json['finish_time']
        dao = UserDAO()
        existing_user = dao.getUserById(user_id)
        if not existing_user:
            return jsonify("User Not Found"), 404
        available_user = self.verifyAvailableUserAtTimeFrame(user_id, unavailable_time_user_start,
                                                             unavailable_time_user_finish)
        if not available_user:
            return jsonify("Time Frame Already Marked as Unavailable"), 409
        else:
            dao.createUnavailableUserTimeFrame(user_id, unavailable_time_user_start,
                                               unavailable_time_user_finish)
            return jsonify('Successfully Marked Time Frame as Unavailable'), 201

    # Read
    def getAllUsers(self):
        dao = UserDAO()
        users_list = dao.getAllUsers()
        if not users_list:  # User List is empty
            return jsonify("No Users Found"), 404
        else:
            result_list = []
            for row in users_list:
                obj = self.build_user_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getUserById(self, user_id):
        dao = UserDAO()
        user_tuple = dao.getUserById(user_id)
        if not user_tuple:  # User Not Found
            return jsonify("User Not Found"), 404
        else:
            result = self.build_user_map_dict(user_tuple)
            return jsonify(result), 200

    # def getUserByEmail(self, user_email):
    #     dao = UserDAO()
    #     user_tuple = dao.getUserByEmail(user_email)
    #     if not user_tuple:  # User Not Found
    #         return jsonify("User Not Found"), 404
    #     else:
    #         result = self.build_user_map_dict(user_tuple)
    #     return jsonify(result), 200

    def getUserRoleById(self, user_id):
        dao = UserDAO()
        user_role = dao.getUserRoleById(user_id)
        if not user_role:  # User Not Found
            return jsonify("User Not Found"), 404
        else:
            result = self.build_role_map_dict(user_role[0])
            return jsonify(result), 200

    def getAllUnavailableTimeOfUsers(self):
        dao = UserDAO()
        unavailable_users_list = dao.getAllUnavailableTimeOfUsers()
        result_list = []
        for row in unavailable_users_list:
            obj = self.build_unavailable_time_user_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getUnavailableTimeOfUserById(self, user_id):
        dao = UserDAO()
        user = dao.getUserById(user_id)
        if not user:  # User Not Found
            return jsonify("User Not Found"), 404

        unavailable_user_tuple = dao.getUnavailableTimeOfUserById(user_id)
        if not unavailable_user_tuple:  # Unavailable Time Slot Not Found
            return jsonify("No Unavailable Time Slots Found for this User"), 404
        else:
            result_list = []
            for row in unavailable_user_tuple:
                obj = self.build_unavailable_time_user_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def verifyAvailableUserAtTimeFrame(self, user_id, start_time_to_verify, finish_time_to_verify):
        dao = UserDAO()

        new_start = dt.datetime.strptime(start_time_to_verify, '%Y-%m-%d %H:%M')
        new_end = dt.datetime.strptime(finish_time_to_verify, '%Y-%m-%d %H:%M')

        user_unavailable_time_slots = dao.getUnavailableTimeOfUserById(user_id)
        if not user_unavailable_time_slots:
            return True
        else:
            for row in user_unavailable_time_slots:
                old_start = row[1]
                old_end = row[2]
                if (old_start < new_start < new_end < old_end) \
                        or (new_start < old_start < old_end < new_end) \
                        or (new_start < old_start < new_end < old_end) \
                        or (old_start < new_start < old_end < new_end) \
                        or (new_start == old_start or new_end == old_end):
                    return False
            return True

    def verifyLogin(self, json):
        user_email = json['user_email']
        user_password = json['user_password']
        user_dao = UserDAO()
        valid_user = user_dao.verifyLogin(user_email, user_password)
        if not valid_user:
            return jsonify("Username or Password entered incorrectly"), 401
        else:
            return jsonify("User logged in successfully", valid_user[0]), 200

    def getUserDaySchedule(self, user_id, json):
        user_dao = UserDAO()
        user = user_dao.getUserById(user_id)
        if not user:  # User Not Found
            return jsonify("User Not Found"), 404

        booking_dao = BookingDAO()
        invitee_dao = BookingInviteeDAO()
        date = json['date']
        start_date = dt.datetime.strptime(date + " 0:00", '%Y-%m-%d %H:%M')
        finish_date = dt.datetime.strptime(date + " 23:59", '%Y-%m-%d %H:%M')

        user_unavailable_time_slots = user_dao.getUnavailableTimeOfUserByIdAndDate(user_id, start_date, finish_date)
        result_list = []
        for row in user_unavailable_time_slots:
            booking_data = booking_dao.getBookingDataAtTimeFrame(row[1], row[2])
            if not booking_data:  # No bookings found at this time frame
                obj = self.build_time_slot_marked_as_busy(row[1], row[2])
                result_list.append(obj)
                continue  # Nothing more to check
            for column in booking_data:
                if row[3] != column[4]:  # User did not create booking
                    invitee_booking_data = invitee_dao.getBookingDataFromInviteeAtTimeFrame(row[3], row[1], row[2])
                    obj = self.build_booking_map_dict_with_room(invitee_booking_data)
                else:
                    obj = self.build_booking_map_dict_with_room(column)
                result_list.append(obj)
        if len(result_list) >= 1:
            return jsonify("User is busy at the following time frames", result_list), 200
        else:
            return jsonify("User is available all day"), 200

    def getMostUsedRoomByUserId(self, user_id):
        dao = UserDAO()
        room_dao = RoomDAO()
        times_used_for_each_room = dao.getUsedRoomsByUserId(user_id)
        if len(times_used_for_each_room) == 0:
            return jsonify("No Used Room available on record"), 404
        else:
            most_used_room = room_dao.getRoomById(times_used_for_each_room[0][0])
            return jsonify(BaseRoom().build_room_map_dict(most_used_room)), 200

    def getInviteUserHasBeenMostBookedWith(self, user_id):
        dao = UserDAO()
        booked_invitees = dao.getInviteeUserHasBeenMostBookedWith(user_id)
        if len(booked_invitees) == 0:
            return jsonify("User has not been booked with any invitee "), 404
        else:
            most_booked_invitee = dao.getUserById(booked_invitees[0][1])
            return jsonify(BaseUser().build_user_map_dict(most_booked_invitee)), 200

    # Update
    def updateUser(self, user_id, json):
        user_email = json['user_email']
        user_password = json['user_password']
        user_first_name = json['user_first_name']
        user_last_name = json['user_last_name']
        role_id = json['role_id']
        dao = UserDAO()
        existing_user = dao.getUserById(user_id)
        existing_email = dao.getUserByEmail(user_email)

        if not existing_user:  # User does not exist
            return jsonify("User Not Found"), 404
        # New email is different from current and new one is used
        elif existing_user[1] != user_email and existing_email:
            return jsonify("An user with that email address already exists"), 409
        else:
            dao.updateUser(user_id, user_email, user_password, user_first_name, user_last_name, role_id, )
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name,
                                               role_id, )
            return jsonify(result), 200

    # Delete
    def deleteUser(self, user_id):
        user_dao = UserDAO()
        booking_dao = BookingDAO()
        invitee_dao = BookingInviteeDAO()
        room_dao = RoomDAO()
        if not user_dao.getUserById(user_id):
            return jsonify("User Not Found"), 404
        unavailable_user_slots = user_dao.getUnavailableTimeOfUserById(user_id)
        for slot in unavailable_user_slots:
            user_dao.deleteUnavailableUserTimeFrame(user_id, slot[1], slot[2])  # Remove Unavailable Time From User
        all_bookings = booking_dao.getAllBookings()
        for booking in all_bookings:
            if booking[0] == user_id:
                booking_dao.deleteBooking(booking[0])  # Booking Without Creator Cannot Exist
                room_dao.deleteUnavailableRoomTime(booking[5], booking[2], booking[3])  # Delete Unavailable Room Time
            invitees = invitee_dao.getInviteeIdListFromBooking(booking[0])
            if user_id in invitees:
                invitee_dao.deleteInvitee(booking[0], user_id)  # Remove Invitee From Booking
        user_dao.deleteUser(user_id)
        return jsonify("User Deleted Successfully"), 200