from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.pet import Pet, PetSchema
from flask_jwt_extended import jwt_required


pets_bp = Blueprint('Pets', __name__, url_prefix = '/pets')

#Route to return all pets
@pets_bp.route('/')
def get_all_pets():
    #get all records of the Pet model
    stmt = db.select(Pet)
    pets = db.session.scalars(stmt)
    return PetSchema(many=True).dump(pets)

# #Route to get one pet's info
# @pets_bp.route('/<int:pet_id>/')
# def get_one_pet(pet_id):
#     #get one pet whose id matches API endpoint
#     stmt = db.select(Pet).filter_by(id = pet_id)
#     pet = db.session.scalar(stmt)
#     # check if the pet exists, if they do, return the PetSchema
#     if pet:
#         return PetSchema().dump(pet)
#     #if pet with the provided id does not exist, return an error message
#     else:
#         return {'message': f'Cannot find pet with id {pet_id}'}, 404


# #Route to create new pet
# @pets_bp.route('/', methods = ['POST'])
# def create_pet():
#     #load info from the request to PetSchema to apply validation methods
#     data = PetSchema().load(request.json)
#     #create a new pet instance from the provided data
#     #l_name and email are optional so use request.json.get
#     #to avoid crashing the program
#     pet = Pet(
#         name = data['f_name'],
#         breed = request.json.get('breed'), 
#         client_id = data['client_id'],
#         year = data['year'],
#         size_id = data['size_id'], 
#         type_id = data['type_id']
#     )
#     #add pet to the database if no conflicts, and catch IntegrityError 
#     try:    
#         db.session.add(pet)
#         db.session.commit()
#         #respond to the user
#         return PetSchema().dump(pet), 201
#     except IntegrityError:
#         return {'error': 'Phone number already exists'}, 409 

# #Route to delete a pet
# @pets_bp.route('/<int:pet_id>/', methods = ['DELETE'])
# def delete_pet(pet_id):
#     #get one pet whose id matches API endpoint
#     stmt = db.select(Pet).filter_by(id = pet_id)
#     pet = db.session.scalar(stmt)
#     # check if the pet exists, if they do, delete them from the database
#     if pet:
#         db.session.delete(pet)
#         db.session.commit()
#         return {'message': 'Pet deleted successfully'}
#     #if pet with the provided id does not exist, return an error message
#     else:
#         return {'message': f'Cannot find pet with id {pet_id}'}, 404

# #Route to update pet's info
# @pets_bp.route('/<int:pet_id>/', methods = ['PUT', 'PATCH'])
# def update_pet(pet_id):
#     #get one pet whose id matches API endpoint
#     stmt = db.select(Pet).filter_by(id = pet_id)
#     pet = db.session.scalar(stmt)
#     # check if the pet exists, if they do, update their info
#     if pet:
#         pet.name = request.json.get('name') or pet.name
#         pet.client_id = request.json.get('client_id') or pet.client_id
#         pet.breed = request.json.get('breed') or pet.breed
#         pet.year = request.json.get('year') or pet.year
#         pet.size_id = request.json.get('size_id') or pet.size_id
#         pet.type_id = request.json.get('type_id') or pet.type_id
#         db.session.commit()
#         return PetSchema().dump(pet)
#     #if pet with the provided id does not exist, return an error message
#     else:
#         return {'message': f'Cannot find pet with id {pet_id}'}, 404