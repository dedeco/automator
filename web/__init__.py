from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_uploads import configure_uploads

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from .uploadsets import reports_upload
from .routes import page_not_found, internal_server_error

db = SQLAlchemy()

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    register_special_routers(app)
    configure_uploads(app, (reports_upload,))
    return app

def initialize_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app,
         supports_credentials=True,
         resources={r"/automator/excel*": {"origins": app.config['INDEX_URL']}}
         )
    #sentry_sdk.init(
    #    dsn=app.config['SENTRY_URL'],
    #    integrations=[FlaskIntegration()]
    #)

from web.receipt import receipt_blueprint

def register_blueprints(app):
    app.register_blueprint(receipt_blueprint, url_prefix='/automator/excel')

def register_special_routers(app):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
