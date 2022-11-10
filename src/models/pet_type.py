from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Range
from marshmallow.exceptions import ValidationError


class PetType(db.Model):
    __tablename__ = 'pet_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    pets = db.relationship('Pet', back_populates = 'type', cascade = 'all, delete')

class PetTypeSchema(ma.Schema):
    pets = fields.List(fields.Nested('PetSchema', exclude = ['client', 'type', 'bookings']))

    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError('Type name must be longer than 2 characters')
            
        stmt = db.select(PetType).filter_by(name = value.capitalize())
        type_name = db.session.scalar(stmt)

        if type_name:
            raise ValidationError('Pet type already exists')

    class Meta:
        fields = ('id', 'name', 'pets')
        ordered = True