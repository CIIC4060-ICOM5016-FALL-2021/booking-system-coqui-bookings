import psycopg2

from config.dbconfig import db_root_config


class BookingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Create
    def createNewBooking(self, booking_name, booking_time_start, booking_time_end, user_id, room_id):
        cursor = self.conn.cursor()
        query = 'insert into "Booking" (booking_name, booking_start, booking_finish, user_id, room_id)' \
                'values (%s,%s,%s,%s,%s) returning booking_id;'
        cursor.execute(query, (booking_name, booking_time_start, booking_time_end, user_id, room_id))
        booking_id = cursor.fetchone()[0]
        self.conn.commit()
        return booking_id

    # Read
    def getAllBookings(self):
        cursor = self.conn.cursor()
        query = 'select booking_id, booking_name, booking_start, booking_finish, user_id, room_id from "Booking";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBookingById(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select booking_id, booking_name, booking_start, booking_finish , user_id, room_id from "Booking"' \
                'where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result

    def getUserBookedRoomAtTimeFrame(self, room_id, booking_start, booking_finish):
        cursor = self.conn.cursor()
        query = 'select user_id from "Booking"' \
                'where room_id = %s and booking_start = %s and booking_finish = %s'
        cursor.execute(query, (room_id,booking_start,booking_finish))
        result = cursor.fetchone()
        return result
        
    def getAllTimes(self):
        cursor = self.conn.cursor()
        query = 'select booking_start, booking_finish from "Booking"' 
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # def getMostBookedUsers(self):
    #     cursor = self.conn.cursor()
    #     query = 'select user_id, "BookingInvitee".user_id from "Booking" inner join "BookingInvitee" on "Booking".booking_id = "BookingInvitee".booking_id;'
    #     cursor.execute(query)
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     return result

    def getTop10MostBookedRooms(self):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name, count(room_id) as times_used from "Booking" natural inner join "Room" group by room_id, room_name order by times_used desc limit 10;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Used in Booking Update Only
    def getBookingStartFinishTime(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select booking_start, booking_finish from "Booking" where booking_id = %s'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result

    # Used in Booking Update Only
    def getBookingRoomFromId(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select room_id from "Booking" where booking_id = %s'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result

    # Used in Getting Booking Invitees Only
    def getBookingRoomTypeFromId(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select room_type_id from "Booking" natural inner join "Room" where booking_id = %s'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result

    # Update
    def updateBooking(self, booking_id, booking_name, booking_time_start, booking_time_end, user_id, room_id):
        cursor = self.conn.cursor()
        query = 'update "Booking" set booking_name = %s, booking_start = %s, booking_finish = %s, user_id = %s,' \
                'room_id = %s where booking_id = %s'
        cursor.execute(query, (booking_name, booking_time_start, booking_time_end, user_id, room_id, booking_id))
        self.conn.commit()
        return True

    # Delete
    def deleteBooking(self, booking_id):
        cursor = self.conn.cursor()
        query = 'delete from "Booking" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0
