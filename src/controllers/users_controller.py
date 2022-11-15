from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from controllers.auth_controller import authorize_employee
from flask_jwt_extended import jwt_required


users_bp = Blueprint('Users', __name__, url_prefix = '/users')

#Users table is used for management purposes only. Only staff has access to it, and can only read. 
#to create, update and delete clients or employees, use respective routes.

#Route to return all users
@users_bp.route('/')
@jwt_required()
def get_all_users():
    #checks if the user is an employee
    authorize_employee()

    #get all records of the User model
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['employee']).dump(users)

#Route to get one user by id
@users_bp.route('/<int:user_id>/')
@jwt_required()
def get_one_user(user_id):
    #checks if the user is an employee
    authorize_employee()

    #get one user whose id matches API endpoint
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    # check if the user exists, if they do, return the UserSchema
    if user:
        return UserSchema(exclude=['employee']).dump(user)
    #if user with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find user with id {user_id}'}, 404

#Route to get one user's info by phone
@users_bp.route('/search/')
@jwt_required()
def search_user():
    args = request.args

    #checks if the user is an employee
    authorize_employee()

    #get one user whose id matches API endpoint
    stmt = db.select(User).filter_by(phone=args.get('phone'))
    user = db.session.scalar(stmt)

    #respond to the user
    return UserSchema(exclude = ['employee']).dump(user)
