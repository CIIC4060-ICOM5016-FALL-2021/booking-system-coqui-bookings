from flask import jsonify
from model.room import UserDAO


class BaseRoom:

    def build_room_dict(self, row):
        result = {'room_id': row[0], 'room_name': row[1]}
        return result

    def build_room_attr_dict(self, room_id, room_name):
        result = {}
        result['room_id'] = room_id
        result['room_name'] = room_name
        return result

    def build_unavailable_room_dict(self, row):
        result = {'unavailable_id': row[0], 'unavailable_time_start': row[1], 'unavailable_time_end': row[2],
                  'room_id': row[3]}
        return result
# Create
    def createNewRoom(self, json):
        room_name = json['room_name']
        dao = UserDAO()
        room_id = dao.createNewRoom(room_name)
        result = self.build_room_attr_dict(room_id, room_name)
        return jsonify(result), 201

# Read
    def getAllRooms(self):
        dao = UserDAO()
        rooms_list = dao.getAllRooms()
        result_list = []
        for row in rooms_list:
            obj = self.build_room_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getRoomById(self, room_id):
        dao = UserDAO()
        room_tuple = dao.getRoomById(room_id)
        if not room_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_room_dict(room_tuple)
            return jsonify(result), 200

    def getAllUnavailableRooms(self):
        dao = UserDAO()
        unavailable_rooms_list = dao.getAllUnavailableRooms()
        result_list = []
        for row in unavailable_rooms_list:
            obj = self.build_unavailable_room_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    # Update
    def updateRoom(self, json):
        room_name = json['room_name']
        room_id = json['room_id']
        dao = UserDAO()
        updated_code = dao.updateRoom(room_id, room_name)
        result = self.build_room_attr_dict(room_id, room_name)
        return jsonify(result), 200

    # Delete
    def deleteRoom(self, room_id):
        dao = UserDAO()
        result = dao.deleteRoom(room_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404




