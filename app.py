from datetime import datetime, timedelta
from functools import wraps

import MySQLdb
import bcrypt as bcrypt
import flask_login
from flask import Flask, request, json, jsonify, make_response
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:admin@127.0.0.1/flask"
app.config['SECRET_KEY'] = 'ruslan'
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 200
db = SQLAlchemy(app)
migrate = Migrate(app, db)


choose_shoes = db.Table('choose_shoes',
    db.Column('names_id', db.Integer, db.ForeignKey('names.id')),
    db.Column('sizes_id', db.Integer, db.ForeignKey('sizes.id'))
)
choose_shoes_2 = db.Table('choose_shoes_2',
    db.Column('names_id', db.Integer, db.ForeignKey('names.id')),
    db.Column('colours_id', db.Integer, db.ForeignKey('colours.id'))
)


"""Create models"""
class Names(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    prise = db.Column(db.Integer, nullable=False)
    nam = db.relationship('Sizes', lazy='dynamic', secondary=choose_shoes)
    nam_2 = db.relationship('Colours', lazy='dynamic', secondary=choose_shoes_2)

    def __repr__(self):
        return self.name, self.description, self.prise


class Sizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.size


class Colours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colour = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.colour


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    gmail = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.gmail, self.password


class BlackJWTList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200))


class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_record = db.Column(db.Integer, nullable=False)
    id_good = db.Column(db.Integer, nullable=False)
    id_colour_shoes = db.Column(db.Integer, nullable=False)
    id_size_shoes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    all_summ = db.Column(db.Integer, nullable=False)
    id_customer = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.id_record, self.id_good, self.id_colour_shoes, self.id_size_shoes, self.status, self.all_summ, self.id_customer


@app.route('/signup', methods=['POST'])
def create_record():
    try:
        create_user(request.headers.get('gmail'), request.headers.get('password'), request.headers.get('surname'))
        return 'Created successfully'
    except:
        return "User already exist of check your data"


def create_user(gmail, password, surname):
    user = User(
        gmail=gmail,
        password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        username=surname)
    db.session.add_all([user])
    db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    user = User.query.filter_by(gmail=auth.username).first()
    if bcrypt.checkpw(auth.password.encode('utf-8'), user.password.encode('utf-8')):
        print(user.password)
        token = jwt.encode(
            {'email': user.gmail, 'exp': datetime.utcnow() + timedelta(minutes=30)}, JWT_SECRET, JWT_ALGORITHM)
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/logout', methods=['POST'])
def logout():
    token = request.headers['x-access-tokens']
    black_list_token = BlackJWTList(
        data=token)
    db.session.add(black_list_token)
    db.session.commit()
    return jsonify({"msg": "Successfully logged out"}), 200


@app.route("/add_brand", methods=("POST", "GET"))
def add_brand():
    bran = request.headers.get("name")
    cos = request.headers.get("cost")
    desc = request.headers.get("des")
    z_id = request.headers.get("size_id")
    c_id = request.headers.get("colour_id")
# Create goods
    names = Names(name=bran, description=desc, prise=cos)
    db.session.add_all([names])
    db.session.commit()
# do with models
    sizes = Sizes.query.get(z_id)
    names.nam.append(sizes)
    db.session.commit()

    colours = Colours.query.get(c_id)
    names.nam_2.append(colours)
    db.session.commit()

    return "bam"


@app.route("/add_colour", methods=("POST", "GET"))
def add_colour():
    col = request.headers.get("colour")
    colours = Colours(colour=col)
    db.session.add_all([colours])
    db.session.commit()
    return str(colours)


@app.route("/add_size", methods=("POST", "GET"))
def add_size():
    siz = request.headers.get("size")
    sizes = Sizes(size=siz)
    db.session.add_all([sizes])
    db.session.commit()
    return str(sizes)


@app.route("/del_brand", methods=["DELETE"])
def del_from_names():
    del_names_id = request.headers.get("del_names_id")
    id_names = Names.query.get(del_names_id)
    db.session.delete(id_names)
    db.session.commit()
    return "Done"


@app.route("/del_colour", methods=["DELETE"])
def del_from_colours():
    del_colours_id = request.headers.get("del_colours_id")
    id_colours = Colours.query.get(del_colours_id)
    db.session.delete(id_colours)
    db.session.commit()
    return "Done"


@app.route("/del_size", methods=["DELETE"])
def del_from_sizes():
    del_size_id = request.headers.get("del_sizes_id")
    id_sizes = Sizes.query.get(del_size_id)
    db.session.delete(id_sizes)
    db.session.commit()
    return "Done"


@app.route("/update", methods=["PUT"])
def update_brands():
    update_name_id = request.headers.get("update_name_id")
    if not update_name_id:
        return "No name id"
    update_name = request.headers.get("update_name")
    update_description = request.headers.get("update_description")
    update_prise = request.headers.get("update_prise")
    update_name_shoes_id = request.headers.get("update_name_shoes_id")
    update_size_shoes_id = request.headers.get("update_size_shoes_id")
    update_colour_shoes_id = request.headers.get("update_colour_shoes_id")

    user_z = Sizes.query.get(update_size_shoes_id)
    user_c = Colours.query.get(update_colour_shoes_id)
    user = Names.query.get(update_name_shoes_id)
    if update_name:
        user.name = update_name
    if update_description:
        user.description = update_description
    if update_prise:
        user.prise = update_prise
    if user_z:
        user.nam = [user_z]
    if user_c:
        user.nam_2 = [user_c]
    db.session.commit()
    return "Done"


