from flask import jsonify

from backend.model.booking import BookingDAO
from backend.model.room import RoomDAO
import datetime as dt

from backend.model.user import UserDAO


class BaseRoom:

    def build_room_map_dict(self, row):
        result = {'room_id': row[0], 'room_name': row[1], 'room_type_id': row[2]}
        return result

    def build_most_booked_map_dict(self, row):
        result = {'room_id': row[0], 'room_name': row[1], 'times_booked': row[2]}
        return result

    def build_room_attr_dict(self, room_id, room_name, room_type_id):
        result = {'room_id': room_id, 'room_name': room_name, 'room_type_id': room_type_id}
        return result

    def build_unavailable_time_room_map_dict(self, row):
        result = {'unavailable_time_room_id': row[0],
                  'unavailable_time_room_start': row[1],
                  'unavailable_time_room_finish': row[2],
                  'room_id': row[3]}
        return result

    def build_type_map_dict(self, row):
        result = {'room_type_id': row}
        return result

    def build_time_slot_attr_dict(self, start_time, finish_time):
        result = {'start_time': dt.datetime.strftime(start_time, '%Y-%m-%d %H:%M') + " AST",
                  'finish_time': dt.datetime.strftime(finish_time, '%Y-%m-%d %H:%M') + " AST"}
        return result

    def build_time_slot_marked_as_busy(self, start_time, finish_time):
        result = {'start_time': start_time,
                  'finish_time': finish_time,
                  'booking_name': "Room marked as busy by Admin"}
        return result

    def build_booking_map_dict_with_room(self, row):
        result = {'booking_id': row[0], 'booking_name': row[1],
                  'start_time': row[2],
                  'finish_time': row[3],
                  'organizer_id': row[4], 'room_id': row[5], 'room_name': row[6]}
        return result

    # Create
    def createNewRoom(self, json):
        room_name = json['room_name']
        room_type_id = json['room_type_id']
        dao = RoomDAO()
        existing_room = dao.getRoomByName(room_name)
        if not existing_room:  # Room with such name dos not exist
            room_id = dao.createNewRoom(room_name, room_type_id)
            result = self.build_room_attr_dict(room_id, room_name, room_type_id)
            return jsonify(result), 201
        else:
            return jsonify("A room with that name already exists"), 409

    def createRoomUnavailableTimeFrame(self, user_id, room_id, json):
        unavailable_time_room_start = json['start_date'] + " " + json['start_time']
        unavailable_time_room_finish = json['finish_date'] + " " + json['finish_time']
        dao_room = RoomDAO()
        dao_user = UserDAO()

        existing_user = dao_user.getUserById(user_id)
        if not existing_user:
            return jsonify("User Not Found"), 404

        existing_room = dao_room.getRoomById(room_id)
        if not existing_room:
            return jsonify("Room Not Found"), 404

        existing_user_role = dao_user.getUserRoleById(user_id)[0]
        if existing_user_role == 3:

            verify_slot = self.verifyAvailableRoomAtTimeFrame(room_id, unavailable_time_room_start,
                                                              unavailable_time_room_finish)
            if not verify_slot:
                return jsonify("Time Frame Already Marked as Unavailable"), 409
            else:
                dao_room.createRoomUnavailableTimeSlot(room_id, unavailable_time_room_start,
                                                       unavailable_time_room_finish)
                return jsonify("Successfully Marked Time as Unavailable"), 201
        else:
            return jsonify(f"User with role {existing_user_role} does not have permission to create"), 403

    # Read
    def getAllRooms(self):
        dao = RoomDAO()
        rooms_list = dao.getAllRooms()
        if not rooms_list:  # There are no rooms
            return jsonify("No Rooms Found"), 404
        else:
            result_list = []
            for row in rooms_list:
                obj = self.build_room_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list)

    def getMostUsedRoom(self):
        dao = RoomDAO()
        times_used_for_each_room = dao.getTimesUsedForEachRoom()
        if len(times_used_for_each_room) == 0:
            return jsonify("No Used Room available on record"), 404
        else:
            return jsonify(self.build_room_map_dict(times_used_for_each_room[0])), 200

    def getRoomById(self, room_id):
        dao = RoomDAO()
        room_tuple = dao.getRoomById(room_id, )
        if not room_tuple:
            return jsonify("Room Not Found"), 404
        else:
            result = self.build_room_map_dict(room_tuple)
            return jsonify(result), 200

    def getRoomTypeById(self, room_id):
        dao = RoomDAO()
        room_type = dao.getRoomTypeById(room_id)

        if not room_type:  # Room Not Found
            return jsonify("Room Not Found"), 404
        else:
            result = self.build_type_map_dict(room_type[0])
            return jsonify(result), 200

    def getAllAvailableRoomsAtTimeFrame(self, json):
        search_start = json['start_date'] + " " + json['start_time']
        search_finish = json['finish_date'] + " " + json['finish_time']

        dao = RoomDAO()
        rooms_list = dao.getAllRooms()
        if not rooms_list:  # There are no rooms
            return jsonify("No Rooms Found"), 404
        else:
            result_list = []
            for room in rooms_list:
                if self.verifyAvailableRoomAtTimeFrame(room[0], search_start, search_finish):
                    obj = self.build_room_map_dict(room)
                    result_list.append(obj)

            if len(result_list) == 0:
                return jsonify("No Rooms Available at Specified Time Frame"), 200
            else:
                return jsonify(result_list), 200

    def getAllUnavailableTimeOfRooms(self):  # MIGHT NOT BE NEEDED
        room_dao = RoomDAO()
        unavailable_rooms_list = room_dao.getAllUnavailableTimeOfRooms()
        result_list = []
        for row in unavailable_rooms_list:
            obj = self.build_unavailable_time_room_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getUnavailableTimeOfRoomById(self, room_id):
        room_dao = RoomDAO()
        booking_dao = BookingDAO()
        room = room_dao.getRoomById(room_id)
        if not room:
            return jsonify("Room Not Found"), 404
        unavailable_room_tuple = room_dao.getUnavailableTimeOfRoomById(room_id)
        if not unavailable_room_tuple:  # Unavailable Room Not Found
            return jsonify("No Unavailable Time Slots Found for this Room"), 404
        else:
            result_list = []
            for row in unavailable_room_tuple:
                booking_data = booking_dao.getBookingDataAtTimeFrame(row[1], row[2])
                if not booking_data:  # No bookings found at this time frame
                    obj = self.build_time_slot_marked_as_busy(row[1], row[2])
                    result_list.append(obj)
                    continue  # Nothing more to check
                for column in booking_data:
                    if column[5] == row[3]:
                        obj = self.build_booking_map_dict_with_room(column)
                        result_list.append(obj)
            return jsonify(result_list), 200

    def verifyAvailableRoomAtTimeFrame(self, room_id, start_time_to_verify, finish_time_to_verify):
        dao = RoomDAO()
        new_start = dt.datetime.strptime(start_time_to_verify, '%Y-%m-%d %H:%M')
        new_end = dt.datetime.strptime(finish_time_to_verify, '%Y-%m-%d %H:%M')

        room_unavailable_time_slots = dao.getUnavailableTimeOfRoomById(room_id)
        if not room_unavailable_time_slots:
            return True
        else:
            for row in room_unavailable_time_slots:
                old_start = row[1]
                old_end = row[2]
                if (old_start < new_start < new_end < old_end) \
                        or (new_start < old_start < old_end < new_end) \
                        or (new_start < old_start < new_end < old_end) \
                        or (old_start < new_start < old_end < new_end) \
                        or (new_start == old_start or new_end == old_end):
                    return False
            return True

    def getRoomDaySchedule(self, room_id, json):
        room_dao = RoomDAO()
        room = room_dao.getRoomById(room_id)
        if not room:
            return jsonify("Room Not Found"), 404

        booking_dao = BookingDAO()
        date = json['date']
        start_date = dt.datetime.strptime(date + " 0:00", '%Y-%m-%d %H:%M')
        finish_date = dt.datetime.strptime(date + " 23:59", '%Y-%m-%d %H:%M')

        room_unavailable_time_slots = room_dao.getUnavailableTimeOfRoomByIdAndDate(room_id, start_date, finish_date)
        result_list = []
        for row in room_unavailable_time_slots:
            booking_data = booking_dao.getBookingDataAtTimeFrame(row[1], row[2])
            if not booking_data:  # No bookings found at this time frame
                obj = self.build_time_slot_marked_as_busy(row[1], row[2])
                result_list.append(obj)
                continue  # Nothing more to check
            for column in booking_data:
                if column[5] == row[3]:
                    obj = self.build_booking_map_dict_with_room(column)
                    result_list.append(obj)
        if len(result_list) >= 1:
            return jsonify("Room is busy at the following time frames", result_list), 200
        else:
            return jsonify("Room is available all day"), 200

    # Update
    def updateRoom(self, room_id, json):
        room_name = json['room_name']
        room_type_id = json['room_type_id']
        dao = RoomDAO()
        existing_room = dao.getRoomById(room_id)
        existing_name = dao.getRoomByName(room_name)
        if not existing_room:
            return jsonify("Room Not Found"), 404
        elif existing_room[1] != room_name and existing_name:
            return jsonify("A room with that name already exists"), 409
        else:
            dao.updateRoom(room_id, room_name, room_type_id)
            result = self.build_room_attr_dict(room_id, room_name, room_type_id)
            return jsonify(result), 200

    # Delete
    def deleteRoom(self, room_id):
        room_dao = RoomDAO()
        booking_dao = BookingDAO()
        if not room_dao.getRoomById(room_id):
            return jsonify("Room Not Found"), 404
        all_bookings = booking_dao.getAllBookings()
        for booking in all_bookings:
            if booking[5] == room_id:
                booking_dao.deleteBooking(booking[0])
        unavailable_room_slots = room_dao.getUnavailableTimeOfRoomById(room_id)  # Search any remaining slots
        for slot in unavailable_room_slots:
            room_dao.deleteUnavailableRoomTime(room_id, slot[1], slot[2])
        room_dao.deleteRoom(room_id)
        return jsonify("Room Deleted Successfully"), 200

    def deleteUnavailableRoomTime(self, room_id, start_time, finish_time):
        dao = RoomDAO()
        result = dao.deleteUnavailableRoomTime(room_id, start_time, finish_time)
        if result:
            return jsonify("Room Time Freed Successfully"), 200
        else:
            return jsonify("Room Is Already Free at Specified Time"), 200
