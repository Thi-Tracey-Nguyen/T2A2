from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.booking import Booking, BookingSchema
from models.employee import Employee
from models.pet import Pet
from flask_jwt_extended import jwt_required


bookings_bp = Blueprint('Bookings', __name__, url_prefix = '/bookings')

#Route to return all bookings
@bookings_bp.route('/')
def get_all_bookings():
    #get all records of the Booking model
    stmt = db.select(Booking).order_by(Booking.date)
    bookings = db.session.scalars(stmt)
    return BookingSchema(many=True).dump(bookings)

#Route to get one booking by id
@bookings_bp.route('/<int:booking_id>/')
def get_one_booking(booking_id):
    #get one booking whose id matches API endpoint
    stmt = db.select(Booking).filter_by(id = booking_id)
    booking = db.session.scalar(stmt)
    # check if the booking exists, if they do, return the BookingSchema
    if booking:
        return BookingSchema().dump(booking)
    #if booking with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find booking with id {booking_id}'}, 404

#Route to get bookings by status
@bookings_bp.route('/<status>/')
def get_booking_by_status(status):
    #get all bookings whose status matches API endpoint
    stmt = db.select(Booking).filter_by(status=status.capitalize())
    bookings = db.session.scalars(stmt)

    # respond to the user
    return BookingSchema(many=True).dump(bookings)
    # #if booking with the provided id does not exist, return an error message
    # else:
    #     return {'message': f'Cannot find booking with id {booking_id}'}, 404

#Route to create new booking
@bookings_bp.route('/', methods = ['POST'])
def create_booking():
    #get data from the request
    data = request.json

    #retrieve pet_id from data to check if it exists
    pet_stmt = db.select(Pet).filter_by(id = data['pet_id'])
    pet = db.session.scalar(pet_stmt)

    #retrieve employee_id from data to check if they exist
    employee_stmt = db.select(Employee).filter_by(id = data['employee_id'])
    employee = db.session.scalar(employee_stmt)

    #create a new booking instance from the provided data
    #if the pet and employee exist
    if pet and employee:
        booking = Booking(
            pet_id = data['pet_id'],
            employee_id = data['employee_id'],
            date = data['date'],
            time = data['time'],
            service_id = data['service_id'],
            status = request.json.get('status') #optional field -> use .get()
        )
        try:
            #add the booking and commit if no conflicts
            db.session.add(booking)
            db.session.commit()
            return BookingSchema().dump(booking)

        #catch IntegrityError if the combination of
        #pet_id, date and time already exists
        except IntegrityError:
            return {'message':
            'The combination of pet\'s id, date and time already exists'}
    elif not pet:
        return {'message': 'Pet\'s id does not exist'}, 404
    elif not employee:
        return {'message': 'Employee\'s id does not exist'}, 404

#Route to delete a booking
@bookings_bp.route('/<int:booking_id>/', methods = ['DELETE'])
def delete_booking(booking_id):
    #get one booking whose id matches API endpoint
    stmt = db.select(Booking).filter_by(id = booking_id)
    booking = db.session.scalar(stmt)
    # check if the booking exists, if they do, delete them from the database
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return {'message': 'Booking deleted successfully'}
    #if booking with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find booking with id {booking_id}'}, 404

#Route to update booking's info
@bookings_bp.route('/<int:booking_id>/', methods = ['PUT', 'PATCH'])
def update_booking(booking_id):
    #get one booking whose id matches API endpoint
    stmt = db.select(Booking).filter_by(id = booking_id)
    booking = db.session.scalar(stmt)
    
    # check if the booking exists, if it does, update its info
    if booking:
        try:
            #load the request into BookingSchema to apply validations
            data = BookingSchema().load(request.json)
            #get the info from the request, if not provided, keep as it is
            booking.service_id = data.get('service_id') or booking.service_id
            booking.pet_id = data.get('pet_id') or booking.pet_id
            booking.employee_id = data.get('employee_id') or booking.employee_id
            booking.date = data.get('date') or booking.date
            booking.time = data.get('time') or booking.time
            booking.status = data.get('status') or booking.status
            db.session.commit() #commit the changes
            return BookingSchema().dump(booking)
        #catch IntegrityError when the updated info already exist in the database
        except IntegrityError:
            return {'message': 'The combination of pet\'s id, date and time already exists'}

    #if booking with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find booking with id {booking_id}'}, 404