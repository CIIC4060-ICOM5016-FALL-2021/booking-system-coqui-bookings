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

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = 'select user_id, user_email, user_password, user_first_name, user_last_name from "User";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

