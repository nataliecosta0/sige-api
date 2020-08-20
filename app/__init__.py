from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from config import BaseConfig


app_settings = BaseConfig().APP_SETTINGS
bcrypt = Bcrypt()
#db = MongoEngine()
jwt = JWTManager()

def create_app(config=app_settings):
	"""
	docstring
	"""
	this_app = Flask(__name__)
	this_app.config.from_object(config)
	bcrypt.init_app(this_app)
	#db.init_app(this_app)

	#from app.auth.helpers import jwt
	jwt.init_app(this_app)

	from app.auth import auth_blueprint
	this_app.register_blueprint(auth_blueprint)

	return this_app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
