from sqlalchemy import UniqueConstraint
from init import db, ma 
from marshmallow import fields

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    breed = db.Column(db.String(50), default = 'Unknown')
    year = db.Column(db.Integer, nullable=False)

    type_id = db.Column(db.Integer, db.ForeignKey('pet_types.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('name', 'client_id'),)

    client = db.relationship('Client', back_populates = 'pets')
    type = db.relationship('PetType')
    size = db.relationship('Size')

class PetSchema(ma.Schema):
    client = fields.Nested('ClientSchema', only = ['user'])
    type = fields.Nested('PetTypeSchema', only = ['name'])
    size = fields.Nested('SizeSchema', only = ['name'])

    class Meta:
        fields = ('id', 'name', 'breed', 'year', 'client', 'client_id', 'type', 'size')
        ordered = True