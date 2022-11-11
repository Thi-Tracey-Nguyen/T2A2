from flask import Flask
from init import db, ma, bcrypt, jwt
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
import os
from controllers.cli_controller import db_commands
from controllers.users_controller import users_bp
from controllers.clients_controller import clients_bp
from controllers.pets_controller import pets_bp
from controllers.employees_controller import employees_bp
from controllers.bookings_controller import bookings_bp
from controllers.user_types_controller import user_types_bp
from controllers.services_controller import services_bp
from controllers.pet_types_controller import pet_types_bp
from controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def index():
        return ('Welcome to Nice and Dandy Animal Spa')

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_types_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(pet_types_bp)

    @app.errorhandler(404)
    def not_found(err):
        return {'Error': str(err)}, 404

    @app.errorhandler(400)
    def bad_request(err):
        return {'Error': str(err)}, 400

    @app.errorhandler(401)
    def unauthorize(err):
        return {'Error': str(err)}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'Error': f'The field {err} is required'}, 400

    # @app.errorhandler(IntegrityError)
    # def integrity_error(err):
    #     return {'message': 'Record already exists'}, 409

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'message': err.messages}, 400

    @app.errorhandler(DataError)
    def data_error(err):
        return {'message': 'Input data is invalid'}, 400

    return app

