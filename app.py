from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:admin@127.0.0.1/flask"
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


@app.route("/information", methods=("POST", "GET"))
def inf():
    """Get info from postman"""
    bran = request.headers.get("name")
    cos = request.headers.get("cost")
    desc = request.headers.get("des")
    siz = request.headers.get("size")
    col = request.headers.get("colour")
    """Create instance of a class"""
    names = Names(name=bran, description=desc, prise=cos)
    sizes = Sizes(size=siz)
    colours = Colours(colour=col)
    db.session.add_all([names, sizes, colours])
    db.session.commit()
    """Do relationship"""
    names.nam.append(sizes)
    db.session.commit()
    names.nam_2.append(colours)
    db.session.commit()
    return "Product has been added"


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="localhost")
