from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError

class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False)
    weight = db.Column(db.String(20), nullable=False)

    pets = db.relationship('Pet', back_populates = 'size', cascade='all, delete')

class SizeSchema(ma.Schema):
    pets = fields.List(fields.Nested('PetSchema', exclude = ['size']))

    @validates('name')
    def validate_name(self, value):
        
        #get a size whose name matches requested name
        stmt = db.select(Size).filter_by(name = value.capitalize())
        size = db.session.scalar(stmt)

        #if size name already exists, raise ValidationError
        if size:
            raise ValidationError('Pet size already exists')

    class Meta:
        fields = ('id', 'weight', 'name', 'pets')
        ordered = True