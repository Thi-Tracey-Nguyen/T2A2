from init import db, ma 
from models.client import Client
from models.pet_type import PetType
from models.size import Size
from marshmallow import fields, validates
from marshmallow.validate import Length
from marshmallow.exceptions import ValidationError

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    breed = db.Column(db.String(50), default = 'Unknown')
    year = db.Column(db.Integer, nullable=False)

    type_id = db.Column(db.Integer, db.ForeignKey('pet_types.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    __table_args__ = (db.UniqueConstraint('name', 'client_id', 'type_id'),)

    client = db.relationship('Client', back_populates = 'pets')
    bookings = db.relationship('Booking', back_populates = 'pet', cascade = 'all, delete')
    type = db.relationship('PetType')
    size = db.relationship('Size')

class PetSchema(ma.Schema):
    client = fields.Nested('ClientSchema', only = ['user', 'id'])
    type = fields.Nested('PetTypeSchema', only = ['name'])
    size = fields.Nested('SizeSchema', only = ['name'])
    bookings = fields.List(fields.Nested('BookingSchema', exclude = ['pet']))

    name = fields.String(required=True, validate=Length(min=2))

    @validates('client_id')
    def client(self, client_id):
        #get the client object from the request to check if they exist
        client_stmt = db.select(Client).filter_by(id=client_id)
        client = db.session.scalar(client_stmt)

        if not client:
            raise ValidationError('Client id does not exist')

    @validates('type_id')
    def type(self, type_id):
        #get the pettype object from the request to check if they exist
        type_stmt = db.select(PetType).filter_by(id=type_id)
        type = db.session.scalar(type_stmt)

        if not type:
            raise ValidationError('Type id does not exist')

    @validates('size_id')
    def size(self, size_id):
        #get the size object from the request to check if they exist
        size_stmt = db.select(Size).filter_by(id=size_id)
        size = db.session.scalar(size_stmt)

        if not size:
            raise ValidationError('Size id does not exist')

    class Meta:
        fields = ('id', 'name', 'breed', 'year', 'type', 'size', 'client', 'bookings', 'type_id', 'size_id', 'client_id')
        ordered = True