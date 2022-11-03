from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.employee import Employee, EmployeeSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE

employees_bp = Blueprint('Employee', __name__, url_prefix = '/employees')

#Route to return all employee
@employees_bp.route('/')
def get_all_employee():
    #get all records of the Employee model
    stmt = db.select(Employee)
    employees = db.session.scalars(stmt)
    return EmployeeSchema(many=True).dump(employees)

#Route to get one employee's info
@employees_bp.route('/<int:employee_id>/')
def get_one_employee(employee_id):
    #get one employee whose id matches API endpoint
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)
    # check if the employee exists, if they do, return the EmployeeSchema
    if employee:
        return EmployeeSchema().dump(employee)
    #if employee with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find employee with id {employee_id}'}, 404

#Route to get one employee's info by unique phone number
@employees_bp.route('/phone/<phone>/')
def get_one_employee_by_phone(phone):
    #has to go through users table because it is where phone number is stored
    #get one user whose phone number matches API endpoint
    stmt = db.select(User).filter_by(phone = phone)
    user = db.session.scalar(stmt)

    #checks if the user with the phone number exists
    if user:
        #retrieve user_id from the user and look it up in the employee table
        employee_stmt = db.select(Employee).filter_by(user_id = user.id)
        employee = db.session.scalar(employee_stmt)

        # check if the employee exists, if they do, return the ClientSchema
        if employee:
            return EmployeeSchema().dump(employee)

        #if employee with the provided phone number does not exist, return an error message
        else:
            return {'message': 'Cannot find employee associated with the phone number'}, 404

    #if user with the provided phone number does not exist, return an error message
    else:
        return {'message': 'Cannot find user associated with the phone number'}, 404

#Route to create new employee
@employees_bp.route('/', methods = ['POST'])
def create_employee():
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

        #create a new employee instance with the user_id from the new user
        new_employee = Employee(user_id = user.id)

        #add the new employee to the database and commit
        db.session.add(new_employee)
        db.session.commit()

        #respond to the user
        return EmployeeSchema().dump(new_employee), 201

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
        user_data = UserSchema().load(request.json, unknown=EXCLUDE)

        #get the user_id from employee id to update corresponding fields in users table
        user_stmt = db.select(User).filter_by(id = employee.user_id)
        user = db.session.scalar(user_stmt)

        #f_name, l_name and phone are in the users table
        #or keep as it is if not provided
        user.f_name = request.json.get('f_name') or user.f_name
        user.l_name = request.json.get('l_name') or user.l_name
        user.phone = request.json.get('phone') or user.phone
        
        #to update password, load provided password into ValidatingSchema
        #to validate lenght and content
        # EmployeeSchema.ValidatingSchema().load({'password': request.json.get('password')})
        employee_data = EmployeeSchema().load(request.json, unknown = EXCLUDE)
        employee.password = request.json.get('password') or employee.password

        #commit the changes and response to the user
        db.session.commit()
        return EmployeeSchema(exclude=['password']).dump(employee)
    #if employee with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find employee with id {employee_id}'}, 404