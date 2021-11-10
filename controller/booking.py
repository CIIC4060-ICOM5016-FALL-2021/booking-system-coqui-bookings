from flask import jsonify
from model.booking import BookingDAO


class BaseBooking:
    def build_booking_dict(self, row):
        result = {'booking_id': row[0], 'booking_name': row[1], 'booking_start': row[2], 'booking_finish': row[3],
                  'user_id': row[4], 'room_id': row[5]}
        return result

    def build_booking_attr_dict(self, booking_id, booking_name, booking_start, booking_finish, user_id, room_id):
        result = {'booking_id': booking_id, 'booking_name': booking_name, 'booking_start': booking_start,
                  'booking_finish': booking_finish, 'user_id': user_id, 'room_id': room_id}
        return result

    # Create
    def createNewBooking(self, json):
        booking_name = json['booking_name']
        booking_start = json['booking_start_date'] + " " + json['booking_start_time']
        booking_finish = json['booking_finish_date'] + " " + json['booking_finish_time']
        user_id = json['creator_user_id']
        room_id = json['room_id']
        dao = BookingDAO()
        booking_id = dao.createNewBooking(booking_name, booking_start, booking_finish, user_id, room_id)
        result = self.build_booking_attr_dict(booking_id, booking_name, booking_start, booking_finish, user_id, room_id)
        return jsonify(result), 201

    # Read
    def getAllBookings(self):
        dao = BookingDAO()
        bookings_list = dao.getAllBookings()
        result_list = []
        for row in bookings_list:
            obj = self.build_booking_dict(row)
            result_list.append(obj)
            return jsonify(result_list)

    def getBookingById(self, booking_id):
        dao = BookingDAO()
        booking_tuple = dao.getBookingById(booking_id)
        if not booking_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_booking_dict(booking_tuple)
            return jsonify(result), 200

    # Update
    def updateBooking(self, booking_id, json):
        booking_name = json['booking_name']
        booking_start = json['booking_start_date'] + " " + json['booking_start_time']
        booking_finish = json['booking_finish_date'] + " " + json['booking_finish_time']
        user_id = json['creator_user_id']
        room_id = json['room_id']
        dao = BookingDAO()
        existentBooking = dao.getBookingById(booking_id)
        if not existentBooking:
            return jsonify("Not Found"), 404
        else:
            dao.updateBooking(booking_id, booking_name, booking_start, booking_finish, user_id, room_id)
            result = self.build_booking_attr_dict(booking_id, booking_name, booking_start, booking_finish, user_id,
                                                  room_id)
            return jsonify(result), 200

    # Delete
    def deleteBooking(self, booking_id):
        dao = BookingDAO()
        result = dao.deleteBooking(booking_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
