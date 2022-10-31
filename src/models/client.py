from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(15))
    phone = db.Column(db.String(6), nullable=False, unique=True)
    email = db.Column(db.String)

    # pet = db.relationship('Pet', back_populates = ['client_id'])

class ClientSchema(ma.Schema):
    # pet = fields.List(fields.Nested('PetSchema', only = ['name', 'type', 'size']))

    phone = fields.String(required = True, validate = Length(min = 6, error = 'Phone number must be 6 digit long'))

    class Meta:
        fields = ('id', 'f_name', 'l_name', 'phone', 'email')
        ordered = True