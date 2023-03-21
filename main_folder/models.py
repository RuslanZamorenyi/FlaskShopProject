# from main_folder.database import db
#
# choose_shoes = db.Table('choose_shoes',
#     db.Column('names_id', db.Integer, db.ForeignKey('names.id')),
#     db.Column('sizes_id', db.Integer, db.ForeignKey('sizes.id'))
# )
# choose_shoes_2 = db.Table('choose_shoes_2',
#     db.Column('names_id', db.Integer, db.ForeignKey('names.id')),
#     db.Column('colours_id', db.Integer, db.ForeignKey('colours.id'))
# )
#
#
# """Create models"""
# class Names(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     description = db.Column(db.String(100), nullable=False)
#     prise = db.Column(db.Integer, nullable=False)
#     nam = db.relationship('Sizes', lazy='dynamic', secondary=choose_shoes)
#     nam_2 = db.relationship('Colours', lazy='dynamic', secondary=choose_shoes_2)
#
#     def __repr__(self):
#         return self.name, self.description, self.prise
#
#
# class Sizes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     size = db.Column(db.String(80), nullable=False)
#
#     def __repr__(self):
#         return self.size
#
#
# class Colours(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     colour = db.Column(db.String(80), nullable=False)
#
#     def __repr__(self):
#         return self.colour
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False)
#     gmail = db.Column(db.String(20), unique=True)
#     password = db.Column(db.String(200), nullable=False)
#
#     def __repr__(self):
#         return self.gmail, self.password
#
#
# class BlackJWTList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(200))
#
#
# class Basket(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     id_record = db.Column(db.Integer, nullable=False)
#     id_good = db.Column(db.Integer, nullable=False)
#     id_colour_shoes = db.Column(db.Integer, nullable=False)
#     id_size_shoes = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.String(20), nullable=False)
#     all_summ = db.Column(db.Integer, nullable=False)
#     id_customer = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return self.id_record, self.id_good, self.id_colour_shoes, self.id_size_shoes, self.status, self.all_summ, self.id_customer
