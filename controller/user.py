import time

from flask import jsonify
from model.user import UserDAO
import datetime as dt


class BaseUser:
    def build_user_map_dict(self, row):
        result = {'user_id': row[0], 'user_email': row[1], 'user_password': row[2], 'user_first_name': row[3],
                  'user_last_name': row[4], 'role_id': row[5]}
        return result

    def build_user_attr_dict(self, user_id, user_email, user_password, user_first_name, user_last_name, role_id):
        result = {'user_id': user_id, 'user_email': user_email, 'user_password': user_password,
                  'user_first_name': user_first_name, 'user_last_name': user_last_name, 'role_id': role_id}
        return result

    def build_unavailable_time_user_map_dict(self, row):
        result = {'unavailable_time_user_id': row[0], 'unavailable_time_user_start': row[1],
                  'unavailable_time_user_finish': row[2], 'user_id': row[3]}
        return result

    def build_role_map_dict(self, row):
        result = {'role_id': row[0]}
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
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name,
                                               role_id)
            return jsonify("result"), 201
        else:
            return jsonify("An user with that email address already exists"), 409

    # TODO IT ADDS DUPLICATES (SEND HELP)
    def createUserUnavailableTimeSlot(self, user_id, json):
        unavailable_time_user_start = json['unavailable_time_user_start']
        unavailable_time_user_finish = json['unavailable_time_user_finish']
        dao = UserDAO()
        existing_user = dao.getUserById(user_id)
        if not existing_user:
            return jsonify("User Not Found"), 404
        available_user = self.verifyAvailableUserAtTimeFrame(user_id, unavailable_time_user_start,
                                                             unavailable_time_user_finish)
        if not available_user:
            return jsonify("Time slot overlaps"), 409
        else:
            dao.createUserUnavailableTimeSlot(user_id, unavailable_time_user_start,
                                                       unavailable_time_user_finish)
            return jsonify('Successfully inserted unavailable slot'), 201

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

    def getUserRoleById(self, user_id):
        dao = UserDAO()
        user_role = dao.getUserRoleById(user_id)
        if not user_role:  # User Not Found
            return jsonify("User Not Found"), 404
        else:
            result = self.build_role_map_dict(user_role)
            return jsonify(result), 200

    def getAllUnavailableTimeOfUsers(self):
        dao = UserDAO()
        unavailable_users_list = dao.getAllUnavailableTimeOfUsers()
        result_list = []
        for row in unavailable_users_list:
            obj = self.build_unavailable_time_user_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getUnavailableTimeOfUserById(self, user_id):
        dao = UserDAO()
        user = dao.getUserById(user_id)
        if not user:  # User Not Found
            return jsonify("User Not Found"), 404
        unavailable_user_tuple = dao.getUnavailableTimeOfUserById(user_id)
        if not unavailable_user_tuple:  # Unavailable Time Slot Not Found
            return jsonify("No Unavailable Time Slots Found for this User"), 404
        else:
            result_list = []
            for row in unavailable_user_tuple:
                obj = self.build_unavailable_time_user_map_dict(row)
                result_list.append(obj)
            return jsonify(result_list), 200

    def verifyAvailableUserAtTimeFrame(self, user_id, start_time_to_verify, finish_time_to_verify):
        dao = UserDAO()
        new_start = dt.datetime.strptime(start_time_to_verify, '%Y-%m-%d %H:%M')
        new_end = dt.datetime.strptime(finish_time_to_verify, '%Y-%m-%d %H:%M')

        user_unavailable_time_slots = dao.getUnavailableTimeOfUserById(user_id)
        if not user_unavailable_time_slots:
            return True
        else:
            for row in user_unavailable_time_slots:
                old_start = row[1]
                old_end = row[2]      
                if (old_start < new_start < new_end < old_end) \
                        or (new_start < old_start < old_end < new_end) \
                        or (new_start < old_start < new_end < old_end) \
                        or (old_start < new_start < old_end < new_end)\
                        or (new_start==old_start or new_end==old_end):
                    return False
            return True

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
            dao.updateUser(user_id, user_email, user_password, user_first_name, user_last_name, role_id, )
            result = self.build_user_attr_dict(user_id, user_email, user_password, user_first_name, user_last_name,
                                               role_id, )
            return jsonify(result), 200

    # Delete
    def deleteUser(self, user_id):
        dao = UserDAO()
        result = dao.deleteUser(user_id)
        if result:
            return jsonify("User Deleted Successfully"), 200
        else:
            return jsonify("User Not Found"), 404
