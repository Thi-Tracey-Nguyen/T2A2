from init import db, ma
from marshmallow import fields

class UserType(db.Model):
    __tablename__ = 'user_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    user = db.relationship('User', back_populates = 'type')

class UserTypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')
        ordered = True