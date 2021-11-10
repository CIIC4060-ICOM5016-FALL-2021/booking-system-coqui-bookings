from flask import jsonify
from model.user import UserDAO


class BaseUser:
    def build_map_dict(self, row):
        result = {'user_id': row[0], 'user_email': row[1], 'user_password': row[2], 'user_first_name': row[3],
                  'user_last_name': row[4], 'role_id': row[5]}
        return result

    def build_user_attr_dict(self, user_id, user_email, user_password, user_first_name, user_last_name, role_id):
        result = {}
        result['user_id'] = user_id
        result['user_email'] = user_email
        result['user_password'] = user_password
        result['user_first_name'] = user_first_name
        result['user_last_name'] = user_last_name
        result['role_id'] = role_id
        return result

    def build_unavailable_user_dict(self, row):
        result = {'unavailable_id': row[0], 'unavailable_time_start': row[1], 'unavailable_time_end': row[2],
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
        user_id = dao.createNewUser(user_email, user_password, user_first_name, user_last_name, role_id)
        result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name, role_id)
        return jsonify(result), 201

# Read
    def getAllUsers(self):
        dao = UserDAO()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getUserById(self, user_id):
        dao = UserDAO()
        user_tuple = dao.getUserById(user_id)
        if not user_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(user_tuple)
            return jsonify(result), 200

    def getAllUnavailableUsers(self):
        dao = UserDAO()
        unavailable_users_list = dao.getAllUnavailableUsers()
        result_list = []
        for row in unavailable_users_list:
            obj = self.build_unavailable_user_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

# Update
    def updateUser(self, json):
        user_email = json['user_email']
        user_password = json['user_password']
        user_first_name = json['user_first_name']
        user_last_name = json['user_last_name']
        role_id = json['role_id']
        user_id = json['user_id']
        dao = UserDAO()
        updated_code = dao.updateUser(user_id, user_email, user_password, user_first_name, user_last_name, role_id,)
        if not updated_code:
            return jsonify("Not Found"), 404
        else:
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name, role_id,)

            return jsonify(result), 200

    # Delete
    def deleteUser(self, user_id):
        dao = UserDAO()
        result = dao.deleteUser(user_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404