from flask import Blueprint, request
from init import db
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

#Get one client's info
@clients_bp.route('/<int:client_id>/')
def get_one_clients(client_id):
    #get one client whose id matches API endpoint
    stmt = db.select(Client).filter_by(id = client_id)
    client = db.session.scalar(stmt)
    # check if the client exists, if they do, return the ClientSchema
    if client:
        return ClientSchema().dump(client)
    #if client with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find client with id {client_id}'}, 404


#Create new client
@clients_bp.route('/', methods = ['POST'])
def create_client():
    #load info from the request to ClientSchema to apply validation methods
    data = ClientSchema().load(request.json)
    #create a new client instance from the provided data
    client = Client(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
        email = data['email']
    )
    db.session.add(client)
    db.session.commit()
    #respond to the user 
    return ClientSchema().dump(client), 201