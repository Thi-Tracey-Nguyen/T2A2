from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.client import Client, ClientSchema
from models.user import User, UserSchema
from controllers.auth_controller import authorize_employee, authorize_employee_or_account_owner
from flask_jwt_extended import jwt_required


clients_bp = Blueprint('Clients', __name__, url_prefix = '/clients')

#Route to return all clients
@clients_bp.route('/')
@jwt_required()
def get_all_clients():
    #verify if the user is an employee
    authorize_employee()

    #get all records of the Client model
    stmt = db.select(Client)
    clients = db.session.scalars(stmt)
    return ClientSchema(many=True, exclude=['password']).dump(clients)

#Route to get one client by id
@clients_bp.route('/<int:client_id>/')
def get_one_client(client_id):
    #get one client whose id matches API endpoint
    stmt = db.select(User).filter_by(id = client_id)
    client = db.session.scalar(stmt)
    # check if the client exists, if they do, return the UserSchema
    if client:
        return UserSchema().dump(client)
    #if client with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find client with id {client_id}'}, 404

#Route to get one client's info by phone or id
@clients_bp.route('/search/')
@jwt_required()
def search_client():
    args = request.args
   
    #verify the user is an employee or the owner of the account
    authorize_employee_or_account_owner(args)

    #get one user whose id matches API endpoint
    #user.type_id == 1 to ensure user is a client
    #have to search in the users table because it is where the info is stored
    stmt = db.select(User).where(db.and_(User.type_id==1), db.or_(User.id==args.get('id'), User.phone==args.get('phone')))
    user = db.session.scalar(stmt)

    #if the user exists user the user id to retrieve the client
    try:
        #get the client whose id matches the user id
        client_stmt = db.select(Client).filter_by(id=user.id)
        client = db.session.scalar(client_stmt)

        #respond to the user
        return ClientSchema(exclude = ['password']).dump(client)

    #if user with the provided id does not exist, return an error message
    except AttributeError:
        return {'message': 'Cannot find client with provided info'}, 404


#Route to create new client onsite
@clients_bp.route('/', methods = ['POST'])
@jwt_required()
def create_client():
    #verify the user is an employee
    authorize_employee()

    #create a user with provided info first
    #load info from the request to UserSchema to apply validation methods
    data = UserSchema().load(request.json)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
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
        new_client = Client(id = user.id)

        #add the new client to the database and commit
        db.session.add(new_client)
        db.session.commit()

        #respond to the user
        return ClientSchema(exclude = ['pets']).dump(new_client), 201

    #catch IntegrityError when phone number already exists
    except IntegrityError:
        return {'message': 'Phone number already exists'}, 409
    

#Route to delete a client
@clients_bp.route('/<int:client_id>/', methods = ['DELETE'])
@jwt_required()
def delete_client(client_id):
    #verify the user is an employee
    authorize_employee()

    #get one pet whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    client = db.session.scalar(stmt)
    # check if the client exists, if they do, delete them from the client table
    if client:
        db.session.delete(client)
        db.session.commit()
        return {'message': 'Client deleted successfully'}
    #if client with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find client with id {client_id}'}, 404

#Route to update client's info by client's id or phone
@clients_bp.route('/<int:number>/', methods = ['PUT', 'PATCH'])
def update_client(number):
    #verify that the user is an employee or account owner
    authorize_employee_or_user()

    #get one client whose id matches API endpoint
    #have to search in the users table because it is where the info is stored
    stmt = db.select(User).where(db.and_(User.type_id == 1), db.or_(User.id == int(number), User.phone == number))
    user = db.session.scalar(stmt)

    # check if the user exists, if they do, update their info
    if user:

        #load the request into the UserSchema to use validations
        data = UserSchema().load(request.json)

        #get the id from clients table to update corresponding fields in users table
        user_stmt = db.select(User).filter_by(id = client.id)
        user = db.session.scalar(user_stmt)

        #update client's info if no conflicts (duplicate phone numbers)
        try:
            #assign user's attributes with provided values 
            #or keep as it is if not provided
            user.f_name = data.get('f_name') or user.f_name
            user.l_name = data.get('l_name') or user.l_name
            user.phone = data.get('phone') or user.phone

            #commit the changes and response to the user
            db.session.commit()
            return ClientSchema().dump(client)
        
        #catch IntegrityError when updated phone number already exists
        except IntegrityError:
            return {'message': 'Phone number already exists'}
    #if client with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find client with provided info'}, 404