from flask import make_response, jsonify, request, Response
from http import HTTPStatus
from app import bcrypt
from models import User, UserSchema
from flask.views import MethodView
from app.auth.helpers import generate_token
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required
from datetime import timedelta

user_schema = UserSchema()

class LoginApi(MethodView):
	def post(self):
		"""
		docstring
		"""
		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)
		
		email = post_data.get("email")
		password = post_data.get("password")
		
		obj_users = User.query.filter_by(email=email).first()
		data, error = user_schema.load(req_data, partial=True) #ver isso aqui 

		if not obj_users:
			status_code = HTTPStatus.UNAUTHORIZED.value
			return make_response(jsonify(response), status_code)
		
		if not bcrypt.check_password_hash(obj_users.password.encode('utf-8'), password):
			response.update(dict(message="Usuário ou senha incorretos!"))
			status_code = HTTPStatus.UNAUTHORIZED.value
			return make_response(jsonify(response), status_code)

		if not data.get('email') or not data.get('password'):
			return custom_response({'error': 'you need email and password to sign in'}, 400)
		

		js_user = {
			"name": obj_users.name, # TODO: fazer um metodo serialize em models.py
			"email": obj_users.email,
			"password": obj_users.password,
			"id": obj_users.id
		}
		response = {
			"token": create_access_token(
				identity=js_user, fresh=timedelta(minutes=5)
			)
		}
		#if not get_jwt_identity():
		#	response.update(
		#		dict(
		#			refresh_token=create_refresh_token(
		#				identity=obj_users
		#			)
		#		)
		#	)
		#obj_users.update(last_access_at=datetime.utcnow())
		return make_response(jsonify(response), HTTPStatus.OK.value)

class SignUpApi(MethodView):
	"""
	docstring
	"""
	decorators = [jwt_required]
	def post(self):
		print("FÉ EM DEUS DJ")
		
		response = dict(status="fail")
		data, error = user_schema.load(response)

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)

		if error:
			return custom_response(error, 400)
		# check if user already exist in the db
		user_in_db = User.get_user_by_email(data.get('email'))

		if user_in_db:
			message = {'error': 'User already exist, please supply another email address'}
			return custom_response(message, 400)

		user = User(data)
		user.save()

		ser_data = user_schema.dump(user).data

		token = Auth.generate_token(ser_data.get('id'))

		return custom_response({'jwt_token': token}, 201)
		#return make_response(jsonify(response), HTTPStatus.OK.value)

	def custom_response(res, status_code):
  		"""
  		Custom Response Function
  		"""
  		return Response(
    		mimetype="application/json",
    		response=json.dumps(res),
    		status=status_code
  		)