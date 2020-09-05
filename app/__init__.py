from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from config import BaseConfig


config = BaseConfig()
app_settings = config.APP_SETTINGS
postgres_uri = config.POSTGRES_URI

bcrypt = Bcrypt()
#db = MongoEngine()
jwt = JWTManager()
db = SQLAlchemy()


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

	return this_app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
