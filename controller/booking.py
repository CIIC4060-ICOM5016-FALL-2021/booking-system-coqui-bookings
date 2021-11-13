from flask import jsonify

from controller.room import BaseRoom
from controller.user import BaseUser
from model.booking import BookingDAO
from model.booking_invitee import BookingInviteeDAO
from model.room import RoomDAO
from model.user import UserDAO

# CONSTANT VALUES IN DATABASE
PROFESSOR_ROLE = 1
STUDENT_ROLE = 2
STAFF_ROLE = 3

LAB_TYPE = 1
CLASSROOM_TYPE = 2
STUDY_SPACE_TYPE = 3


class BaseBooking:
    def build_booking_map_dict(self, row):
        result = {'booking_id': row[0], 'booking_name': row[1], 'booking_start': row[2], 'booking_finish': row[3],
                  'user_id': row[4], 'room_id': row[5]}
        return result

    def build_booking_attr_dict(self, booking_id, booking_name, booking_start, booking_finish, user_id, room_id,
                                booking_invitees):
        result = {'booking_id': booking_id, 'booking_name': booking_name, 'booking_start': booking_start,
                  'booking_finish': booking_finish, 'user_id': user_id, 'room_id': room_id,
                  'booking_invitees': booking_invitees}
        return result

    # Create
    def createNewBooking(self, user_id, json):
        booking_name = json['booking_name']
        booking_start = json['booking_start_date'] + " " + json['booking_start_time']
        booking_finish = json['booking_finish_date'] + " " + json['booking_finish_time']
        booking_invitees = json['booking_invitee_id']
        room_id = json['room_id']

        booking_dao = BookingDAO()
        user_dao = UserDAO()
        room_dao = RoomDAO()
        invitee_dao = BookingInviteeDAO()

        room_type = room_dao.getRoomTypeById(room_id)
        if not room_dao.getRoomById(room_id):
            return jsonify("Room Not Found"), 404
        room_type = room_type[0]

        role = user_dao.getUserRoleById(user_id)
        if not user_dao.getUserById(user_id):
            return jsonify("User Not Found"), 404
        role = role[0]

        for invitee_id in booking_invitees:
            if not user_dao.getUserById(invitee_id):
                return jsonify("One or More Invitees Not Found"), 404

        if role == STAFF_ROLE or (role == PROFESSOR_ROLE and room_type == CLASSROOM_TYPE) \
                or (role == STUDENT_ROLE and room_type == STUDY_SPACE_TYPE):

            # Verification if room is available during booking time
            available_room = BaseRoom().verifyAvailableRoomAtTimeFrame(room_id, booking_start, booking_finish)
            if not available_room:
                return jsonify("Room is not available during specified time"), 409
            # Verification if user is available during booking time
            available_user = BaseUser().verifyAvailableUserAtTimeFrame(user_id, booking_start, booking_finish)
            if not available_user:
                return jsonify("User is not available during specified time"), 409
            # Verification if invitees are available during booking time
            for invitee_id in booking_invitees:
                if not BaseUser().verifyAvailableUserAtTimeFrame(invitee_id, booking_start, booking_finish):
                    return jsonify("One Or More Invitees is not available during specified time")

            booking_id = booking_dao.createNewBooking(booking_name, booking_start, booking_finish, user_id, room_id)
            user_dao.createUnavailableUserTimeFrame(user_id, booking_start, booking_finish)
            room_dao.createRoomUnavailableTimeSlot(room_id, booking_start, booking_finish)
            for invitee_id in booking_invitees:
                user_dao.createUnavailableUserTimeFrame(invitee_id, booking_start, booking_finish)
                invitee_dao.createNewInvitee(booking_id, invitee_id)

            result = self.build_booking_attr_dict(booking_id, booking_name, booking_start, booking_finish,
                                                  user_id, room_id, booking_invitees)
            return jsonify(result), 201
        else:
            return jsonify(f"User with role {role} does not have permission to book room type {room_type}"), 403

    # TODO LIMIT BY ROLE
    # Read
    def getAllBookings(self):
        dao = BookingDAO()
        bookings_list = dao.getAllBookings()
        if not bookings_list:  # No existing Bookings
            return jsonify("No Bookings Found"), 404
        else:
            result_list = []
            for row in bookings_list:
                obj = self.build_booking_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getBookingById(self, booking_id):
        dao = BookingDAO()
        booking_tuple = dao.getBookingById(booking_id, request.json)
        if not booking_tuple:
            return jsonify("Booking Not Found"), 404
        else:
            result = self.build_booking_map_dict(booking_tuple)
            return jsonify(result), 200

    def getUserBookedRoomAtTimeFrame(self, room_id):
        dao = BookingDAO()
        user_id = dao.getUserBookedRoomAtTimeFrame(room_id)
        if not user_id:
            


    # TODO: GET TOP 5 MOST BOOKED USERS
    # def getMostBookedUsers(self):
    #     dao = BookingDAO()
    #     getMostBookedUsers = dao.getMostBookedUsers
    #     if user_list:
    #         return jsonify("Not enough users found"), 404
    #     else:
    #         result = self.build_booking_map_dict(booking_tuple)
    #         return jsonify(result), 200
    # TODO: GET BUSIEST TIMES
    # def getBusiestTimes(self):
    #     dao = BookingDAO()
    #     all_bookings = dao.getAllBookings()
    #     result_list = []
    #     for row in all_bookings:
    #         start = row[2]
    #         end = row[3]
    #     if len(all_bookings) == 0:
    #         return jsonify("No bookings available"), 404
    #     else:
    #         return jsonify(self.build_room_map_dict(busiest_time[0])), 200

    def getTop10MostBookedRooms(self):
        dao = BookingDAO()
        top_booked_rooms = dao.getTop10MostBookedRooms()
        if len(top_booked_rooms) == 0:
            return jsonify("No Booked Rooms Available"), 404
        else:
            result_list = []
            for row in top_booked_rooms:
                obj = BaseRoom().build_room_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    # Update
    def updateBooking(self, booking_id, user_id, json):
        booking_name = json['booking_name']
        booking_start = json['booking_start_date'] + " " + json['booking_start_time']
        booking_finish = json['booking_finish_date'] + " " + json['booking_finish_time']
        new_invitees = json['booking_invitee_id']
        new_room_id = json['room_id']

        booking_dao = BookingDAO()
        user_dao = UserDAO()
        room_dao = RoomDAO()
        invitee_dao = BookingInviteeDAO()
        role = user_dao.getUserRoleById(user_id)[0]
        current_room_id = booking_dao.getBookingRoomFromId(booking_id)[0]

        if not room_dao.getRoomById(new_room_id):
            return jsonify("Room Not Found"), 404

        room_type = room_dao.getRoomTypeById(new_room_id)[0]

        for invitee_id in new_invitees:
            if not user_dao.getUserById(invitee_id):
                return jsonify("One or More Invitees Not Found"), 404

        current_invitees = invitee_dao.getInviteesByBookingId(booking_id)
        old_times = booking_dao.getBookingStartFinishTime(booking_id)  # Get old times to compare changes

        if role == STAFF_ROLE or (role == PROFESSOR_ROLE and room_type == CLASSROOM_TYPE) \
                or (role == STUDENT_ROLE and room_type == STUDY_SPACE_TYPE):  # User has permission to book

            user_dao.deleteUnavailableUserTimeFrame(user_id, old_times[0], old_times[1])  # User is free at old time
            # Verification if user is available during new booking time
            if not BaseUser().verifyAvailableUserAtTimeFrame(user_id, booking_start, booking_finish):
                # Re-insert old time frame
                user_dao.createUnavailableUserTimeFrame(user_id, old_times[0], old_times[1])
                return jsonify("User is not available during specified time"), 409

            # Room is free at old time
            room_dao.deleteUnavailableRoomTime(current_room_id, old_times[0], old_times[1])
            # Verification if room is available during new booking time
            if not BaseRoom().verifyAvailableRoomAtTimeFrame(new_room_id, booking_start, booking_finish):
                # Re-insert old time
                room_dao.createRoomUnavailableTimeSlot(new_room_id, old_times[0], old_times[1])
                return jsonify("Room is not available during specified time"), 409

            valid_update = self.updateBookingInvitees(booking_id, current_invitees, new_invitees, old_times[0],
                                                      old_times[1], booking_start, booking_finish)
            if not valid_update:
                return jsonify("One Or More Invitees is not available during specified time"), 409

            user_dao.createUnavailableUserTimeFrame(user_id, booking_start, booking_finish)
            room_dao.createRoomUnavailableTimeSlot(new_room_id, booking_start, booking_finish)
            booking_dao.updateBooking(booking_id, booking_name, booking_start, booking_finish, user_id, new_room_id)
            result = self.build_booking_attr_dict(booking_id, booking_name, booking_start, booking_finish,
                                                  user_id, new_room_id, new_invitees)
            return jsonify(result), 200  # Successfully Updated Booking

        else:
            return jsonify(f"User with role {role} does not have permission to book room type {room_type}"), 403

    # AUXILIARY METHOD FOR UPDATE BOOKING
    def updateBookingInvitees(self, booking_id, old_invitees, new_invitees, old_time_start, old_time_finish,
                              new_time_start, new_time_finish):
        user_dao = UserDAO()
        invitee_dao = BookingInviteeDAO()
        for current_invitee_id in old_invitees:  # Remove the current invitees of the old time
            invitee_dao.deleteInvitee(booking_id, current_invitee_id)
            user_dao.deleteUnavailableUserTimeFrame(current_invitee_id, old_time_start, old_time_finish)

        for new_invitee_id in new_invitees:  # Verify all New Invitees
            if not BaseUser().verifyAvailableUserAtTimeFrame(new_invitee_id, new_time_start, new_time_finish):
                for removed_id in old_invitees:  # Rollback the removed users
                    invitee_dao.createNewInvitee(booking_id, removed_id)
                    user_dao.createUnavailableUserTimeFrame(removed_id, old_time_start, old_time_finish)
                return False

        # Add new invitees
        for invitee_id in new_invitees:
            invitee_dao.createNewInvitee(booking_id, invitee_id)
            user_dao.createUnavailableUserTimeFrame(invitee_id, new_time_start, new_time_finish)
        return True

    # Delete
    def deleteBooking(self, booking_id):
        dao = BookingDAO()
        result = dao.deleteBooking(booking_id)
        if result:
            return jsonify("Booking Deleted Successfully"), 200
        else:
            return jsonify("Booking Not Found"), 404
