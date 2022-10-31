from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.client import Client, ClientSchema
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


#Route to create new client
@clients_bp.route('/', methods = ['POST'])
def create_client():
    #load info from the request to ClientSchema to apply validation methods
    data = ClientSchema().load(request.json)
    #create a new client instance from the provided data
    #l_name and email are optional so use request.json.get
    #to avoid crashing the program
    client = Client(
        f_name = data['f_name'],
        l_name = request.json.get('l_name'), 
        phone = data['phone'],
        email = request.json.get('email') 
    )
    #add client to the database if no conflicts, and catch IntegrityError if phone number already exists in databse
    try:
        db.session.add(client)
        db.session.commit()
        #respond to the user
        return ClientSchema().dump(client), 201
    except IntegrityError:
        return {'error': 'Phone number already exists'}, 409 

#Route to delete a client
@clients_bp.route('/<int:client_id>/', methods = ['DELETE'])
def delete_client(client_id):
    #get one client whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    client = db.session.scalar(stmt)
    # check if the client exists, if they do, delete them from the database
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
        client.f_name = request.json.get('f_name') or client.f_name
        client.l_name = request.json.get('l_name') or client.l_name
        client.phone = request.json.get('phone') or client.phone
        client.email = request.json.get('email') or client.email
        db.session.commit()
        return ClientSchema().dump(client)
    #if client with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find client with id {client_id}'}, 404