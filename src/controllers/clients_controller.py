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

#Route to get one pet's info
@clients_bp.route('/<int:client_id>/')
def get_one_client(client_id):
    #get one pet whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    pet = db.session.scalar(stmt)
    # check if the pet exists, if they do, return the ClientSchema
    if pet:
        return ClientSchema().dump(pet)
    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {client_id}'}, 404


#Route to create new pet
@clients_bp.route('/', methods = ['POST'])
def create_client():
    #load info from the request to ClientSchema to apply validation methods
    data = ClientSchema().load(request.json)
    #create a new pet instance from the provided data
    #l_name and email are optional so use request.json.get
    #to avoid crashing the program
    pet = Client(
        f_name = data['f_name'],
        l_name = request.json.get('l_name'), 
        phone = data['phone'],
        email = request.json.get('email') 
    )
    #add pet to the database if no conflicts, and catch IntegrityError if phone number already exists in databse
    try:
        db.session.add(pet)
        db.session.commit()
        #respond to the user
        return ClientSchema().dump(pet), 201
    except IntegrityError:
        return {'error': 'Phone number already exists'}, 409 

#Route to delete a pet
@clients_bp.route('/<int:client_id>/', methods = ['DELETE'])
def delete_client(client_id):
    #get one pet whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    pet = db.session.scalar(stmt)
    # check if the pet exists, if they do, delete them from the database
    if pet:
        db.session.delete(pet)
        db.session.commit()
        return {'message': 'Client deleted successfully'}
    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {client_id}'}, 404

#Route to update pet's info
@clients_bp.route('/<int:client_id>/', methods = ['PUT', 'PATCH'])
def update_client(client_id):
    #get one pet whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    pet = db.session.scalar(stmt)
    # check if the pet exists, if they do, update their info
    if pet:
        pet.f_name = request.json.get('f_name') or pet.f_name
        pet.l_name = request.json.get('l_name') or pet.l_name
        pet.phone = request.json.get('phone') or pet.phone
        pet.email = request.json.get('email') or pet.email
        db.session.commit()
        return ClientSchema().dump(pet)
    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {client_id}'}, 404