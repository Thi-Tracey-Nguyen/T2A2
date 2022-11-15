from flask import Blueprint, request
from init import db
from models.user_type import UserType, UserTypeSchema
from controllers.auth_controller import authorize_admin, authorize_employee
from flask_jwt_extended import jwt_required


user_types_bp = Blueprint('UserTypes', __name__, url_prefix = '/user_types')

#Route to return all user_types
@user_types_bp.route('/')
@jwt_required()
def get_all_user_types():
    #verify that the user is an employee
    authorize_employee()

    #get all records of the UserType model
    stmt = db.select(UserType)
    user_types = db.session.scalars(stmt)
    return UserTypeSchema(many=True).dump(user_types)

#Route to get one user_type by id
@user_types_bp.route('/<int:user_type_id>/')
@jwt_required()
def get_one_user_type(user_type_id):
    #verify that the user is an employee
    authorize_employee()

    #get one user_type whose id matches API endpoint
    stmt = db.select(UserType).filter_by(id = user_type_id)
    user_type = db.session.scalar(stmt)
    # check if the user_type exists, if they do, return the UserTypeSchema
    if user_type:
        return UserTypeSchema().dump(user_type)
    #if user_type with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user_type with id {user_type_id}'}, 404

#Route to create new user_type
@user_types_bp.route('/', methods = ['POST'])
@jwt_required()
def create_user_type():
    #verify that the user is an admin
    authorize_admin()

    #load request into UserTypeSChema to apply validation
    data = UserTypeSchema().load(request.json)

    #create new user_type instance
    new_user_type = UserType(
       name = data['name'].capitalize()
    )

    #add new user_type to the database and commit it
    db.session.add(new_user_type)
    db.session.commit()

    #respond to the user
    return UserTypeSchema().dump(new_user_type)

#Route to delete a user_type
@user_types_bp.route('/<int:user_type_id>/', methods = ['DELETE'])
@jwt_required()
def delete_user_type(user_type_id):
    #verify that the user is an admin
    authorize_admin()

    #get one user_type whose id matches API endpoint
    stmt = db.select(UserType).filter_by(id = user_type_id)
    user_type = db.session.scalar(stmt)
    # check if the user_type exists, if they do, delete them from the database
    if user_type:
        db.session.delete(user_type)
        db.session.commit()
        return {'message': 'User type deleted successfully'}
    #if user_type with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user_type with id {user_type_id}'}, 404

#Route to update user_type's info
@user_types_bp.route('/<int:user_type_id>/', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_user_type(user_type_id):
    #verify that the user is an admin
    authorize_admin()

    #get one user_type whose id matches API endpoint
    stmt = db.select(UserType).filter_by(id = user_type_id)
    user_type = db.session.scalar(stmt)
    
    # check if the user_type exists, if it does, update its info
    if user_type:
        #load request into UserTypeSChema to apply validation
        data = UserTypeSchema().load(request.json)

        #get the info from the request, if not provided, keep as it is
        user_type.name = data.get('name', user_type.name).capitalize()

        db.session.commit() #commit the changes
        return UserTypeSchema().dump(user_type)
        
    #if user_type with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user_type with id {user_type_id}'}, 404