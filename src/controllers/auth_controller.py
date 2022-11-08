from flask import Blueprint, request, abort
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from models.employee import Employee
from models.user import User, UserSchema
from models.client import Client, ClientSchema
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

#route for online registration of a client
@auth_bp.route('/register/', methods=['POST'])
def auth_register_client():
    #create a user with provided info first
    #load info from the request to UserSchema to apply validation methods
    data = UserSchema().load(request.json)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
        type_id = 1 #type_id for client
    )
    #add user to the database if no conflicts
    try:
        db.session.add(user)
        db.session.commit()

        #retrieve the new user's id with the provided phone number because it is unique
        stmt = db.select(User).filter_by(phone = data['phone'])
        user = db.session.scalar(stmt)

        #create a new client instance with the user.id from the new user
        new_client = Client(
            id = user.id,
            password = bcrypt.generate_password_hash(data['password']).decode('utf8')
        )

        #add the new client to the database and commit
        db.session.add(new_client)
        db.session.commit()

        #respond to the user
        return ClientSchema(exclude = ['pets', 'password']).dump(new_client), 201

    #catch IntegrityError when phone number already exists
    except IntegrityError:
        return {'message': 'Phone number already exists'}, 409
    

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    #A user can be client or employee
    #checks if they are a client 
    user_stmt = db.select(User).filter_by(personal_email = request.json['email'])
    user = db.session.scalar(user_stmt)

    #check if they are an employee
    employee_stmt = db.select(Employee).filter_by(email = request.json['email'])
    employee = db.session.scalar(employee_stmt)

    #if the user or employee exists and password matches the hash
    if employee and bcrypt.check_password_hash(employee.password, request.json['password']):
        # generate token
        token = create_access_token(identity=employee.id, expires_delta=timedelta(days=1))

        return {'email': employee.email, 'token': token, 'is_admin': employee.is_admin}
    
    elif user:
        client_stmt = db.select(Client).filter_by(id = user.id)
        client = db.session.scalar(client_stmt)

        if bcrypt.check_password_hash(client.password, request.json['password']):
            # generate token
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'email': user.personal_email, 'token': token, 'is_admin': 'false'}
        else:
            return {"error": "Invalid email or password"}, 401 #401 Unauthorized
    else:
        return {"error": "Invalid email or password"}, 401 #401 Unauthorized


def authorize_admin():
    #extract the employee identity from the token
    employee_id = get_jwt_identity() 

    #retrieve the employee from the id
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)

    #if the employee is not admin, abort with 401 error
    if not employee.is_admin:
        abort(401)

def authorize_employee():
    #extract the user identity from the token
    user_id = get_jwt_identity()

    #get the employee from the id
    stmt = db.select(Employee).filter_by(id = user_id)
    employee = db.session.scalar(stmt)

    #if the employee with such id does not exist, abort with 401 error
    if not employee:
        abort(401)

#this function is used when accessing and editing client's info
def authorize_employee_or_account_owner(args):
    #extract the user identity from the token
    user_id = get_jwt_identity()

    #get user from the token (to access type_id later)
    token_stmt = db.select(User).filter_by(id = user_id)
    token_user = db.session.scalar(token_stmt)

    #get the user from the provided id
    stmt = db.select(User).where(db.and_(User.type_id == 1), db.or_(User.id == args.get('id'), (User.phone == args.get('phone'))))
    user = db.session.scalar(stmt)


    #if the id from the token does not match looked up id,
    #or the user is not an employee, abort with 401 error
    try:
        if not user.id == user_id and not token_user.type_id == 2:
            abort(401)
    except AttributeError:
        return {'message': 'Cannot find client with provided info'}, 404

#this function is used when accessing and editing an employee's info
def authorize_admin_or_account_owner(args):
    #extract the user identity from the token
    user_id = get_jwt_identity()

    #get employee from the token 
    token_stmt = db.select(Employee).filter_by(id = user_id)
    token_user = db.session.scalar(token_stmt)

    #get the user from the provided id
    stmt = db.select(User).where(db.or_(User.id == args.get('id'), (User.phone == args.get('phone'))))
    user = db.session.scalar(stmt)

    #if the id from the token does not match looked up id,
    #or the user is not an admin, abort with 401 error
    try:
        if  not token_user or (not user.id == user_id and token_user.is_admin is False):
                abort(401)
    except AttributeError:
        return {'message': 'Cannot find employee with provided info'}, 404

