from init import db, ma
from models.pet import Pet
from models.employee import Employee
from models.service import Service
from datetime import datetime, date as dt
from marshmallow import fields, validates
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES = ['Pending', 'In-progress', 'Completed']

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='SET NULL'))
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

    @validates('pet_id')
    def validate_pet(self, pet_id):
        #get the employee object from the request to check if they exist
        pet_stmt = db.select(Pet).filter_by(id=pet_id)
        pet = db.session.scalar(pet_stmt)

        if not pet:
            raise ValidationError('Pet does not exist')

    @validates('employee_id')
    def validate_employee(self, employee_id):
        #get the employee object from the request to check if they exist
        employee_stmt = db.select(Employee).filter_by(id=employee_id)
        employee = db.session.scalar(employee_stmt)

        if not employee:
            raise ValidationError('Employee does not exist')

    @validates('service_id')
    def validate_service(self, service_id):
        #get the service object from the request to check if it exists
        service_stmt = db.select(Service).filter_by(id=service_id)
        service = db.session.scalar(service_stmt)

        if not service:
            raise ValidationError('Service does not exist')


    class Meta:
        fields = ('id', 'pet_id', 'service_id', 'status', 'service', 'date', 'time',
        'pet', 'employee_id', 'employee', 'date_created')
        ordered = True

#validate date and time when updating existing booking
def validate_date_time(input_data):
    #convert booking date and time from request, opening and closing time to python date and time object
    #catch ValueError if input is invalid
    try:
        time_obj = datetime.strptime(input_data.get('time'), '%H:%M').time()
        date_obj = datetime.strptime(input_data.get('date'), '%Y-%m-%d').date()
    except ValueError:
        return {'message': "Input date and time must be in 'YYYY-MM-DD' and 'HH:MM' format"}

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

