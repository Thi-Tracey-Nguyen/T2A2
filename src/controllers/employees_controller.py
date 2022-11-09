from flask import Blueprint, request, json
from init import db
from sqlalchemy.exc import IntegrityError
from models.employee import Employee, EmployeeSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize_admin_or_account_owner
from marshmallow import EXCLUDE
from init import bcrypt

employees_bp = Blueprint('Employee', __name__, url_prefix = '/employees')

#Route to return all employee
@employees_bp.route('/')
def get_all_employee():
    #get all records of the Employee model
    stmt = db.select(Employee)
    employees = db.session.scalars(stmt)
    return EmployeeSchema(many=True, exclude=['password', 'bookings']).dump(employees)

#Route to get one employee's info by phone or id
@employees_bp.route('/search/')
@jwt_required()
def search_employee():
    args = request.args
   
    #verify the user is an admin or the owner of the account
    authorize_admin_or_account_owner(args)

    #get one user whose id matches API endpoint
    #user.type_id == 1 to ensure user is a client
    #have to search in the users table because it is where the info is stored
    stmt = db.select(User).where(db.and_(User.type_id==2), db.or_(User.id==args.get('id'), User.phone==args.get('phone')))
    user = db.session.scalar(stmt)

    #if the user exists user the user id to retrieve the client
    try:
        #get the client whose id matches the user id
        employee_stmt = db.select(Employee).filter_by(id=user.id)
        employee = db.session.scalar(employee_stmt)

        #respond to the user
        return EmployeeSchema(exclude = ['password']).dump(employee)

    #if employee with the provided id does not exist, return an error message
    except AttributeError:
        return {'message': 'Cannot find employee with provided info'}, 404


#Route to get one employee's info
@employees_bp.route('/<int:employee_id>/')
def get_one_employee(employee_id):
    #get one employee whose id matches API endpoint
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)
    # check if the employee exists, if they do, return the EmployeeSchema
    if employee:
        return EmployeeSchema(exclude=['password', 'bookings']).dump(employee)
    #if employee with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find employee with id {employee_id}'}, 404


#Route to create new employee
@employees_bp.route('/', methods = ['POST'])
def create_employee():
    # #function to generate random password
    # def auto_password():
    #     password_length = 10
    #     return secrets.token_urlsafe(password_length)
    #create a user with provided info first
    #load info from the request to UserSchema to apply validation methods
    data = UserSchema().load(request.json)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
        type_id = 2 #type_id for employee
    )
    #add user to the database if no conflicts
    try:
        db.session.add(user)
        db.session.commit()

        #retrieve the new user's id with the provided phone number because it is unique
        stmt = db.select(User).filter_by(phone = data['phone'])
        user = db.session.scalar(stmt)

        #create a new employee instance with the id from the new user
        new_employee = Employee(
            id = user.id,
            password = auto_password(),
            email = user.f_name.lower() + '.' + user.l_name.lower() + '@dog_spa.com'
        )

        #add the new employee to the database and commit
        db.session.add(new_employee)
        db.session.commit()

        #respond to the user
        return EmployeeSchema(exclude=['password', 'bookings']).dump(new_employee), 201

    #catch IntegrityError when phone number already exists
    except IntegrityError:
        return {'message': 'Phone number already exists'}, 409
    
#Route to delete a employee
@employees_bp.route('/<int:employee_id>/', methods = ['DELETE'])
def delete_employee(employee_id):
    #get one pet whose id matches API endpoint
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)
    # check if the employee exists, if they do, delete them from the employee table
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return {'message': 'Employee deleted successfully'}
    #if employee with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find employee with id {employee_id}'}, 404

#Route to update employee's info
@employees_bp.route('/<int:employee_id>/', methods = ['PUT', 'PATCH'])
def update_employee(employee_id):
    #get one employee whose id matches API endpoint
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)
    
    # check if the employee exists, if they do, update their info
    if employee:
        #load the request into the UserSchema to use validations
        #exclude unknown fileds which are in EmployeeSchema
        UserSchema().load(request.json, partial=True, unknown=EXCLUDE)

        #get the id to update corresponding fields in users table
        user_stmt = db.select(User).filter_by(id = employee.id)
        user = db.session.scalar(user_stmt)

        #f_name, l_name and phone are in the users table
        #or keep as it is if not provided
        user.f_name = request.json.get('f_name', user.f_name)
        user.l_name = request.json.get('l_name', user.l_name)
        user.phone = request.json.get('phone', user.phone)
        
        #to update password, load request into EmployeeSchema to apply validations
        EmployeeSchema().load(request.json, partial = True, unknown = EXCLUDE)

        #handles password in the request
        # employee.password = bcrypt.generate_password_hash(request.json.get('password', employee.password)).decode('utf8')

        employee.is_admin = json.loads(request.json.get('is_admin', str(employee.is_admin)).lower())

        #commit the changes and response to the user
        db.session.commit()
        return EmployeeSchema(exclude=['password', 'bookings']).dump(employee)
    #if employee with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find employee with id {employee_id}'}, 404