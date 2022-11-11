from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.booking import Booking, BookingSchema
from models.user import User
from models.pet import Pet, PetSchema
from controllers.auth_controller import authorize_employee
from flask_jwt_extended import jwt_required


bookings_bp = Blueprint('Bookings', __name__, url_prefix = '/bookings')

#Route to return all bookings
@bookings_bp.route('/')
@jwt_required()
def get_all_bookings():
    #verify that the user is an employee
    authorize_employee()

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
    
#Route to create new booking
@bookings_bp.route('/', methods = ['POST'])
@jwt_required()
def create_booking():
    #verify that the user is an employee
    authorize_employee()

    #load request on to BookingSchema to apply validations
    data = BookingSchema().load(request.json, partial=True)

    #retrieve pet_id from data to check if it exists
    pet_stmt = db.select(Pet).filter_by(id = data['pet_id'])
    pet = db.session.scalar(pet_stmt)

    # #retrieve employee_id from data to check if they exist
    # employee_stmt = db.select(Employee).filter_by(id = data['employee_id'])
    # employee = db.session.scalar(employee_stmt)

    #create a new booking instance from the provided data
    #if the pet and employee exist
    if pet:
        booking = Booking(
            pet_id = data['pet_id'],
            employee_id = data.get('employee_id'),
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

    #respond to the user if pet_id does not exist
    else:
        return {'message': 'Pet\'s id does not exist'}, 404

    # #respond to the user if employee_id does not exist
    # elif not employee:
    #     return {'message': 'Employee\'s id does not exist'}, 404

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
@jwt_required()
def update_booking(booking_id):
    #verify that the user is an employee
    authorize_employee()

    #get one booking whose id matches API endpoint
    stmt = db.select(Booking).filter_by(id = booking_id)
    booking = db.session.scalar(stmt)
    
    # check if the booking exists, if it does, update its info
    if booking:
        try:
            #load the request into BookingSchema to apply validations
            data = BookingSchema().load(request.json, partial=True)
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

#search booking with pet's name and client's phone
#Both have to be correct for it to work
@bookings_bp.route('/search/')
def search_booking():
    args = request.args

    #get the pet from provided info
    pet_stmt = db.select(Pet).filter_by(name = args['name'].capitalize())
    pets = db.session.scalars(pet_stmt) #there may be more than one pet with the same name

    #get the client from the phone number
    client_stmt = db.select(User).filter_by(phone = args['phone'])
    client = db.session.scalar(client_stmt)

    #for each pet, check if the client_id matches client_id from phone number
    for pet in pets:
        if pet.client_id == client.id:
            return PetSchema(only=['client', 'bookings']).dump(pet)

    #if client_id from pet does not match client_id from phone number, returns error
    return {'message': 'Pet name and/or phone number are incorrect'}, 404
    