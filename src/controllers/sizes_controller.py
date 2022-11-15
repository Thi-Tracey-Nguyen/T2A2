from flask import Blueprint, request
from init import db
from models.size import Size, SizeSchema
from controllers.auth_controller import authorize_admin
from flask_jwt_extended import jwt_required


sizes_bp = Blueprint('Sizes', __name__, url_prefix = '/sizes')

#Route to return all sizes
@sizes_bp.route('/')
def get_all_sizes():
    #get all records of the Size model
    stmt = db.select(Size)
    sizes = db.session.scalars(stmt)
    return SizeSchema(many=True, exclude=['pets']).dump(sizes)

#Route to get one sizes by id
@sizes_bp.route('/<int:sizes_id>/')
def get_one_sizes(sizes_id):
    #get one size whose id matches API endpoint
    stmt = db.select(Size).filter_by(id = sizes_id)
    size = db.session.scalar(stmt)

    # check if the size exists, if they do, return the SizeSchema
    if size:
        return SizeSchema(exclude=['pets']).dump(size)
    #if size with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find sizes with id {size_id}'}, 404

#Route to create new size
@sizes_bp.route('/', methods = ['POST'])
@jwt_required()
def create_sizes():
    #verify that the user is an admin
    authorize_admin()

    #load request into SizeSchema to apply validation
    data = SizeSchema().load(request.json)

    #create new sizes instance
    new_size = Size(
       name = data['name'].title(),
       weight = data['weight']
    )

    #add new size to the database and commit it
    db.session.add(new_size)
    db.session.commit()

    #respond to the user
    return SizeSchema().dump(new_size)

#Route to delete a size
@sizes_bp.route('/<int:size_id>/', methods = ['DELETE'])
@jwt_required()
def delete_size(size_id):
    #verify that the user is an admin
    authorize_admin()

    #get one size whose id matches API endpoint
    stmt = db.select(Size).filter_by(id = size_id)
    size = db.session.scalar(stmt)

    # check if the size exists, if it does, delete them from the database
    if size:
        db.session.delete(size)
        db.session.commit()
        return {'message': 'Pet size deleted successfully'}

    #if size with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find a size with id {size_id}'}, 404

#Route to update a size's info
@sizes_bp.route('/<int:size_id>/', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_size(size_id):
    #verify that the user is an admin
    authorize_admin()

    #get one size whose id matches API endpoint
    stmt = db.select(Size).filter_by(id = size_id)
    size = db.session.scalar(stmt)
    
    # check if the size exists, if it does, update its info
    if size:
        #load request into SizeSChema to apply validation
        data = SizeSchema(partial=True).load(request.json)

        #get the info from the request, if not provided, keep as it is
        size.name = data.get('name', size.name).title()
        size.weight = data.get('weight', size.weight)

        db.session.commit() #commit the changes
        return SizeSchema().dump(size)
        
    #if size with the provided id does not exist, return an error message
    else:
        return {'message': f'Cannot find sizes with id {size_id}'}, 404