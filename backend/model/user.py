import psycopg2

from backend.config.dbconfig import db_root_config


class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Create
    def createNewUser(self, user_email, user_password, user_first_name, user_last_name, role_id):
        cursor = self.conn.cursor()
        query = 'insert into "User" (user_email, user_password, user_first_name, user_last_name, role_id) values (%s,' \
                '%s,%s,%s,%s) returning user_id; '
        cursor.execute(query, (user_email, user_password, user_first_name, user_last_name, role_id,))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def createUnavailableUserTimeFrame(self, user_id, unavailable_time_user_start, unavailable_time_user_finish):
        cursor = self.conn.cursor()
        query = 'insert into "UnavailableTimeUser" ' \
                '(unavailable_time_user_start, unavailable_time_user_finish, user_id) values (%s, %s, %s);'
        cursor.execute(query, (unavailable_time_user_start, unavailable_time_user_finish, user_id,))
        self.conn.commit()
        return True

    # Read
    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select user_id, user_email, user_password, user_first_name, user_last_name, role_id from "User";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, user_id):
        cursor = self.conn.cursor()
        query = 'select user_id, user_email, user_password, user_first_name, user_last_name, role_id ' \
                'from "User" where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def getUserRoleById(self, user_id):
        cursor = self.conn.cursor()
        query = 'select role_id ' \
                'from "User" where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def getAllUnavailableTimeOfUsers(self):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_user_id, unavailable_time_user_start, unavailable_time_user_finish, user_id ' \
                'from "UnavailableTimeUser";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUnavailableTimeOfUserById(self, user_id):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_user_id, unavailable_time_user_start, unavailable_time_user_finish, user_id ' \
                'from "UnavailableTimeUser" where user_id = %s;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Used in User Schedule
    def getUnavailableTimeOfUserByIdAndDate(self, user_id, date_start, date_finish):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_user_id, unavailable_time_user_start, unavailable_time_user_finish, user_id ' \
                'from "UnavailableTimeUser" where user_id = %s and unavailable_time_user_start >= %s and ' \
                'unavailable_time_user_finish <= %s;'
        cursor.execute(query, (user_id, date_start, date_finish,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserByEmail(self, user_email):
        cursor = self.conn.cursor()
        query = 'select user_id, user_email, user_password, user_first_name, user_last_name, role_id ' \
                'from "User" where user_email = %s;'
        cursor.execute(query, (user_email,))
        result = cursor.fetchone()
        return result

    def getUsedRoomsByUserId(self, user_id):
        cursor = self.conn.cursor()
        query = 'select room_id, room_name, count(room_id) as times_used from "Booking" ' \
                'natural inner join "Room" where user_id = %s group by room_id, room_name order by times_used desc;'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteeUserHasBeenMostBookedWith(self, user_id):
        cursor = self.conn.cursor()
        query = 'select "Booking".user_id, BI.user_id, count(BI.user_id) as times_booked_invitee ' \
                'from "Booking"inner join "BookingInvitee" BI on "Booking".booking_id = BI.booking_id ' \
                'where "Booking".user_id = %s group by "Booking".user_id, BI. user_id order by count(BI.user_id) desc'
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Update
    def updateUser(self, user_id, user_email, user_password, user_first_name, user_last_name, role_id):
        cursor = self.conn.cursor()
        query = 'update "User" ' \
                'set user_email = %s, user_password = %s, user_first_name = %s, user_last_name = %s , role_id = %s ' \
                'where user_id = %s '
        cursor.execute(query, (user_email, user_password, user_first_name, user_last_name, role_id, user_id))
        self.conn.commit()
        return True

    # Delete
    def deleteUser(self, user_id):
        cursor = self.conn.cursor()
        query = 'delete from "User" where user_id = %s;'
        cursor.execute(query, (user_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    # Used in Update Booking Only
    def deleteUnavailableUserTimeFrame(self, user_id, start_time, finish_time):
        cursor = self.conn.cursor()
        query = 'delete from "UnavailableTimeUser" where user_id = %s and unavailable_time_user_start = %s ' \
                'and unavailable_time_user_finish = %s;'
        cursor.execute(query, (user_id, start_time, finish_time,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0
