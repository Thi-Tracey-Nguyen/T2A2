from flask import Blueprint, request
from init import db
from models.service import Service, ServiceSchema
from controllers.auth_controller import authorize_admin
from flask_jwt_extended import jwt_required


services_bp = Blueprint('Services', __name__, url_prefix = '/services')

#Route to return all services
@services_bp.route('/')
def get_all_services():
    #get all records of the Service model
    stmt = db.select(Service)
    services = db.session.scalars(stmt)
    return ServiceSchema(many=True).dump(services)

#Route to get one service by id
@services_bp.route('/<int:service_id>/')
def get_one_service(service_id):
    #get one service whose id matches API endpoint
    stmt = db.select(Service).filter_by(id = service_id)
    service = db.session.scalar(stmt)
    # check if the service exists, if they do, return the ServiceSchema
    if service:
        return ServiceSchema().dump(service)
    #if service with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find service with id {service_id}'}, 404

#Route to create new service
@services_bp.route('/', methods = ['POST'])
@jwt_required()
def create_service():
    #verify that the user is an admin
    authorize_admin()

    #load request into ServiceSchema to apply validation
    data = ServiceSchema().load(request.json)

    #create new service instance
    new_service = Service(
       name = data['name'].title(),
       duration = data['duration'],
       price = data['price']
    )

    #add new service to the database and commit it
    db.session.add(new_service)
    db.session.commit()

    #respond to the user
    return ServiceSchema().dump(new_service)

#Route to delete a service
@services_bp.route('/<int:service_id>/', methods = ['DELETE'])
@jwt_required()
def delete_service(service_id):
    #verify that the user is an admin
    authorize_admin()

    #get one service whose id matches API endpoint
    stmt = db.select(Service).filter_by(id = service_id)
    service = db.session.scalar(stmt)

    # check if the service exists, if they do, delete them from the database
    if service:
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted successfully'}
    #if service with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find service with id {service_id}'}, 404

#Route to update service's info
@services_bp.route('/<int:service_id>/', methods = ['PUT', 'PATCH'])
def update_service(service_id):
    #get one service whose id matches API endpoint
    stmt = db.select(Service).filter_by(id = service_id)
    service = db.session.scalar(stmt)
    
    # check if the service exists, if it does, update its info
    if service:
        #load request into ServiceSChema to apply validation
        data = ServiceSchema(partial=True).load(request.json)

        #get the info from the request, if not provided, keep as it is
        service.name = data.get('name', service.name).title()
        service.duration = data.get('duration', service.duration)
        service.price = data.get('price', service.price)

        db.session.commit() #commit the changes
        return ServiceSchema().dump(service)
        
    #if service with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find service with id {service_id}'}, 404