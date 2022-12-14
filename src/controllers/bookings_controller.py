from flask import Blueprint, request, abort
from init import db
from sqlalchemy.exc import IntegrityError
from models.booking import Booking, BookingSchema, validate_date_time
from models.user import User
from models.pet import Pet
from models.client import Client, ClientSchema
from models.employee import Employee
from models.service import Service
from controllers.auth_controller import authorize_employee, authorize_employee_or_owner_booking
from flask_jwt_extended import jwt_required, get_jwt_identity


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
@jwt_required()
def get_one_booking(booking_id):
    #verify that the user is an employee or owner of the booking
    authorize_employee_or_owner_booking(booking_id)

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
@jwt_required()
def get_booking_by_status(status):
    #verify that the user is an employee
    authorize_employee()

    #get all bookings whose status matches API endpoint
    stmt = db.select(Booking).filter_by(status=status.capitalize())
    bookings = db.session.scalars(stmt)

    # respond to the user
    return BookingSchema(many=True).dump(bookings)
    
#Route to create new booking
@bookings_bp.route('/', methods = ['POST'])
@jwt_required()
def create_booking():
    # #load request on to BookingSchema to apply validations
    data = BookingSchema().load(request.json, partial=True)

    #validate booking date and time have not passed
    validate_date_time(data)

    #get the user object from the token id
    user_stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(user_stmt)

    #retrieve pet_id from data to check if it exists
    pet_stmt = db.select(Pet).filter_by(id = data['pet_id'])
    pet = db.session.scalar(pet_stmt)

    #create a new booking instance from the provided data
    #ifthe user is employee or the user is the owner of the pet, a booking can be made
    if pet.client_id == get_jwt_identity() or user.type_id == 2:
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

        #catch IntegrityError if the combination of pet_id, date and time already exists
        except IntegrityError:
            return {'message':
            'The combination of pet\'s id, date and time already exists'}
  
    #if the pet's owner is not the user or user is not an employee, abort 401 with a message
    elif pet.client_id != get_jwt_identity() and user.type_id != 2:
        return {'message': f"You are not the owner of pet id {data.get('pet_id')}"}, 401


#Route to delete a booking
@bookings_bp.route('/<int:booking_id>/', methods = ['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    #verify that the user is an employee or owner of the booking
    authorize_employee_or_owner_booking(booking_id)

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
    #verify that the user is an employee or owner of the booking
    authorize_employee_or_owner_booking(booking_id)

    #get the user object from the token to check if they are an employee
    user_stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(user_stmt)

    #get one booking whose id matches API endpoint
    stmt = db.select(Booking).filter_by(id = booking_id)
    booking = db.session.scalar(stmt)
    
    #load status from the request to the Schema for validation
    data = BookingSchema().load(request.json)

    # check if the booking exists, if it does, update its info
    if booking:
        try:
            #validate booking date and time are in the future if they are provided in the request
            if data.get('date') or data.get('time'): 
                validate_date_time(data)

            #get the info from the request, if not provided, keep as it is
            booking.service_id = data.get('service_id', booking.service_id)
            booking.employee_id = data.get('employee_id', booking.employee_id)
            booking.date = data.get('date', booking.date)
            booking.time = data.get('time', booking.time)
            booking.status = data.get('status', booking.status)

            #if the user wants to change pet_id in a booking
            #only an employee can do so
            if data.get('pet_id') and user.type_id == 2:
                booking.pet_id = data.get('pet_id')

            #if the user is not an employee: send a message with 401 response
            elif data.get('pet_id') and user.type_id != 2:
                return {'message': 'Only employee can edit pet_id in a booking'}, 401

            #if pet_id is not in the request, keep as it is
            elif not data.get('pet_id'):
                booking.pet_id = booking.pet_id


            db.session.commit() #commit the changes
            return BookingSchema().dump(booking)
        #catch IntegrityError when the updated info already exist in the database
        except IntegrityError:
            return {'message': 'The combination of pet\'s id, date and time already exists'}

    #if booking with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find booking with id {booking_id}'}, 404

#search booking with client's phone
@bookings_bp.route('/search/')
@jwt_required()
def search_booking():
    args = request.args
    user_id = get_jwt_identity()

    #get the user from user_id to access type_id
    token_user_stmt = db.select(User).filter_by(id=user_id)
    token_user = db.session.scalar(token_user_stmt)

    #get the user from the phone number because phone is stored in users table
    user_stmt = db.select(User).filter_by(phone = args['phone'])
    user = db.session.scalar(user_stmt)

    #if the user exist, means phone number exist in the database
    if user:
        #get the client from the user
        client_stmt = db.select(Client).filter_by(id=user.id)
        client = db.session.scalar(client_stmt)

        #if the client from phone number matches the user id, 
        #or if the user is an employee, return ClientSchema, where booking info is nested
        if user_id == client.id or token_user.type_id == 2:
            return ClientSchema(exclude=['password']).dump(client)

        #if the client from the phone number does not match the user's id
        #and the user is not an employee abort 401
        elif user_id != client.id and token_user.type_id != 2:
            abort(401)
    #if no user can be found from the provided phone number, return a message
    else:
        return {'message': 'Phone number not found'}, 404
    
    