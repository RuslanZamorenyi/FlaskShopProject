# from functools import wraps
#
# import MySQLdb
# import jwt
# from flask import request, jsonify
#
# from main_folder.models import BlackJWTList, User
# # from main_folder.route_link import db_con
#
# JWT_SECRET = 'secret'
# JWT_ALGORITHM = 'HS256'
# JWT_EXP_DELTA_SECONDS = 200
#
#
# def db_con():
#     conn = MySQLdb.connect(host='127.0.0.1',
#                            user='root',
#                            passwd='admin',
#                            db='flask')
#     return conn
#
# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         c = db_con().cursor()
#
#         token = None
#
#         if 'x-access-tokens' in request.headers:
#             token = request.headers['x-access-tokens']
#
#         if not token:
#             return jsonify({'message': 'a valid token is missing'})
#         if BlackJWTList.query.get(token):
#             return jsonify({'message': 'User is not logged in'})
#         try:
#             data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
#             user_find_id = "SELECT id FROM user WHERE gmail = %s"
#             argums = data['email']
#             c.execute(user_find_id, [argums])
#             id_find = c.fetchall()
#             current_user = User.query.get(id_find)
#         except:
#             return jsonify({'message': 'token is invalid'})
#
#         return f(current_user, *args, **kwargs)
#
#     return decorator