from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.pet import Pet, PetSchema
from models.client import Client, ClientSchema
from models.user import User
from flask_jwt_extended import jwt_required


pets_bp = Blueprint('Pets', __name__, url_prefix = '/pets')

#Route to return all pets
@pets_bp.route('/')
def get_all_pets():
    #get all records of the Pet model
    stmt = db.select(Pet)
    pets = db.session.scalars(stmt)
    return PetSchema(many=True).dump(pets)

#Route to get one pet's info using pet's id
@pets_bp.route('/<int:pet_id>/')
def get_one_pet(pet_id):
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
@pets_bp.route('/phone/<phone>/')
def get_one_pet_by_phone(phone):

    #get the user associated with the provided phone number
    stmt = db.select(User).filter_by(phone = phone)
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
def create_pet():
    #load info from the request to PetSchema to apply validation methods
    data = PetSchema().load(request.json)

    #create a new pet instance from the provided data
    #breed is optional so use request.json.get
    #to avoid crashing the program
    pet = Pet(
        name = data['name'].capitalize(),
        breed = request.json.get('breed').capitalize(), 
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
        return PetSchema(exclude = ['size_id', 'type_id']).dump(pet), 201

    #catch IntegrityError if the same pet name already exists with the same client's number
    except IntegrityError:
        return {'message': 'The combination of pet\'s name, client\'s id and pet type already exists'}

#Route to delete a pet
@pets_bp.route('/<int:pet_id>/', methods = ['DELETE'])
def delete_pet(pet_id):

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
def update_pet(pet_id):
    #get one pet whose id matches API endpoint
    stmt = db.select(Pet).filter_by(id = pet_id)
    pet = db.session.scalar(stmt)

    # check if the pet exists, if they do, update their info
    if pet:
        try:
            #get the info from the request, if not provided, keep as it is
            pet.name = request.json.get('name', pet.name).capitalize()
            pet.client_id = request.json.get('client_id', pet.client_id)
            pet.breed = request.json.get('breed', pet.breed).capitalize()
            pet.year = request.json.get('year', pet.year)
            pet.size_id = request.json.get('size_id', pet.size_id)
            pet.type_id = request.json.get('type_id', pet.type_id)
            db.session.commit() #commit the changes
            return PetSchema().dump(pet)
        #catch IntegrityError when the updated info already exist in the database
        except IntegrityError:
            return {'message': 'The combination of pet\'s name, client\'s id and pet type already exists'}

    #if pet with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find pet with id {pet_id}'}, 404