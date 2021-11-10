import psycopg2

from config.dbconfig import db_root_config


class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Create
    def createNewBooking(self, booking_time_start, booking_time_end):
        cursor = self.conn.cursor()
        query = 'insert into "Booking" (booking_start, booking_finish) values (%s,%s) returning booking_id;'
        cursor.execute(query, (booking_time_start, booking_time_end))
        booking_id = cursor.fetchone()[0]
        self.conn.commit()
        return booking_id

    # Read
    def getAllBookings(self):
        cursor = self.conn.cursor()
        query = 'select booking_id, booking_start, booking_finish from "Booking";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBookingById(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select booking_id, booking_start, booking_finish from "Booking" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result

    # Update
    def updateBooking(self, booking_id, booking_time_start, booking_time_end):
        cursor = self.conn.cursor()
        query = 'update "Booking" ' \
                'set booking_start = %s, booking_finish = %s'
        cursor.execute(query, (booking_time_start, booking_time_end, booking_id))
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
