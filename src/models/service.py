from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Range
from marshmallow.exceptions import ValidationError

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    bookings = db.relationship('Booking', back_populates = 'service', cascade = 'all, delete')

class ServiceSchema(ma.Schema):
    duration = fields.Float(required=True, validate=(Range(min=0.25)))
    price = fields.Float(required=True, validate=(Range(min=20)))
    bookings = fields.List(fields.Nested('BookingSchema', exclude=['service']))

    @validates('name')
    def validate_name(self, value):
        if len(value) < 2:
            raise ValidationError('Type name must be longer than 2 characters')
            
        stmt = db.select(Service).filter_by(name = value.capitalize())
        type_name = db.session.scalar(stmt)

        if type_name:
            raise ValidationError('Service already exists')
    
    class Meta:
        fields = ('id', 'name', 'duration', 'price', 'bookings')
        ordered = True