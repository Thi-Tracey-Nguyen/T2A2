from init import db, ma 
from marshmallow import fields

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    size = db.Column(db.String, nullable=False)
    breed = db.Column(db.String(50))
    year = db.Column(db.Integer, nullable=False)

    type_id = db.Column(db.ForeignKey('types.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    client = db.relationship('Client', back_populates = 'pet')
    type = db.relationship('Type')

class PetSchema(ma.Schema):
    client = fields.Nested('ClientSchema', only = ['f_name', 'l_name', 'phone'])
    type = fields.Nested('TypeSchema', only = ['name'])

    class Meta:
        fields = ('id', 'name', 'type_id', 'size', 'breed', 'client', 'type')
        ordered = True