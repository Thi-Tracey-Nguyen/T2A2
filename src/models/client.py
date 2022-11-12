from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    password = db.Column(db.String)

    user = db.relationship('User', back_populates = 'client', cascade = 'all, delete')
    pets = db.relationship('Pet', back_populates = 'client', cascade = 'all, delete')

class ClientSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['employee', 'id'])
    pets = fields.List(fields.Nested('PetSchema', exclude = ['client']))
    password = fields.String(required=True, validate=And(
        Length(min=6, error='Password must be at least 6 characters.'),
        Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).*$', error='Password must inlcude at least one uppercase letter, one lowercase letter, one digit and one special character.')
    ))

    class Meta:
        fields = ('id', 'user', 'pets', 'password')
        ordered = True