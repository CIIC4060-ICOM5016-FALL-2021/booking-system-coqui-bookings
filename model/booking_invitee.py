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
    def createNewInvitee(self, user_id, booking_id):
        cursor = self.conn.cursor()
        query = 'insert into "BookingInvitee" (user_id, booking_id) values (%s,' \
                '%s,%s,%s,%s)  '
        cursor.execute(query, (user_id, booking_id,))
        self.conn.commit()
        return True

    # Read
    def getAllInvitees(self):
        cursor = self.conn.cursor()
        query = 'select user_id, booking_id from "User" natural inner join "Booking" natural inner join "BookingInvitee";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteeById(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select user_id, booking_id ' \
                'from "User" natural inner join "Booking" natural inner join "BookingInvitee" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        return result

    # Update
    def updateInvitee(self, booking_id, user_id):
        cursor = self.conn.cursor()
        query = 'update "BookingInvitee" ' \
                'set user_id = %s ' \
                'where booking_id = %s '
        cursor.execute(query, (user_id, booking_id,))
        self.conn.commit()
        return True

    # Delete
    def deleteInvitee(self, booking_id):
        cursor = self.conn.cursor()
        query = 'delete from "BookingInvitee" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    # TODO: deleteUserFromBooking (Unavailable User)
