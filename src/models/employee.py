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

    user = db.relationship('User', viewonly=True)
    bookings = db.relationship('Booking', back_populates = 'employee')

class EmployeeSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['employee', 'client', 'id'])
    bookings = fields.List(fields.Nested('BookingSchema', exclude = ['employee']))
    is_admin = fields.String(validate = OneOf(VALID_ADMIN_STATUSES))
    password = fields.String(required=True, validate=And(
        Length(min=6, error='Password must be at least 6 characters.'),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).*$', error='Password must inlcude at least one uppercase letter, one lowercase letter, one digit and one special character.')
    ))

    # @validates('password')
    # def validate_password(self, password):
    #     if not any(char.isdigit() for char in password):
    #         raise ValidationError('Password must contain a number')
    #     if len(password) < 6:
    #         raise ValidationError('Password must be at least 6 character long')

    class Meta:
        fields = ('id', 'user', 'password', 'email', 'is_admin', 'bookings')
        ordered = True
    