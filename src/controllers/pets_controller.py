from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.pet import Pet, PetSchema
from models.client import Client, ClientSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize_employee, authorize_employee_or_pet_owner, authorize_employee_or_account_owner_search


pets_bp = Blueprint('Pets', __name__, url_prefix = '/pets')

#Route to return all pets
@pets_bp.route('/')
@jwt_required()
def get_all_pets():
    #verify that the user is an employee
    authorize_employee()

    #get all records of the Pet model
    stmt = db.select(Pet)
    pets = db.session.scalars(stmt)
    return PetSchema(many=True).dump(pets)

#Route to get one pet's info using pet's id
@pets_bp.route('/<int:pet_id>/')
@jwt_required()
def get_one_pet(pet_id):
    #verify the user is pet's owner or employee
    authorize_employee_or_pet_owner(pet_id)

    #get one pet whose id matches API endpoint
    stmt = db.select(Pet).filter_by(id = pet_id)
    pet = db.session.scalar(stmt)
    # check if the pet exists, if they do, return the PetSchema
    if pet:
        return PetSchema().dump(pet)
    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {pet_id}'}, 404

#Route to get one pet's info using client's phone
@pets_bp.route('/search/')
@jwt_required()
def search_pet():
    args = request.args

    #verify that the user is an employee or account owner
    authorize_employee_or_account_owner_search(args)

    #get the user associated with the provided phone number
    stmt = db.select(User).filter_by(phone = args.get('phone'))
    user = db.session.scalar(stmt)

    #get the id from the user, and use it to get the client
    client_stmt = db.select(Client).filter_by(id = user.id)
    client = db.session.scalar(client_stmt)

    # check if the pet exists, if they do, return the PetSchema
    if client:
        return ClientSchema(only=['pets']).dumps(client)
    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': 'Cannot find pet with the provided phone number'}, 404


#Route to create new pet
@pets_bp.route('/', methods = ['POST'])
@jwt_required()
def create_pet():
    #load info from the request to PetSchema to apply validation methods
    data = PetSchema().load(request.json)

    #get the user object from the token
    user_stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(user_stmt)

    #an employee can add any pets to the system but a client can only add pets
    #to their own client_id
    if user.type_id == 2 or data['client_id'] == user.id:
    
        #create a new pet instance from the provided data
        #breed is optional so use request.json.get
        #to avoid crashing the program
        pet = Pet(
            name = data['name'].capitalize(),
            breed = request.json.get('breed'), 
            client_id = data['client_id'],
            year = data['year'],
            size_id = data['size_id'],
            type_id = data['type_id']
        )
        try:
            #add pet to the database if no conflicts
            db.session.add(pet)
            db.session.commit()

            #respond to the user
            return PetSchema().dump(pet), 201

        #catch IntegrityError if the same pet name already exists with the same client's number
        except IntegrityError:
            return {'message': 'The combination of pet\'s name, client\'s id and pet type already exists'}

    #if the user try to create a pet with client_id other than their own
    #return error message
    elif user.type_id != 2 and data['client_id'] != user.id:
        return {'message': f'Client_id must be {user.id}'}, 401

#Route to delete a pet
@pets_bp.route('/<int:pet_id>/', methods = ['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    #verify the user is pet's owner or employee
    authorize_employee_or_pet_owner(pet_id)

    #get one pet whose id matches API endpoint
    stmt = db.select(Pet).filter_by(id = pet_id)
    pet = db.session.scalar(stmt)

    # check if the pet exists, if they do, delete them from the database
    if pet:
        db.session.delete(pet)
        db.session.commit()
        return {'message': 'Pet deleted successfully'}

    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {pet_id}'}, 404

#Route to update pet's info
@pets_bp.route('/<int:pet_id>/', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_pet(pet_id):
    #verify the user is pet's owner or employee
    authorize_employee_or_pet_owner(pet_id)

    #load request onto PetSchema to apply validations
    data = PetSchema().load(request.json)

    #get one pet whose id matches API endpoint
    stmt = db.select(Pet).filter_by(id = pet_id)
    pet = db.session.scalar(stmt)

    # check if the pet exists, if they do, update their info
    if pet:
        try:
            #get the info from the request, if not provided, keep as it is
            pet.name = data.get('name', pet.name).capitalize()
            pet.client_id = data.get('client_id', pet.client_id)
            pet.breed = data.get('breed', pet.breed).capitalize()
            pet.year = data.get('year', pet.year)
            pet.size_id = data.get('size_id', pet.size_id)
            pet.type_id = data.get('type_id', pet.type_id)
            
            #only an employee can change client_id info for a pet
            if request.json.get('client_id'):

                #get the user object using user_id from jwt token
                user_stmt = db.select(User).filter_by(id=get_jwt_identity())
                user = db.session.scalar(user_stmt)

                #if the user is an employee, update client_id
                if user.type_id == 2:
                    pet.client_id = request.json.get('client_id')

                #if the user is not an employee, return a message
                else:
                    return {'message': 'Only an employee can change client_id'}, 401
            
            #if client_id is not included in the request, keep as it is
            else:
                pet.client_id = pet.client_id
                
            db.session.commit() #commit the changes
            return PetSchema().dump(pet)
        #catch IntegrityError when the updated info already exist in the database
        except IntegrityError:
            return {'message': 'The combination of pet\'s name, client\'s id and pet type already exists'}

    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {pet_id}'}, 404

    