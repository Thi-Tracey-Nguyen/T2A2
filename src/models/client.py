from init import db, ma
from marshmallow import fields

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique = True)

    user = db.relationship('User', viewonly=True)
    pets = db.relationship('Pet', back_populates = 'client')

class ClientSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['client', 'staff'])
    pets = fields.List(fields.Nested('PetSchema', exclude = ['client']))

    class Meta:
        fields = ('user', 'pets')