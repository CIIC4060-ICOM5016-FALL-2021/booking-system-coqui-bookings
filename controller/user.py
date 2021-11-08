from flask import jsonify
from model.user import UserDAO


class BaseUser:
    def build_map_dict(self, row):
        result = {'user_id': row[0], 'user_email': row[1], 'user_password': row[2], 'user_first_name': row[3],
                  'user_last_name': row[4]}
        return result

    def getAllUsers(self):
        dao = UserDAO()
        part_list = dao.getAllUsers()
        result_list = []
        for row in part_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)
