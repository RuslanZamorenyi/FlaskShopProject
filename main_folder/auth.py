# from datetime import datetime, timedelta
#
# import bcrypt
# import jwt
# from flask import request, make_response, jsonify, Blueprint
#
# # from main_folder.app import db
#
# from main_folder.models import User, BlackJWTList, db
#
# auth = Blueprint('auth', __name__)
# JWT_SECRET = 'secret'
# JWT_ALGORITHM = 'HS256'
# JWT_EXP_DELTA_SECONDS = 200
#
# @auth.route('/signup', methods=['POST'])
# def create_record():
#     try:
#         create_user(request.headers.get('gmail'), request.headers.get('password'), request.headers.get('surname'))
#         return 'Created successfully'
#     except:
#         return "User already exist of check your data"
#
#
# def create_user(gmail, password, surname):
#     user = User(
#         gmail=gmail,
#         password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
#         username=surname)
#     db.session.add_all([user])
#     db.session.commit()
#
#
# @auth.route('/login', methods=['GET', 'POST'])
# def login_user():
#     auth = request.authorization
#     if not auth or not auth.username or not auth.password:
#
#         return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
#     user = User.query.filter_by(gmail=auth.username).first()
#     if bcrypt.checkpw(auth.password.encode('utf-8'), user.password.encode('utf-8')):
#         print(user.password)
#         token = jwt.encode(
#             {'email': user.gmail, 'exp': datetime.utcnow() + timedelta(minutes=30)}, JWT_SECRET, JWT_ALGORITHM)
#         return jsonify({'token': token})
#
#     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
#
#
# @auth.route('/logout', methods=['POST'])
# def logout():
#     token = request.headers['x-access-tokens']
#     black_list_token = BlackJWTList(
#         data=token)
#     db.session.add(black_list_token)
#     db.session.commit()
#     return jsonify({"msg": "Successfully logged out"}), 200

