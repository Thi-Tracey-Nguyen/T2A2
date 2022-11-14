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
        #pet type name must be longer than 2 characters
        if len(value) < 2:
            raise ValidationError('Type name must be longer than 2 characters')
        
        #get the pet type whose name matches requested name
        stmt = db.select(PetType).filter_by(name = value.capitalize())
        type_name = db.session.scalar(stmt)

        #if pet type already exists, raise ValidationError
        if type_name:
            raise ValidationError('Pet type already exists')

    class Meta:
        fields = ('id', 'name', 'pets')
        ordered = True