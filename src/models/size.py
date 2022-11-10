from init import db, ma
from marshmallow import fields

class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    weight = db.Column(db.String(20))

    pets = db.relationship('Pet', back_populates = 'size', cascade='all, delete')

class SizeSchema(ma.Schema):
    pets = fields.List(fields.Nested('PetSchema', exclude = ['size']))

    class Meta:
        fields = ('id', 'weight', 'name', 'pets')
        ordered = True