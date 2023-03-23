from datetime import datetime, timedelta
from functools import wraps

import MySQLdb
import bcrypt as bcrypt
from flask import Flask, request, jsonify, make_response
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
        return self.id_record, self.id_good, self.id_colour_shoes, self.id_size_shoes, self.status, self.all_summ, \
               self.id_customer


def db_connect():
    connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='admin', db='flask')
    return connect


def finds_id(colum, table, goods_id):
    c = db_connect().cursor()
    project_id = f"SELECT {colum} FROM {table} WHERE names_id = %s"
    argument_for_add = goods_id
    c.execute(project_id, [argument_for_add])
    find_id = c.fetchall()
    return find_id


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        c = db_connect().cursor()

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        if BlackJWTList.query.get(token):
            return jsonify({'message': 'User is not logged in'})
        try:
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            user_find_id = "SELECT id FROM user WHERE gmail = %s"
            argument = data['email']
            c.execute(user_find_id, [argument])
            id_find = c.fetchall()
            current_user = User.query.get(id_find)
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


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
@token_required
def add_brand():
    brand = request.headers.get("name")
    prise = request.headers.get("cost")
    description = request.headers.get("des")
    size_id = request.headers.get("size_id")
    colour_id = request.headers.get("colour_id")
# Create goods
    names = Names(name=brand, description=description, prise=prise)
    db.session.add_all([names])
# do relations
    sizes = Sizes.query.get(size_id)
    names.nam.append(sizes)

    colours = Colours.query.get(colour_id)
    names.nam_2.append(colours)
    db.session.commit()
    return "good was added"


@app.route("/add_colour", methods=("POST", "GET"))
@token_required
# add colour to table Colours
def add_colour():
    colour_name = request.headers.get("colour")
    colours = Colours(colour=colour_name)
    db.session.add_all([colours])
    db.session.commit()
    return str(colours), "was added"


@app.route("/add_size", methods=("POST", "GET"))
@token_required
# add size to table Sizes
def add_size():
    size_number = request.headers.get("size")
    sizes = Sizes(size=size_number)
    db.session.add_all([sizes])
    db.session.commit()
    return str(sizes), "was added"


@app.route("/del_brand", methods=["DELETE"])
@token_required
# del name from table Names
def del_from_names():
    del_names_id = request.headers.get("del_names_id")
    id_names = Names.query.get(del_names_id)
    db.session.delete(id_names)
    db.session.commit()
    return "success"


@app.route("/del_colour", methods=["DELETE"])
@token_required
# del colour from table Colours
def del_from_colours():
    del_colour_id = request.headers.get("del_colours_id")
    id_colour = Colours.query.get(del_colour_id)
    db.session.delete(id_colour)
    db.session.commit()
    return "success"


@app.route("/del_size", methods=["DELETE"])
@token_required
# del size from table Sizes
def del_from_sizes():
    del_size_id = request.headers.get("del_sizes_id")
    id_size = Sizes.query.get(del_size_id)
    db.session.delete(id_size)
    db.session.commit()
    return "success"


@app.route("/update", methods=["PUT"])
@token_required
def update_brands():
    update_name_id = request.headers.get("update_name_id")
    if not update_name_id:
        return "No name id"
    update_name = request.headers.get("update_name")
    update_description = request.headers.get("update_description")
    update_prise = request.headers.get("update_prise")
    update_name_shoes_id = request.headers.get("update_name_shoes_id")
    update_size_choose_shoes_id = request.headers.get("update_size_shoes_id")
    update_colour_choose_shoes_2_id = request.headers.get("update_colour_shoes_id")

    user_size = Sizes.query.get(update_size_choose_shoes_id)
    user_colour = Colours.query.get(update_colour_choose_shoes_2_id)
    user = Names.query.get(update_name_shoes_id)
    list_for_checking = [update_name, update_description, update_prise, user_size, user_colour]
    for item in list_for_checking:
        if item:
            user.name = update_name
            user.description = update_description
            user.prise = update_prise
            user.nam = [user_size]
            user.nam_2 = [user_colour]
        else:
            return 'Please check your data again'
    db.session.commit()
    return "success"


@app.route("/info_one", methods=["GET"])
@token_required
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
                 "user_size_id": user_size.id,
                 "user_size": user_size.size,
                 "user_colour_id": user_colour.id,
                 "user_colour": user_colour.colour}
    return jsonify(str(user_dict))


@app.route("/info_all", methods=["GET"])
@token_required
def info_many():
    def filter_goods(user_list, filter_key, filter_value):
        try:
            values = [int(filter_value)]
            filter_list = [d for d in user_list if d[filter_key] in values]
            return filter_list
        except:
            values = [filter_value]
            filter_list = [d for d in user_list if d[filter_key] in values]
            return filter_list

    def sort_goods(user_list, sort_key, sort_value, less_or_more):
        if less_or_more == "less":
            sort_list = [d for d in user_list if d[sort_key] <= int(sort_value)]
            return sort_list
        elif less_or_more == "more":
            sort_list = [d for d in user_list if d[sort_key] > int(sort_value)]
            return sort_list

    filter_value = request.headers.get("filter_value")
    filter_key = request.headers.get("filter_key")
    sort_key = request.headers.get("sort_key")
    sort_value = request.headers.get("sort_value")
    less_or_more = request.headers.get('less_or_more')

    c = db_connect().cursor()

    users = Names.query.all()
    user_list = []

    for user_id in users:
        user = Names.query.get(user_id.id)

        find_colour_id = finds_id('colours_id', 'choose_shoes_2', user_id.id)
        find_size_id = finds_id('size_id', 'choose_shoes', user_id.id)

        if find_colour_id and find_size_id:
            user_colour = Colours.query.get(find_colour_id)
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
    if filter_value and filter_key:
        filter_goods(user_list, filter_key, filter_value)
        return jsonify(str(filter_goods))
    elif sort_key and sort_value:
        sort_goods(user_list, sort_key, sort_value, less_or_more)
        return jsonify(str(sort_goods))
    else:
        return jsonify(str(user_list))


@app.route("/add_to_basket")
@token_required
def add_basket(current_user):
    c = db_connect().cursor()

    id_shoes = request.headers.get("id_good")
    num_record = request.headers.get("num_record")
    stat = request.headers.get("status")

    customer = current_user.id
    shoes = Names.query.get(id_shoes)
    find_colour_id = finds_id('colours_id', 'choose_shoes_2', shoes.id)
    find_size_id = finds_id('size_id', 'choose_shoes', shoes.id)

    user_colour = Colours.query.get(find_colour_id)
    user_size = Sizes.query.get(find_size_id)
    basket = Basket(id_record=num_record, id_good=shoes.id, id_colour_shoes=user_colour.id, id_size_shoes=user_size.id,
                    status=stat, all_summ=shoes.prise, id_customer=customer)
    db.session.add_all([basket])
    db.session.commit()
    return 'successfully'


@app.route('/change_status')
@token_required
def status_change():
    new_status = request.headers.get("new_status")
    id_for_change = request.headers.get("id_for_change")
    basket_id_for_change = Basket.query.get(id_for_change)
    if new_status:
        basket_id_for_change.status = new_status
    else:
        if basket_id_for_change.status == "in the basket":
            db.session.delete(basket_id_for_change)
            return "success delete "
        else:
            return "Your status don`t in the basket"
    db.session.commit()
    return new_status


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="localhost")
