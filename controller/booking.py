from flask import jsonify
from model.booking import UserDAO


class BaseBooking:
    def build_booking_dict(self, row):
        result = {'booking_id': row[0], 'booking_time_start': row[1], 'booking_time_end': row[2]}
        return result

    def build_booking_attr_dict(self, booking_id, booking_time_start, booking_time_end):
        result = {}
        result['booking_id'] = booking_id
        result['booking_time_start'] = booking_time_start
        result['booking_time_end'] = booking_time_end
        return result

    # Create
    def createNewBooking(self, json):
        booking_time_start = json['booking_time_start']
        booking_time_end = json['booking_time_end']
        dao = UserDAO()
        booking_id = dao.createNewBooking(booking_time_start, booking_time_end)
        result = self.build_booking_attr_attr_dict(booking_id, booking_time_start, booking_time_end)
        return jsonify(result), 201

    # Read
    def getAllBookings(self):
        dao = UserDAO()
        bookings_list = dao.getAllBookings()
        result_list = []
        for row in bookings_list:
            obj = self.build_booking_dict(row)
            result_list.append(obj)
            return jsonify(result_list)

    def getBookingById(self, booking_id):
        dao = UserDAO()
        booking_tuple = dao.getBookingById(booking_id)
        if not booking_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_booking_dict(booking_tuple)
            return jsonify(result), 200

    # Update
    def updateBooking(self, json):
        booking_time_start = json['booking_time_start']
        booking_time_end = json['booking_time_end']
        user_id = json['user_id']
        dao = UserDAO()
        updated_code = dao.updateUser(user_id, user_email, user_password, user_first_name, user_last_name,)
        result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name,)
        return jsonify(result), 200

    # Delete