from init import db, ma
from marshmallow import fields

class PetType(db.Model):
    __tablename__ = 'pet_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    pet = db.relationship('Pet', back_populates = 'type')

class PetTypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')
        ordered = True