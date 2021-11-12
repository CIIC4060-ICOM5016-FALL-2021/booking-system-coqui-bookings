import psycopg2

from config.dbconfig import db_root_config


class RoomDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Create
    def createNewRoom(self, room_name, room_type_id):
        cursor = self.conn.cursor()
        query = 'insert into "Room" (room_name, room_type_id) values (%s, %s) returning room_id;'
        cursor.execute(query, (room_name, room_type_id,))
        room_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_id

    def createRoomUnavailableTimeSlot(self, room_id, unavailable_time_room_start, unavailable_time_room_finish):
        cursor = self.conn.cursor()
        query = 'insert into "UnavailableTimeRoom" (unavailable_time_room_start, unavailable_time_room_finish, room_id) values (%s, %s, %s); '
        cursor.execute(query, (unavailable_time_room_start, unavailable_time_room_finish, room_id,))
        #user_id = cursor.fetchone()[0]
        self.conn.commit()
        return True

    # Read
    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name, room_type_id from "Room";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name, room_type_id from "Room" where room_id = %s;'
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        return result

    def getRoomTypeById(self, room_id):
        cursor = self.conn.cursor()
        query = 'select room_type_id ' \
                'from "Room" where room_id = %s;'
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        return result

    def getAllUnavailableTimeOfRooms(self):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_room_id, unavailable_time_room_start, unavailable_time_room_finish, room_id ' \
                'from "UnavailableTimeRoom";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUnavailableTimeOfRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_room_id, unavailable_time_room_start, unavailable_time_room_finish, room_id ' \
                'from "UnavailableTimeRoom" where room_id = %s;'
        cursor.execute(query, (room_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
        
    def getRoomByName(self, room_name):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name, room_type_id from "Room" where room_name = %s;'
        cursor.execute(query, (room_name,))
        result = cursor.fetchone()
        return result

    # Update
    def updateRoom(self, current_room_id, room_name, room_type_id):
        cursor = self.conn.cursor()
        query = 'update "Room" set room_name = %s, room_type_id = %s where room_id = %s;'
        cursor.execute(query, (room_name, room_type_id, current_room_id,))
        self.conn.commit()
        return True

    # Delete
    def deleteRoom(self, room_id):
        cursor = self.conn.cursor()
        query = 'delete from "Room" where room_id = %s;'
        cursor.execute(query, (room_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    # TODO: deleteRoomFromBooking (Unavailable Room)
