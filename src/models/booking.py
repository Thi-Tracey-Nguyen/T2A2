from init import db, ma
from datetime import datetime
from marshmallow import fields

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, default = 'Pending', nullable=False)
    date_created = db.Column(db.Date, default = datetime.now(), nullable=False)
   
    

    pet = db.relationship('Pet', back_populates = 'bookings')
    employee = db.relationship('Employee')
    service = db.relationship('Service', back_populates = 'bookings')

class BookingSchema(ma.Schema):
    pet = fields.Nested('PetSchema', exclude = ['bookings'])
    service = fields.Nested('ServiceSchema', exclude = ['id', 'bookings'])
    employee = fields.Nested('EmployeeSchema', only = ['user'])

    class Meta:
        fields = ('id', 'service', 'date', 'time', 'pet', 'employee', 'date_created')
        ordered = True