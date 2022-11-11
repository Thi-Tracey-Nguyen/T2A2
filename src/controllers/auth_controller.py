from flask import Blueprint, request, abort
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from models.employee import Employee
from models.user import User, UserSchema
from models.client import Client, ClientSchema
from models.booking import Booking
from models.pet import Pet
from datetime import timedelta
from marshmallow import EXCLUDE
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

#route for online registration of a client
@auth_bp.route('/register/', methods=['POST'])
def auth_register_client():
    #create a user with provided info first
    #load info from the request to UserSchema and ClientSchema to apply validation methods
    data = request.json
    UserSchema(unknown=EXCLUDE).load(data)
    ClientSchema(unknown=EXCLUDE).load(data)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
        personal_email = data['personal_email'],
        type_id = 1 #type_id for client
    )
    #add user to the database if no conflicts
    try:
        db.session.add(user)
        db.session.commit()

        #retrieve the new user's id with the provided phone number because it is unique
        stmt = db.select(User).filter_by(phone = data['phone'])
        user = db.session.scalar(stmt)

        #create a new client instance with the user.id from the new user
        new_client = Client(
            id = user.id,
            password = bcrypt.generate_password_hash(data['password']).decode('utf8')
        )

        #add the new client to the database and commit
        db.session.add(new_client)
        db.session.commit()

        #respond to the user
        return ClientSchema(exclude = ['pets', 'password']).dump(new_client), 201

    #catch IntegrityError when phone number already exists
    except IntegrityError:
        return {'message': 'Phone number already exists'}, 409
    

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    #A user can be client or employee
    #checks if they are a client 
    user_stmt = db.select(User).filter_by(personal_email = request.json['email'])
    user = db.session.scalar(user_stmt)

    #check if they are an employee
    employee_stmt = db.select(Employee).filter_by(email = request.json['email'])
    employee = db.session.scalar(employee_stmt)

    #if the user or employee exists and password matches the hash
    if employee and bcrypt.check_password_hash(employee.password, request.json['password']):
        # generate token
        token = create_access_token(identity=employee.id, expires_delta=timedelta(days=1))

        return {'email': employee.email, 'token': token, 'is_admin': employee.is_admin}
    
    elif user:
        client_stmt = db.select(Client).filter_by(id = user.id)
        client = db.session.scalar(client_stmt)

        if bcrypt.check_password_hash(client.password, request.json['password']):
            # generate token
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'email': user.personal_email, 'token': token, 'is_admin': 'false'}
        else:
            return {"error": "Invalid email or password"}, 401 #401 Unauthorized
    else:
        return {"error": "Invalid email or password"}, 401 #401 Unauthorized


def authorize_admin():
    #extract the employee identity from the token
    employee_id = get_jwt_identity() 

    #retrieve the employee from the id
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)

    #if the employee is not admin, abort with 401 error
    if not employee.is_admin:
        abort(401)

def authorize_employee():
    #extract the user identity from the token
    user_id = get_jwt_identity()

    #get the employee from the id
    stmt = db.select(Employee).filter_by(id = user_id)
    employee = db.session.scalar(stmt)

    #if the employee with such id does not exist, abort with 401 error
    if not employee:
        abort(401)

#this function is used when accessing and editing client's info
def authorize_employee_or_account_owner(args):
    #extract the user identity from the token
    user_id = get_jwt_identity()

    #get user from the token (to access type_id later)
    token_stmt = db.select(User).filter_by(id = user_id)
    token_user = db.session.scalar(token_stmt)

    #get the user from the provided id
    stmt = db.select(User).where(db.and_(User.type_id == 1), db.or_(User.id == args.get('id'), 
    (User.phone == args.get('phone'))))
    user = db.session.scalar(stmt)

    #if the id from the token does not match looked up id,
    #or the user is not an employee, abort with 401 error
    try:
        if not user.id == user_id and not token_user.type_id == 2:
            abort(401)
    except AttributeError:
        return {'message': 'Cannot find client with provided info'}, 404

#this function is used when accessing and editing an employee's info
def authorize_admin_or_account_owner(args):
    #extract the user identity from the token
    user_id = get_jwt_identity()

    #get employee from the token
    token_stmt = db.select(Employee).filter_by(id = user_id)
    token_user = db.session.scalar(token_stmt)

    #get the user from the provided id
    stmt = db.select(User).where(db.or_(User.id == args.get('id'), (User.phone == args.get('phone'))))
    user = db.session.scalar(stmt)

    #if the id from the token does not match looked up id,
    #if the user is not employee, token_user is None
    #or the user is not an admin, abort with 401 error
    try:
        if  not token_user or (not user.id == user_id and token_user.is_admin is False):
                abort(401)
    except AttributeError:
        return {'message': 'Cannot find employee with provided info'}, 404

#verify that the user is an employee or booking's owner
def authorize_employee_or_owner_booking(booking_id):
    #get user_id from jwt token
    user_id = get_jwt_identity()

    #get type_id from the user to check if they are an employee
    user_stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(user_stmt)

    #get pet_id from the booking_id
    booking_stmt = db.select(Booking).filter_by(id=booking_id)
    booking = db.session.scalar(booking_stmt)

    #if booking_id exists
    if booking:
        #get client_id from pet_id
        pet_stmt = db.select(Pet).filter_by(id=booking.pet_id)
        pet = db.session.scalar(pet_stmt)

        #checks if the user_id from token matches client_id from pet
        if user_id != pet.client_id and user.type_id != 2:
            abort(401)

def verify_pet_belongs_to_user_or_employee(pet_id):
    #get user_id from token
    user_id = get_jwt_identity()

    #get the user to access type_id
    user_stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(user_stmt)

    #get the pet whose id matches input and client_id matches user_id from token
    pet_stmt = db.select(Pet).where(db.and_(Pet.id==pet_id), (Pet.client_id==user_id))
    pet = db.session.scalar(pet_stmt)

    #if the pet does not exist and user is not employee abort with 401 response
    if not pet and user.type_id != 2:
        abort(401)
