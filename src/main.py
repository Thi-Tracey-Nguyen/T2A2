from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URL'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEY'] = False

    @app.route('/')
    def index():
        return ('Welcome to Nice and Dandy Animal Spa')

        
    return app

