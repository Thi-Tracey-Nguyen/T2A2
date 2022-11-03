from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.client import Client, ClientSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required


clients_bp = Blueprint('Clients', __name__, url_prefix = '/clients')

#Route to return all clients
@clients_bp.route('/')
def get_all_clients():
    #get all records of the Client model
    stmt = db.select(Client)
    clients = db.session.scalars(stmt)
    return ClientSchema(many=True).dump(clients)

#Route to get one client's info
@clients_bp.route('/<int:client_id>/')
def get_one_client(client_id):
    #get one client whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    client = db.session.scalar(stmt)
    # check if the client exists, if they do, return the ClientSchema
    if client:
        return ClientSchema().dump(client)
    #if client with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find client with id {client_id}'}, 404

#Route to get one client's info by unique phone number
@clients_bp.route('/phone/<phone>/')
def get_one_client_by_phone(phone):
    #has to go through users table because it is where phone number is stored
    #get one user whose phone number matches API endpoint
    stmt = db.select(User).filter_by(phone = phone)
    user = db.session.scalar(stmt)

    #retrieve user_id from the user and look it up in the clients table
    client_stmt = db.select(Client).filter_by(user_id = user.id)
    client = db.session.scalar(client_stmt)

    # check if the client exists, if they do, return the ClientSchema
    if client:
        return ClientSchema().dump(client)
    #if client with the provided phone number does not exist, return an error message
    else:
        return {'message': 'Cannot find client associated with the phone number'}, 404


#Route to create new client
@clients_bp.route('/', methods = ['POST'])
def create_client():
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

        #create a new client instance with the user_id from the new user
        new_client = Client(user_id = user.id)

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
def delete_client(client_id):
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

#Route to update client's info
@clients_bp.route('/<int:client_id>/', methods = ['PUT', 'PATCH'])
def update_client(client_id):
    #get one client whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    client = db.session.scalar(stmt)
    # check if the client exists, if they do, update their info
    if client:

        #load the request into the UserSchema to use validations
        data = UserSchema().load(request.json)

        #get the user_id from client id to update corresponding fields in users table
        user_stmt = db.select(User).filter_by(id = client.user_id)
        user = db.session.scalar(user_stmt)

        #update client's info if no confilcts (duplicate phone numbers)
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
        return {'message': f'Cannot find client with id {client_id}'}, 404