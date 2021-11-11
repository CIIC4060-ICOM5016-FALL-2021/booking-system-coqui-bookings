from flask import jsonify
from model.room import RoomDAO
import datetime

from model.user import UserDAO

class BaseRoom:

    def build_room_map_dict(self, row):
        result = {'room_id': row[0], 'room_name': row[1], 'room_type_id': row[2]}
        return result

    def build_room_attr_dict(self, room_id, room_name, room_type_id):
        result = {'room_id': room_id, 'room_name': room_name, 'room_type_id': room_type_id}
        return result

    def build_unavailable_time_room_dict(self, row):
        result = {'unavailable_time_room_id': row[0], 'unavailable_time_room_start': row[1], 'unavailable_time_room_finish': row[2],
                  'room_id': row[3]}
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

    def createRoomUnavailableTimeSlot(self, user_id, room_id, json):
        unavailable_time_room_start = json['unavailable_time_room_start']
        unavailable_time_room_finish = json['unavailable_time_room_finish']
        dao_room = RoomDAO()
        dao_user = UserDAO()
        existing_room = dao_room.getRoomById(room_id)
        existing_user = dao_user.getUserById(user_id)
        existing_user_role = dao_user.getUserRoleById(user_id)

        if not existing_user:
            return jsonify("User Not Found"), 404

        elif existing_user_role[0]==3:
            if not existing_room:
                return jsonify("Room Not Found"), 404

            verify_slot = self.verifyAvailabilityOfRoomAtTimeSlot(room_id, unavailable_time_room_start, unavailable_time_room_finish)
            if verify_slot:
                result = dao_room.createRoomUnavailableTimeSlot(room_id, unavailable_time_room_start, unavailable_time_room_finish)
                return jsonify("Successfully inserted unavailable slot"), 200
            else:
                return jsonify("Time slot overlaps"), 409

        else:
            return jsonify("User does not have permissison to create"), 403

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

    def getRoomById(self, room_id):
        dao = RoomDAO()
        room_tuple = dao.getRoomById(room_id,)
        if not room_tuple:
            return jsonify("Room Not Found"), 404
        else:
            result = self.build_room_map_dict(room_tuple)
            return jsonify(result), 200

    def getAllUnavailableRooms(self):
        dao = RoomDAO()
        unavailable_rooms_list = dao.getAllUnavailableRooms()
        result_list = []
        for row in unavailable_rooms_list:
            obj = self.build_unavailable_time_room_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getUnavailableRoomById(self, room_id):
        dao = RoomDAO()
        unavailable_room_tuple = dao.getUnavailableRoomById(room_id)
        if not unavailable_room_tuple:  # Unavailable Room Not Found
            return jsonify("Unavailable Room Not Found"), 404
        else:
            result = self.build_unavailable_time_room_dict(unavailable_room_tuple)
            return jsonify(result), 200


    def verifyAvailabilityOfRoomAtTimeSlot(self, room_id, unavailable_time_room_start, unavailable_time_room_finish):
        dao = RoomDAO()
        start_format = datetime.datetime.strptime(unavailable_time_room_start, '%Y-%m-%d %H:%M')
        finish_format = datetime.datetime.strptime(unavailable_time_room_finish, '%Y-%m-%d %H:%M')

        room_unavailable_time_slots = dao.getUnavailableRoomById(room_id)
        if not room_unavailable_time_slots:
            return True

        for row in room_unavailable_time_slots:
            existing_start = row[2]
            existing_end = row[3]
            if (existing_start<start_format<finish_format<existing_end) \
                or (start_format<existing_start<existing_end<finish_format)\
                    or (start_format<existing_start<finish_format<existing_end)\
                        or (existing_start<finish_format<existing_end<finish_format):

                return False

        return True

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
        dao = RoomDAO()
        result = dao.deleteRoom(room_id)
        if result:
            return jsonify("Room Deleted Successfully"), 200
        else:
            return jsonify("Room Not Found"), 404
