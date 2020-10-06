from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from config import BaseConfig


base_config = BaseConfig()
app_settings = base_config.APP_SETTINGS
postgres_uri = base_config.POSTGRES_URI

bcrypt = Bcrypt()
#db = MongoEngine()
jwt = JWTManager()
db = SQLAlchemy()
mail = Mail()


def create_app(config=app_settings):
	"""
	docstring
	"""
	this_app = Flask(__name__)
	this_app.config.from_object(config)
	bcrypt.init_app(this_app)

	this_app.config['SQLALCHEMY_DATABASE_URI']=postgres_uri
	db.init_app(this_app)
	

	#from app.auth.helpers import jwt
	jwt.init_app(this_app)

	from app.auth import auth_blueprint
	this_app.register_blueprint(auth_blueprint)

	from app.management import management_blueprint
	this_app.register_blueprint(management_blueprint)

	from app.import_data import import_data_blueprint
	this_app.register_blueprint(import_data_blueprint)

	this_app.config['MAIL_SERVER']=base_config.MAIL_SERVER
	this_app.config['MAIL_PORT']=base_config.MAIL_PORT
	this_app.config['MAIL_USE_SSL']=True
	this_app.config['MAIL_USERNAME']=base_config.MAIL_USERNAME
	this_app.config['MAIL_PASSWORD']=base_config.MAIL_PASSWORD
	mail.init_app(this_app)

	return this_app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
