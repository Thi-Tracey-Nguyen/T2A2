from init import db, ma 
from marshmallow import fields
from marshmallow.validate import And, Length, Regexp

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(15))
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String)

    pet = db.relationship('Pet', back_populates = 'client', cascade = 'all, delete')

class ClientSchema(ma.Schema):
    pet = fields.List(fields.Nested('PetSchema', only = ['name', 'type_id', 'size']))

    phone = fields.String(required = True,
    validate = And(Length(min=6, error = 'Phone number must be 6 digit long'),
    Regexp('^[0-9]+$', error = 'Phone can only contain numbers')
    ))

    class Meta:
        fields = ('id', 'f_name', 'l_name', 'phone', 'email', 'pet')
        ordered = True