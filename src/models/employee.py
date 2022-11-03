from init import db, ma, bcrypt
from marshmallow import fields, validates
from marshmallow.validate import And, Length
from marshmallow.exceptions import ValidationError

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String, default = bcrypt.generate_password_hash('user123').decode('utf8'))
    is_admin = db.Column(db.Boolean, default = False)

    user = db.relationship('User', viewonly=True)


class EmployeeSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['employee', 'client'])

    @validates('password')
    def validate_password(self, password):
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain a number')
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 character long')

    class Meta:
        fields = ('id', 'user', 'password', 'email', 'is_admin')
        ordered = True
    