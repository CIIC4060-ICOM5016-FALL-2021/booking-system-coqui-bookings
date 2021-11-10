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
    def createNewUser(self, user_email, user_password, user_first_name, user_last_name, role_id):
        cursor = self.conn.cursor()
        query = 'insert into "User" (user_email, user_password, user_first_name, user_last_name, role_id) values (%s,' \
                '%s,%s,%s,%s) returning user_id; '
        cursor.execute(query, (user_email, user_password, user_first_name, user_last_name, role_id,))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

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

    def getAllUnavailableUsers(self):
        cursor = self.conn.cursor()
        query = 'select unavailable_time_user_id, unavailable_time_user_start, unavailable_time_user_finish, user_id ' \
                'from "UnavailableTimeUser";'
        cursor.execute(query)
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

    # TODO: deleteUserFromBooking (Unavailable User)
