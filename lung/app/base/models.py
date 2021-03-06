from datetime import datetime
from bcrypt import gensalt, hashpw
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String

from app import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    picture = Column(String(20), nullable=False, default='default.jpg')

    patients = db.relationship('Patient', backref='doctor', lazy=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'password':
                value = hashpw(value.encode('utf8'), gensalt())
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class Patient(db.Model):
    # id of patient
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String)
    address = db.Column(db.String)

    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    health_condition = db.Column(db.String)
    diabetes = db.Column(db.String)
    blood_pressure = db.Column(db.Integer)
    cancer_report = db.Column(db.String)
    other_problems = db.Column(db.String)

    picture = Column(String(20), nullable=False, default='default.png')
    ct_scan = db.Column(db.String)

    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # id of user
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f"Patients('{self.first_name}', '{self.last_name}')"

    # @property
    # def serialize(self):
    #     """Return object data in easily serializable format"""
    #     return {
    #         'id': self.id,
    #         # This is an example how to deal with Many2Many relations
    #         'many2many': self.serialize_many2many
    #     }
    #
    # @property
    # def serialize_many2many(self):
    #     """
    #     Return object's relations in easily serializable format.
    #     NB! Calls many2many's serialize property.
    #     """
    #     return [item.serialize for item in self.many2many]







