# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
#
# class Names(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     description = db.Column(db.String(100), nullable=False)
#     prise = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return self.name, self.description, self.prise
#
#
# class Sizes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     size = db.Column(db.String(80), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('names.id'))
#
#     def __repr__(self):
#         return self.size
#
#
# class Colours(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     colour = db.Column(db.String(80), nullable=False)
#     nam_id = db.Column(db.Integer, db.ForeignKey('names.id'))
#
#     def __repr__(self):
#         return self.colur