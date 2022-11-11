from init import db, ma, bcrypt
from marshmallow import fields, validates
from marshmallow.validate import And, Length, OneOf, Regexp
from marshmallow.exceptions import ValidationError

VALID_ADMIN_STATUSES = ('true', 'True', 'false', 'False')


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)

    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, default = False)

    user = db.relationship('User', cascade = 'all, delete')
    bookings = db.relationship('Booking', back_populates = 'employee')
    rosters = db.relationship('Roster', back_populates = 'employee', cascade = 'all, delete')

class EmployeeSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['employee'])
    rosters = fields.List(fields.Nested('RosterSchema', exclude = ['employee']))
    bookings = fields.List(fields.Nested('BookingSchema', exclude = ['employee']))

    
    is_admin = fields.String(validate = OneOf(VALID_ADMIN_STATUSES))
    password = fields.String(required=True, validate=And(
        Length(min=6, error='Password must be at least 6 characters.'),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).*$', error='Password must inlcude at least one uppercase letter, one lowercase letter, one digit and one special character.')
    ))

    class Meta:
        fields = ('id', 'user', 'password', 'email', 'is_admin', 'bookings', 'rosters')
        ordered = True
    