from flask import Blueprint, request, json
from init import db
from sqlalchemy.exc import IntegrityError
from models.employee import Employee, EmployeeSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize_admin_or_account_owner_search, authorize_admin, authorize_admin_or_account_owner_id
from marshmallow import EXCLUDE
from init import bcrypt

employees_bp = Blueprint('Employee', __name__, url_prefix = '/employees')

#Route to return all employee
@employees_bp.route('/')
@jwt_required()
def get_all_employee():
    #verify that the user is an admin
    authorize_admin()

    #get all records of the Employee model
    stmt = db.select(Employee)
    employees = db.session.scalars(stmt)
    return EmployeeSchema(many=True, exclude=['password', 'bookings']).dump(employees)

#Route to get one employee's info by phone
@employees_bp.route('/search/')
@jwt_required()
def search_employee():
    args = request.args
   
    #verify the user is an admin or the owner of the account
    authorize_admin_or_account_owner_search(args)

    #get one user whose id matches API endpoint
    #user.type_id == 2 to ensure user is an employee
    #have to search in the users table because it is where the info is stored
    stmt = db.select(User).where(db.and_(User.type_id==2), User.phone==args.get('phone'))
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


#Route to get one employee's info by id
@employees_bp.route('/<int:employee_id>/')
@jwt_required()
def get_one_employee(employee_id):
    #verify the user is an admin or the owner of the account
    authorize_admin_or_account_owner_id(employee_id)

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
@jwt_required()
def create_employee():
    #verify the user is an admin
    authorize_admin()

    # create a user with provided info first
    # load info from the request to UserSchema to apply validation methods
    data = UserSchema().load(request.json)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
        personal_email = data.get('personal_email'),
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
            password = user.f_name[:2] + user.f_name[-2:] + user.l_name[0] + user.l_name[-1] + 'ds123!',
            email = user.f_name.lower() + '.' + user.l_name.lower() + '@dog_spa.com',
            is_admin = data.get('is_admin')
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
@jwt_required()
def delete_employee(employee_id):
    #verify the user is an admin
    authorize_admin()

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
@jwt_required()
def update_employee(employee_id):
    #verify the user is an admin or the owner of the account
    authorize_admin_or_account_owner_id(employee_id)

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
        user.personal_email = request.json.get('personal_email', user.personal_email)
        
        #to update password, load request into EmployeeSchema to apply validations
        EmployeeSchema().load(request.json, partial = True, unknown = EXCLUDE)

        #handles password in the request
        if request.json.get('password'):
            employee.password = bcrypt.generate_password_hash(request.json.get('password', employee.password)).decode('utf8')

        #only admin can update 'is_admin' field
        if request.json.get('is_admin'):
            authorize_admin()
            employee.is_admin = json.loads(request.json.get('is_admin', str(employee.is_admin)).lower())

        #commit the changes and response to the user
        db.session.commit()
        return EmployeeSchema(exclude=['password', 'bookings']).dump(employee)
    #if employee with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find employee with id {employee_id}'}, 404