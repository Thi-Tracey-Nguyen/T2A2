from init import db, ma
from datetime import datetime, date as dt
from marshmallow import fields, validates, validates_schema
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES = ['Pending', 'In-progress', 'Completed']

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String, default = VALID_STATUSES[0])
    date_created = db.Column(db.Date, default = datetime.now(), nullable=False)
   
    __table_args__ = (db.UniqueConstraint('pet_id', 'date', 'time'),)

    pet = db.relationship('Pet', back_populates = 'bookings')
    employee = db.relationship('Employee')
    service = db.relationship('Service', back_populates = 'bookings')

class BookingSchema(ma.Schema):
    pet = fields.Nested('PetSchema', exclude = ['bookings'])
    service = fields.Nested('ServiceSchema', exclude = ['id', 'bookings'])
    employee = fields.Nested('EmployeeSchema', only = ['user'])
    status = fields.String(validate = OneOf(VALID_STATUSES))

    #validate booking date is in the future
    @validates('date')
    def validate_date(self, date):
        #convert booking date to python date object
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        
        #raise ValidationError if booking date already passed
        #booking can be made for the same date though
        if date_obj < dt.today():
            raise ValidationError('Booking date must be in the future')

    @validates_schema
    def validate_time(self, data, **kwargs):
        #convert booking date and time from request, opening and closing time to python date and time object
        time_obj = datetime.strptime(data['time'], '%H:%M').time()
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        open = datetime.strptime('10:00', '%H:%M').time()
        close = datetime.strptime('20:00', '%H:%M').time()


        #raise ValidationError if booking date already passed
        if date_obj < dt.today():
            raise ValidationError('Booking date must be in the future')

        #if booking is made for the same date,
        #booking time must be in the future
        if date_obj == dt.today():
            if time_obj < datetime.now().time():
                raise ValidationError('Booking time must be in the future')

        #raise ValidationError if booking time is outside opening hours
        if time_obj < open or time_obj > close:
            raise ValidationError('Booking must be from 10am to 8pm')

    class Meta:
        fields = ('id', 'pet_id', 'service_id', 'status', 'service', 'date', 'time',
        'pet', 'employee', 'date_created')
        ordered = True