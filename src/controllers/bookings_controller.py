from flask import Blueprint, request, abort, json
from init import db
from datetime import datetime, date as dt
from sqlalchemy.exc import IntegrityError
from models.booking import Booking, BookingSchema, validate_date_time, validate_date, validate_time
from models.user import User
from models.pet import Pet
from models.client import Client, ClientSchema
from controllers.auth_controller import authorize_employee, authorize_employee_or_owner_booking, verify_pet_belongs_to_user_or_employee
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

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
    #verify that user is an employee or owner of the pet
    verify_pet_belongs_to_user_or_employee(request.json['pet_id'])

    # #load request on to BookingSchema to apply validations
    data = BookingSchema().load(request.json, partial=True)

    #validate booking date and time have not passed
    validate_date_time(data)
    
    #retrieve pet_id from data to check if it exists
    pet_stmt = db.select(Pet).filter_by(id = data['pet_id'])
    pet = db.session.scalar(pet_stmt)

    #create a new booking instance from the provided data
    #if the pet_id exist and the user is employee, they can make bookings for any pets
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

    #get one booking whose id matches API endpoint
    stmt = db.select(Booking).filter_by(id = booking_id)
    booking = db.session.scalar(stmt)
    
    data = request.json

    #load status from the request to the Schema for validation
    BookingSchema().load(request.json)

    # check if the booking exists, if it does, update its info
    if booking:
        try:
            #validate input if provided in the request (not having this will cause TypeError)
            if data.get('date'):
                validate_date(data.get('date'))
            if data.get('time'):
                validate_time(data.get('time'))

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
            return {'message': 'The combination of pet\'s id, date and time already exists, or invalid pet and/or service id'}

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

    #get the client from the user
    client_stmt = db.select(Client).filter_by(id=user.id)
    client = db.session.scalar(client_stmt)

    if client and (user_id == client.id or token_user.type_id == 2):
        return ClientSchema().dump(client)
    elif not client:
        return {'message': 'Phone number not found'}, 404
    elif user_id != client.id or token_user.type_id != 2:
        abort(401)
    