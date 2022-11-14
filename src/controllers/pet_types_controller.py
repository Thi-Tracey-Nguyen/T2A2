from flask import Blueprint, request
from init import db
from models.pet_type import PetType, PetTypeSchema
from controllers.auth_controller import authorize_admin
from flask_jwt_extended import jwt_required


pet_types_bp = Blueprint('PetTypes', __name__, url_prefix = '/pet_types')

#Route to return all pet_types
@pet_types_bp.route('/')
def get_all_pet_types():
    #get all records of the PetType model
    stmt = db.select(PetType)
    pet_types = db.session.scalars(stmt)
    return PetTypeSchema(many=True, exclude=['pets']).dump(pet_types)

#Route to get one pet_type by id
@pet_types_bp.route('/<int:pet_type_id>/')
def get_one_pet_type(pet_type_id):
    #get one pet_type whose id matches API endpoint
    stmt = db.select(PetType).filter_by(id = pet_type_id)
    pet_type = db.session.scalar(stmt)
    # check if the pet_type exists, if they do, return the PetTypeSchema
    if pet_type:
        return PetTypeSchema(exclude=['pets']).dump(pet_type)
    #if pet_type with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet_type with id {pet_type_id}'}, 404

#Route to create new pet_type
@pet_types_bp.route('/', methods = ['POST'])
@jwt_required()
def create_pet_type():
    #verify that the user is an admin
    authorize_admin()

    #load request into PetTypeSchema to apply validation
    data = PetTypeSchema().load(request.json)

    #create new pet_type instance
    new_pet_type = PetType(
       name = data['name'].title()
    )

    #add new pet_type to the database and commit it
    db.session.add(new_pet_type)
    db.session.commit()

    #respond to the user
    return PetTypeSchema().dump(new_pet_type)

#Route to delete a pet_type
@pet_types_bp.route('/<int:pet_type_id>/', methods = ['DELETE'])
@jwt_required()
def delete_pet_type(pet_type_id):
    #verify that the user is an admin
    authorize_admin()

    #get one pet_type whose id matches API endpoint
    stmt = db.select(PetType).filter_by(id = pet_type_id)
    pet_type = db.session.scalar(stmt)

    # check if the pet_type exists, if they do, delete them from the database
    if pet_type:
        db.session.delete(pet_type)
        db.session.commit()
        return {'message': 'Pet type deleted successfully'}
    #if pet_type with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet_type with id {pet_type_id}'}, 404

#Route to update pet_type's info
@pet_types_bp.route('/<int:pet_type_id>/', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_pet_type(pet_type_id):
    #verify that the user is an admin
    authorize_admin()

    #get one pet_type whose id matches API endpoint
    stmt = db.select(PetType).filter_by(id = pet_type_id)
    pet_type = db.session.scalar(stmt)
    
    # check if the pet_type exists, if it does, update its info
    if pet_type:
        #load request into PetTypeSChema to apply validation
        data = PetTypeSchema(partial=True).load(request.json)

        #get the info from the request, if not provided, keep as it is
        pet_type.name = data.get('name', pet_type.name).title()

        db.session.commit() #commit the changes
        return PetTypeSchema().dump(pet_type)
        
    #if pet_type with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet_type with id {pet_type_id}'}, 404