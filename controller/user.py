from flask import jsonify
from model.user import UserDAO


class BaseUser:
    def build_user_map_dict(self, row):
        result = {'user_id': row[0], 'user_email': row[1], 'user_password': row[2], 'user_first_name': row[3],
                  'user_last_name': row[4], 'role_id': row[5]}
        return result

    def build_user_attr_dict(self, user_id, user_email, user_password, user_first_name, user_last_name, role_id):
        result = {'user_id': user_id, 'user_email': user_email, 'user_password': user_password,
                  'user_first_name': user_first_name, 'user_last_name': user_last_name, 'role_id': role_id}
        return result

    def build_unavailable_time_user_dict(self, row):
        result = {'unavailable_time_user_id': row[0], 'unavailable_time_user_start': row[1], 'unavailable_time_user_finish': row[2],
                  'user_id': row[3]}
        return result

    # Create
    def createNewUser(self, json):
        user_email = json['user_email']
        user_password = json['user_password']
        user_first_name = json['user_first_name']
        user_last_name = json['user_last_name']
        role_id = json['role_id']
        dao = UserDAO()
        existing_user = dao.getUserByEmail(user_email)
        if not existing_user:  # User with that email does not exists
            user_id = dao.createNewUser(user_email, user_password, user_first_name, user_last_name, role_id)
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name, role_id)
            return jsonify(result), 201
        else:
            return jsonify("An user with that email address already exists"), 409

    # Read
    def getAllUsers(self):
        dao = UserDAO()
        users_list = dao.getAllUsers()
        if not users_list:  # User List is empty
            return jsonify("No Users Found"), 404
        else:
            result_list = []
            for row in users_list:
                obj = self.build_user_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def getUserById(self, user_id):
        dao = UserDAO()
        user_tuple = dao.getUserById(user_id)
        if not user_tuple:  # User Not Found
            return jsonify("User Not Found"), 404
        else:
            result = self.build_user_map_dict(user_tuple)
            return jsonify(result), 200

    def getAllUnavailableUsers(self):
        dao = UserDAO()
        unavailable_users_list = dao.getAllUnavailableUsers()
        result_list = []
        for row in unavailable_users_list:
            obj = self.build_unavailable_time_user_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    # verify if user is available, return True if available 
    def verifyAvailableUserAtTimeFrame(self, user_id, start_time, start_finish):
        dao = UserDAO()
        user_times = dao.getUnavailableTimeForUser(user_id)

        if not user_times: return True

        





        return False

    def getUnavailableUserById(self, user_id):
        dao = UserDAO()
        unavailable_user_tuple = dao.getUnavailableUserById(user_id)
        if not unavailable_user_tuple:  # Unavailable User Not Found
            return jsonify("Unavailable User Not Found"), 404
        else:
            result = self.build_unavailable_time_user_dict(unavailable_user_tuple)
            return jsonify(result), 200

    # Update
    def updateUser(self, user_id, json):
        user_email = json['user_email']
        user_password = json['user_password']
        user_first_name = json['user_first_name']
        user_last_name = json['user_last_name']
        role_id = json['role_id']
        dao = UserDAO()
        existing_user = dao.getUserById(user_id)
        existing_email = dao.getUserByEmail(user_email)

        if not existing_user:  # User does not exist
            return jsonify("User Not Found"), 404
        # New email is different from current and new one is used
        elif existing_user[1] != user_email and existing_email:
            return jsonify("An user with that email address already exists"), 409
        else:
            dao.updateUser(user_id, user_email, user_password, user_first_name, user_last_name, role_id,)
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name,
                                               role_id,)
            return jsonify(result), 200

    # Delete
    def deleteUser(self, user_id):
        dao = UserDAO()
        result = dao.deleteUser(user_id)
        if result:
            return jsonify("User Deleted Successfully"), 200
        else:
            return jsonify("User Not Found"), 404