@app.route("/info_one", methods=["GET"])
def info_one():
    get_name_id = request.headers.get("get_name_id")
    get_size_id = request.headers.get("get_size_id")
    get_colour_id = request.headers.get("get_colour_id")

    user = Names.query.get(get_name_id)
    user_size = Sizes.query.get(get_size_id)
    user_colour = Colours.query.get(get_colour_id)
    user_dict = {"user_id": user.id,
                 "user_name": user.name,
                 "user_description": user.description,
                 "user_prise": user.prise,
                 "user_size": user_size.size,
                 "user_colour": user_colour.colour}
    return jsonify(str(user_dict))


def db_con():
    conn = MySQLdb.connect(host='127.0.0.1',
                           user='root',
                           passwd='admin',
                           db='flask')
    return conn


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        # for i in BlackJWTList.query.get(token):
        #     if token == i['data']:
        #         return jsonify({'message': 'User is not logged in'})
        if BlackJWTList.query.get(token):
            return jsonify({'message': 'User is not logged in'})
        data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        print(data)
        current_user = User.query.filter_by(gmail=data['email']).first()
        print(str(current_user))

        try:
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            current_user = User.query.get(gmail=data['email'])

        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator
@app.route("/info_all", methods=["GET"])
def info_many():
    filter_value = request.headers.get("filter_value")
    filter_key = request.headers.get("filter_key")
    sort_key = request.headers.get("sort_key")
    sort_value = request.headers.get("sort_value")
    less_or_more = request.headers.get('less_or_more')

    c = db_con().cursor()

    users = Names.query.all()
    user_list = []

    for user_id in users:
        user = Names.query.get(user_id.id)
        colour_id = "SELECT colours_id FROM choose_shoes_2 WHERE names_id = %s"
        argum = user_id.id
        c.execute(colour_id, [str(argum)])
        find_id = c.fetchall()
        size_id = "SELECT sizes_id FROM choose_shoes WHERE names_id = %s"
        argums = user_id.id
        c.execute(size_id, [argums])
        find_size_id = c.fetchall()
        if find_id and find_size_id:
            user_colour = Colours.query.get(find_id)
            user_size = Sizes.query.get(find_size_id)
        else:
            user_colour = None
            user_size = None
        user_dict = {"user_id": user.id,
                     "user_name": user.name,
                     "user_description": user.description,
                     "user_prise": user.prise,
                     "user_size_id": user_size.id if user_size else None,
                     "user_size": user_size,
                     "user_colour_id": user_colour.id if user_colour else None,
                     "user_colour": str(user_colour)}
        user_list.append(user_dict)
# Filter goods
    if filter_value and filter_key:
        try:
            values = [int(filter_value)]
            filter_list = [d for d in user_list if d[filter_key] in values]
            return jsonify(str(filter_list))
        except:
            values = [filter_value]
            filter_list = [d for d in user_list if d[filter_key] in values]
            return jsonify(str(filter_list))
# Sort goods

    elif sort_key and sort_value:
        if less_or_more == "less":
            sort_list = [d for d in user_list if d[sort_key] <= int(sort_value)]
            return jsonify(str(sort_list))
        elif less_or_more == "more":
            sort_list = [d for d in user_list if d[sort_key] > int(sort_value)]
            return jsonify(str(sort_list))
    else:
        return jsonify(str(user_list))


@app.route("/add_to_basket")
@token_required
def add_basket():

    c = db_con().cursor()
    id_shoes = request.headers.get("id_good")
    num_record = request.headers.get("num_record")
    stat = request.headers.get("status")

    customer = current_user.id
    shoes = Names.query.get(id_shoes)

    colour_id = "SELECT colours_id FROM choose_shoes_2 WHERE names_id = %s"
    argum = shoes.id
    c.execute(colour_id, [str(argum)])
    find_id = c.fetchall()
    size_id = "SELECT sizes_id FROM choose_shoes WHERE names_id = %s"
    argums = shoes.id
    c.execute(size_id, [argums])
    find_size_id = c.fetchall()
    user_colour = Colours.query.get(find_id)
    user_size = Sizes.query.get(find_size_id)
    basket = Basket(id_record=num_record, id_good=shoes.id, id_colour_shoes=user_colour.id, id_size_shoes=user_size.id,
                    status=stat, all_summ=shoes.prise, id_customer=customer)
    db.session.add_all([basket])
    db.session.commit()
    return str([basket])



    # user_dict = {"user_id": user.id,
    #              "user_name": user.name,
    #              "user_description": user.description,
    #              "user_prise": user.prise,
    #              "user_size": user_size.size,
    #              "user_colour": user_colour.colour}
    # return jsonify(str(user_dict))

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="localhost")
