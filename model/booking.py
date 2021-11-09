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

    # Read
    def getAllBookings(self):
        cursor = self.conn.cursor()
        query = 'select booking_id, booking_time_start, booking_time_end from "Booking";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBookingById(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select booking_id, booking_time_start, booking_time_end from "Booking" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result
    # Update

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
