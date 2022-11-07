from init import db, ma 
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp
from datetime import date

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(15))
    date_created = db.Column(db.Date, default = date.today())
    phone = db.Column(db.String, nullable=False, unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('user_types.id'), nullable=False)
    personal_email = db.Column(db.String)

    type = db.relationship('UserType')
    client = db.relationship('Client', back_populates = 'user', cascade = 'all, delete')
    employee = db.relationship('Employee', back_populates = 'user', cascade = 'all, delete')

class UserSchema(ma.Schema):

    phone = fields.String(required = True,
    validate = And(Length(min=6, max=6, error = 'Phone number must be 6 digit long'),
    Regexp('^[0-9]+$', error = 'Phone can only contain numbers')
    ))

    class Meta:
        fields = ('id', 'f_name', 'l_name', 'phone', 'personal_email', 'employee', 'client')
        ordered = True