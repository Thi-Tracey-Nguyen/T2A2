from init import db, ma 
from marshmallow import fields

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    breed = db.Column(db.String(50), default = 'Unknown')
    year = db.Column(db.Integer, nullable=False)

    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    client = db.relationship('Client', back_populates = 'pet')
    type = db.relationship('Type', back_populates = 'pet')
    size = db.relationship('Size', back_populates = 'pet')

class PetSchema(ma.Schema):
    client = fields.Nested('ClientSchema', only = ['f_name', 'l_name', 'phone'])
    type = fields.Nested('TypeSchema', only = ['name'])
    size = fields.Nested('SizeSchema', only = ['name'])

    class Meta:
        fields = ('id', 'name', 'breed', 'client', 'type', 'size')
        ordered = True