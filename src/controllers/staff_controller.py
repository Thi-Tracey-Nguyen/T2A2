from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.staff import Staff, StaffSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required


staff_bp = Blueprint('Staff', __name__, url_prefix = '/staff')

#Route to return all staff
@staff_bp.route('/')
def get_all_staff():
    #get all records of the Staff model
    stmt = db.select(Staff)
    staff = db.session.scalars(stmt)
    return StaffSchema(many=True).dump(staff)

#Route to get one staff's info
@staff_bp.route('/<int:staff_id>/')
def get_one_staff(staff_id):
    #get one staff whose id matches API endpoint
    stmt = db.select(Staff).filter_by(id = staff_id)
    staff = db.session.scalar(stmt)
    # check if the staff exists, if they do, return the StaffSchema
    if staff:
        return StaffSchema().dump(staff)
    #if staff with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find staff with id {staff_id}'}, 404


#Route to create new staff
@staff_bp.route('/', methods = ['POST'])
def create_staff():
    #create a user with provided info first
    #load info from the request to UserSchema to apply validation methods
    data = UserSchema().load(request.json)
    #create a new user instance from the provided data
    user = User(
        f_name = data['f_name'],
        l_name = data['l_name'],
        phone = data['phone'],
        type_id = 2 #type_id for staff
    )
    #add user to the database if no conflicts
    try:
        db.session.add(user)
        db.session.commit()

        #retrieve the new user's id with the provided phone number because it is unique
        stmt = db.select(User).filter_by(phone = data['phone'])
        user = db.session.scalar(stmt)

        #create a new staff instance with the user_id from the new user
        new_staff = Staff(user_id = user.id)

        #add the new staff to the database and commit
        db.session.add(new_staff)
        db.session.commit()

        #respond to the user
        return StaffSchema(exclude = ['pets']).dump(new_staff), 201

    #catch IntegrityError when phone number already exists
    except IntegrityError:
        return {'message': 'Phone number already exists'}, 409
    

#Route to delete a staff
@staff_bp.route('/<int:staff_id>/', methods = ['DELETE'])
def delete_staff(staff_id):
    #get one pet whose id matches API endpoint
    stmt = db.select(Staff).filter_by(id = staff_id)
    staff = db.session.scalar(stmt)
    # check if the staff exists, if they do, delete them from the staff table
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return {'message': 'Staff deleted successfully'}
    #if staff with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find staff with id {staff_id}'}, 404

#Route to update staff's info
@staff_bp.route('/<int:staff_id>/', methods = ['PUT', 'PATCH'])
def update_staff(staff_id):
    #get one staff whose id matches API endpoint
    stmt = db.select(Staff).filter_by(id = staff_id)
    staff = db.session.scalar(stmt)
    # check if the staff exists, if they do, update their info
    if staff:

        #load the request into the UserSchema to use validations
        data = UserSchema().load(request.json)

        #get the user_id from staff id to update corresponding fields in users table
        user_stmt = db.select(User).filter_by(id = staff.user_id)
        user = db.session.scalar(user_stmt)

        #assign user's attributes with provided values 
        #or keep as it is if not provided
        user.f_name = data.get('f_name') or user.f_name
        user.l_name = data.get('l_name') or user.l_name
        user.phone = data.get('phone') or user.phone

        #commit the changes and response to the user
        db.session.commit()
        return StaffSchema().dump(staff)
    #if staff with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find staff with id {staff_id}'}, 404