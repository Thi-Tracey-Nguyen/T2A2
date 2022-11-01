from init import db, ma
from marshmallow import fields

class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    weight = db.Column(db.String(20))

    pet = db.relationship('Pet', back_populates = 'size')

class SizeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'weight', 'name')
        ordered = True