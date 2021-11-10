from flask import jsonify
from model.booking import UserDAO


class BaseBooking:
    def build_booking_dict(self, row):
        result = {'booking_id': row[0], 'booking_start': row[1], 'booking_finish': row[2]}
        return result

    def build_booking_attr_dict(self, booking_id, booking_start, booking_finish):
        result = {'booking_id': booking_id, 'booking_start': booking_start,
                  'booking_finish': booking_finish}
        return result

    # Create
    def createNewBooking(self, json):
        booking_start = json['booking_start']
        booking_finish = json['booking_finish']
        dao = UserDAO()
        booking_id = dao.createNewBooking(booking_start, booking_finish)
        result = self.build_booking_attr_dict(booking_id, booking_start, booking_finish)
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
        booking_start = json['booking_start']
        booking_finish = json['booking_finish']
        booking_id = json['booking_id']
        dao = UserDAO()
        updated_code = dao.updateBooking(booking_id, booking_start, booking_finish)  # TODO FIX
        result = self.build_booking_attr_dict(booking_id, booking_start, booking_finish)
        return jsonify(result), 200

    # Delete
    def deleteBooking(self, booking_id):
        dao = UserDAO()
        result = dao.deleteBooking(booking_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
