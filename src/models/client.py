from init import db, ma
from marshmallow import fields

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)

    user = db.relationship('User', back_populates = 'client', cascade = 'all, delete')
    pets = db.relationship('Pet', back_populates = 'client')

class ClientSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['client', 'employee', 'id'])
    pets = fields.List(fields.Nested('PetSchema', exclude = ['client']))

    class Meta:
        fields = ('id', 'user', 'pets')
        ordered = True