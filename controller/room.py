from flask import jsonify
from model.room import RoomDAO


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
