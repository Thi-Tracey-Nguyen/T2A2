from flask import Flask
from init import db, ma
from controllers.cli_controller import db_commands
from controllers.clients_controller import clients_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    ma.init_app(app)

    @app.route('/')
    def index():
        return ('Welcome to Nice and Dandy Animal Spa')

    app.register_blueprint(db_commands)
    app.register_blueprint(clients_bp)

    @app.errorhandler(404)
    def not_found(err):
        return {'Error': str(err)}, 404

    return app

