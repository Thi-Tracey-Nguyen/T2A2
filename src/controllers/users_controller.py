from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required


users_bp = Blueprint('Users', __name__, url_prefix = '/users')

#Route to return all users
@users_bp.route('/')
def get_all_users():
    #get all records of the User model
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude = ['client', 'staff']).dump(users)

#Route to get one user's info by user_id
@users_bp.route('/<int:user_id>/')
def get_one_user(user_id):
    #get one user whose id matches API endpoint
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    # check if the user exists, if they do, return the UserSchema
    if user:
        return UserSchema(exclude = ['client', 'staff']).dump(user)
    #if user with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user with id {user_id}'}, 404

#Route to get one user's info by unique phone number
@users_bp.route('/phone/<phone>/')
def get_one_user_by_phone(phone):
    #get one user whose phone number matches API endpoint
    stmt = db.select(User).filter_by(phone = phone)
    user = db.session.scalar(stmt)
    # check if the user exists, if they do, return the UserSchema
    if user:
        return UserSchema(exclude = ['client', 'staff']).dump(user)
    #if user with the provided phone number does not exist, return an error message
    else:
        return {'message': 'Cannot find user with the associated phone number'}, 404


#Route to create new user
@users_bp.route('/', methods = ['POST'])
def create_user():
    #create a user with provided info first
    #load info from the request to UserSchema to apply validation methods
    data = UserSchema().load(request.json)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
    )
    #add user to the database if no conflicts
    try:
        db.session.add(user)
        db.session.commit()

        #respond to the user
        return UserSchema(exclude = ['client', 'staff']).dump(user), 201

    #catch IntegrityError when phone number already exists
    except IntegrityError:
        return {'message': 'Phone number already exists'}, 409
    

#Route to delete a user
@users_bp.route('/<int:user_id>/', methods = ['DELETE'])
def delete_user(user_id):
    #get one user whose id matches API endpoint
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    # check if the user exists, if they do, delete them from the users table
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}
    #if user with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user with id {user_id}'}, 404

#Route to update user's info
@users_bp.route('/<int:user_id>/', methods = ['PUT', 'PATCH'])
def update_user(user_id):
    #get one user whose id matches API endpoint
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    # check if the user exists, if they do, update their info
    if user:
        #load the request into the UserSchema to use validations
        data = UserSchema().load(request.json, partial = True)

        #update client's info if no confilcts (duplicate phone numbers)
        try:
            #assign user's attributes with provided values 
            #or keep as it is if not provided
            user.f_name = data.get('f_name') or user.f_name
            user.l_name = data.get('l_name') or user.l_name
            user.phone = data.get('phone') or user.phone

            #commit the changes and response to the user
            db.session.commit()
            return UserSchema(exclude = ['client', 'staff']).dump(user)

        #catch IntegrityError when updated phone number already exists
        except IntegrityError:
            return {'message': 'Phone number already exists'}

    #if user with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user with id {user_id}'}, 404