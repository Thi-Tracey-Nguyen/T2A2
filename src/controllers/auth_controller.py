from flask import Blueprint, request, abort
from init import db, bcrypt
from models.employee import Employee
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

# @auth_bp.route('/register/', methods=['POST'])
# @jwt_required()
# def auth_register():
#     try:
#         user = User(
#             email = request.json['email'],
#             password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
#             name = request.json.get('name')
#         )
#         db.session.add(user)
#         db.session.commit()
#         #Respond to the user
#         return UserSchema(exclude=['password']).dump(user), 201
#     except IntegrityError:
#         return {'error': 'Email address already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    stmt = db.select(Employee).filter_by(email = request.json['email'])
    employee = db.session.scalar(stmt)
    if employee and bcrypt.check_password_hash(employee.password, request.json['password']):

        # generate token
        token = create_access_token(identity=employee.id, expires_delta=timedelta(days=1))
        return {'email': employee.email, 'token': token, 'is_admin': employee.is_admin}
    else:
        return {"error": "Invalid email or password"}, 401 #401 Unauthorized


def authorize():
    employee_id = get_jwt_identity() #extract the employee identity from the token
    stmt = db.select(Employee).filter_by(id = employee_id)
    employee = db.session.scalar(stmt)
    if not employee.is_admin:
        abort(401)
