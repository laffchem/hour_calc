from . import db
from flask_login import UserMixin



class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    sessTime = db.Column(db.Float(5))
    supInd = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    hours = db.relationship('Hours')
