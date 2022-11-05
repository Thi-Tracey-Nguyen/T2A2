from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from models.roster import Roster, RosterSchema
from flask_jwt_extended import jwt_required
from datetime import datetime


rosters_bp = Blueprint('Rosters', __name__, url_prefix = '/rosters')

#Route to return all rosters
@rosters_bp.route('/')
def get_all_rosters():
    #get all records of the Roster model
    stmt = db.select(Roster).order_by(Roster.date)
    rosters = db.session.scalars(stmt)
    return RosterSchema(many=True).dump(rosters)

#Route to get one roster by id
@rosters_bp.route('/<int:roster_id>/')
def get_one_roster(roster_id):
    #get one roster whose id matches API endpoint
    stmt = db.select(Roster).filter_by(id = roster_id)
    roster = db.session.scalar(stmt)
    # check if the roster exists, if they do, return the RosterSchema
    if roster:
        return RosterSchema().dump(roster)
    #if roster with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find roster with id {roster_id}'}, 404

#Route to get add rosters by date
@rosters_bp.route('/<date>/')
def get_roster_by_date(date):
    #get all rosters date matches API endpoint
    stmt = db.select(Roster).filter_by(date=date)
    rosters = db.session.scalars(stmt)

    # respond to the user
    return RosterSchema(many=True).dump(rosters)

#Route to create new roster
@rosters_bp.route('/', methods = ['POST'])
def create_roster():
    #load request data on to the schema to apply validations
    data = RosterSchema().load(request.json)

    #create new roster instance
    new_roster = Roster(
        date = request.json.get('date'),
        employee_id = request.json.get('employee_id')
    )

    #add new roster to the database and commit it
    db.session.add(new_roster)
    db.session.commit()

    #respond to the user
    return RosterSchema().dump(new_roster)

#Route to delete a roster
@rosters_bp.route('/<int:roster_id>/', methods = ['DELETE'])
def delete_roster(roster_id):
    #get one roster whose id matches API endpoint
    stmt = db.select(Roster).filter_by(id = roster_id)
    roster = db.session.scalar(stmt)
    # check if the roster exists, if they do, delete them from the database
    if roster:
        db.session.delete(roster)
        db.session.commit()
        return {'message': 'Roster deleted successfully'}
    #if roster with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find roster with id {roster_id}'}, 404

#Route to update roster's info
@rosters_bp.route('/<int:roster_id>/', methods = ['PUT', 'PATCH'])
def update_roster(roster_id):
    #get one roster whose id matches API endpoint
    stmt = db.select(Roster).filter_by(id = roster_id)
    roster = db.session.scalar(stmt)
    
    # check if the roster exists, if it does, update its info
    if roster:
        try:
            #load the request into RosterSchema to apply validations
            data = RosterSchema().load(request.json)
            #get the info from the request, if not provided, keep as it is
            roster.service_id = data.get('service_id') or roster.service_id
            roster.pet_id = data.get('pet_id') or roster.pet_id
            roster.employee_id = data.get('employee_id') or roster.employee_id
            roster.date = data.get('date') or roster.date
            roster.time = data.get('time') or roster.time
            roster.status = data.get('status') or roster.status
            db.session.commit() #commit the changes
            return RosterSchema().dump(roster)
        #catch IntegrityError when the updated info already exist in the database
        except IntegrityError:
            return {'message': 'The combination of pet\'s id, date and time already exists'}

    #if roster with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find roster with id {roster_id}'}, 404