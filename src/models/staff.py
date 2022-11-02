from init import db, ma, bcrypt
from marshmallow import fields


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String, default = bcrypt.generate_password_hash('user123').decode('utf8'))
    is_admin = db.Column(db.Boolean, default = False)

    user = db.relationship('User', viewonly=True)

class StaffSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['staff', 'client'])

    class Meta:
        fields = ('user', 'email', 'password', 'is_admin')
        ordered = True
    