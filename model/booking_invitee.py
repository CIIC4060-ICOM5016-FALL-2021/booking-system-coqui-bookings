import psycopg2

from config.dbconfig import db_root_config


class BookingInviteeDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Create
    def createNewInvitee(self, booking_id, user_id):
        cursor = self.conn.cursor()
        query = 'insert into "BookingInvitee" (booking_id, user_id) values (%s,%s)'
        cursor.execute(query, (booking_id, user_id,))
        self.conn.commit()
        return True

    # Read
    def getAllInvitees(self):
        cursor = self.conn.cursor()
        query = 'select booking_id, user_id ' \
                'from "User" natural inner join "Booking" natural inner join "BookingInvitee";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteesByBookingIdAdminLevel(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select user_id, user_email, user_password, user_first_name, user_last_name, role_id ' \
                'from "BookingInvitee" natural inner join "User" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteesByBookingIdStudentLevel(self, booking_id):
        cursor = self.conn.cursor()
        query = 'select user_email, user_first_name, user_last_name ' \
                'from "BookingInvitee" natural inner join "User" where booking_id = %s;'
        cursor.execute(query, (booking_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteeUserHasBeenMostBookedWith(self, user_id):
        cursor = self.conn.cursor()
        query = 'select "Booking".user_id, BI.user_id, count(BI.user_id) as times_booked_invitee from "Booking"inner join "BookingInvitee" BI on "Booking".booking_id = BI.booking_id ' \
                'where "Booking".user_id = %s group by "Booking".user_id, BI. user_id order by count(BI.user_id) desc'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
        
    def verifyInviteeInBooking(self, booking_id, user_id):
        cursor = self.conn.cursor()
        query = 'select booking_id, user_id from "BookingInvitee" where booking_id = %s and user_id = %s;'
        cursor.execute(query, (booking_id,user_id,))
        result = cursor.fetchone()
        return result

    # Delete
    def deleteInvitee(self, booking_id, user_id):
        cursor = self.conn.cursor()
        query = 'delete from "BookingInvitee" where booking_id = %s and user_id = %s;'
        cursor.execute(query, (booking_id, user_id))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0
