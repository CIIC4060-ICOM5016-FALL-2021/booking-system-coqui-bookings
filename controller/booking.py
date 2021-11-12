from flask import jsonify

from controller.room import BaseRoom
from controller.user import BaseUser
from model.booking import BookingDAO
from model.room import RoomDAO
from model.user import UserDAO


class BaseBooking:
    def build_booking_map_dict(self, row):
        result = {'booking_id': row[0], 'booking_name': row[1], 'booking_start': row[2], 'booking_finish': row[3],
                  'user_id': row[4], 'room_id': row[5]}
        return result

    def build_booking_attr_dict(self, booking_id, booking_name, booking_start, booking_finish, user_id, room_id):
        result = {'booking_id': booking_id, 'booking_name': booking_name, 'booking_start': booking_start,
                  'booking_finish': booking_finish, 'user_id': user_id, 'room_id': room_id}
        return result

    # Create
    def createNewBooking(self, user_id, json):  
        booking_name = json['booking_name']
        booking_start = json['booking_start_date'] + " " + json['booking_start_time']
        booking_finish = json['booking_finish_date'] + " " + json['booking_finish_time']
        #user_id = json['creator_user_id']
        room_id = json['room_id']

        booking_dao = BookingDAO()
        user_dao = UserDAO()
        room_dao = RoomDAO()

        role = user_dao.getUserRoleById(user_id)
        room_type = room_dao.getRoomTypeById(room_id)

        if (role == 3 and (room_type==1 or room_type==2)) or (role==2 and room_type==2) or (role==1 and room_type==3): 
            # Verification if another room is available during booking time
            available_room = BaseRoom().verifyAvailableRoomAtTimeFrame(room_id, booking_start, booking_finish)
            # Verification if user is available during
            available_user = BaseUser().verifyAvailableUserAtTimeFrame(user_id, booking_start, booking_finish)

            if not available_room:
                return jsonify("Room is not available during specified time"), 409
            elif not available_user:
                return jsonify("User is not available during specified time"), 409
            else:
                booking_id = booking_dao.createNewBooking(booking_name, booking_start, booking_finish, user_id, room_id)
                result = self.build_booking_attr_dict(booking_id, booking_name, booking_start, booking_finish, user_id,
                                                    room_id)
                return jsonify(result), 201
        else:
            return jsonify(f"User with role {role} does not have permission to book room type {room_type[0]}"),403

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
                return jsonify(result_list)

    def getBookingById(self, booking_id):
        dao = BookingDAO()
        booking_tuple = dao.getBookingById(booking_id)
        if not booking_tuple:
            return jsonify("Booking Not Found"), 404
        else:
            result = self.build_booking_map_dict(booking_tuple)
            return jsonify(result), 200

    # Update
    def updateBooking(self, booking_id, json): # TODO Limit By ID
        booking_name = json['booking_name']
        booking_start = json['booking_start_date'] + " " + json['booking_start_time']
        booking_finish = json['booking_finish_date'] + " " + json['booking_finish_time']
        user_id = json['creator_user_id']
        room_id = json['room_id']
        booking_dao = BookingDAO()

        # Verification if another room is available during booking time
        available_room = BaseRoom().verifyAvailableRoomAtTimeFrame(room_id, booking_start, booking_finish)
        # Verification if user is available during
        available_user = BaseUser().verifyAvailableUserAtTimeFrame(user_id, booking_start, booking_finish)

        if not available_room:
            return jsonify("Room is not available during specified time"), 409
        elif not available_user:
            return jsonify("User is not available during specified time"), 409
        else:
            booking_dao.updateBooking(booking_id, booking_name, booking_start, booking_finish, user_id, room_id)
            result = self.build_booking_attr_dict(booking_id, booking_name, booking_start, booking_finish, user_id,
                                                  room_id)
            return jsonify(result), 200

    # Delete
    def deleteBooking(self, booking_id):
        dao = BookingDAO()
        result = dao.deleteBooking(booking_id)
        if result:
            return jsonify("Booking Deleted Successfully"), 200
        else:
            return jsonify("Booking Not Found"), 404
