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
    def createNewRoom(self, room_name):
        cursor = self.conn.cursor()
        query = 'insert into "Room" (room_name) values (%s) returning room_id;'
        cursor.execute(query, (room_name,))
        room_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_id

    # Read
    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name from "Room";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name from "Room" where room_id = %s;'
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        return result

    def getAllUnavailableRooms(self):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_room_id, unavailable_time_room_start, unavailable_time_room_finish, room_id ' \
                'from "UnavailableTimeRoom";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Update
    def updateRoom(self, room_id, room_name):
        cursor = self.conn.cursor()
        query = 'update "Room" set room_name = %s where room_id = %s;'
        cursor.execute(query, (room_name, room_id))
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
