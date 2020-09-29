from flask import make_response, jsonify, request, Response
from http import HTTPStatus
from app import bcrypt
from app.models import User, UserSchema, UserPermission
from flask.views import MethodView
from app.helpers import Auth, custom_response, master_required, check_user_status, decorator_check_user_status
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required, get_jwt_claims
from datetime import timedelta
from marshmallow import ValidationError

user_schema = UserSchema()
auth = Auth()


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

		if not obj_users:
			status_code = HTTPStatus.UNAUTHORIZED.value
			return make_response(jsonify(response), status_code)
		
		if not bcrypt.check_password_hash(obj_users.password.encode('utf-8'), password):
			response.update(dict(message="Usuário ou senha incorretos!"))
			status_code = HTTPStatus.UNAUTHORIZED.value
			return make_response(jsonify(response), status_code)

		if not obj_users.email or not obj_users.password:
			return custom_response({'error': 'you need email and password to sign in'}, HTTPStatus.BAD_REQUEST.value)
		
		status_response = check_user_status(obj_users.status_id)
		if status_response:
			return status_response

		user_id = obj_users.id
		token = auth.generate_token(user_id)
		#if not get_jwt_identity():
		#	response.update(
		#		dict(
		#			refresh_token=create_refresh_token(
		#				identity=obj_users
		#			)
		#		)
		#	)
		#obj_users.update(last_access_at=datetime.utcnow())
		#return make_response(jsonify(response), HTTPStatus.OK.value)
		return custom_response({'token': token}, HTTPStatus.OK.value) 


class SignUpApi(MethodView):
	"""
	docstring
	"""
	def post(self):
		
		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)

		try:
			post_data.update({"status_id": 3})
			data = user_schema.load(post_data)
		except ValidationError as err:
			print(err.messages)
			print(err.valid_data)
			return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

		# check if user already exist in the db
		user_in_db = User.get_user_by_email(data.get('email'))

		if user_in_db:
			message = {'error': 'User already exist, please supply another email address'}
			return custom_response(message, HTTPStatus.BAD_REQUEST.value)

		user = User(data)
		user.save()

		user_id = user.id

		permission = UserPermission.get_one_permission(user_id)
		if not permission:
			user_permission = UserPermission(
				data={"permission_id": 1, "user_id": user_id}
				)
			user_permission.save()

		# token = Auth.generate_token(user_id)

		return make_response(jsonify({'msg': "Usuario Criado com sucesso."}), HTTPStatus.OK.value)
		#return make_response(jsonify(response), HTTPStatus.OK.value)

class TestLogin(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def get(self):
		return make_response(jsonify({"msg": "LOGIN BOM"}), HTTPStatus.OK.value)

class ResetPassword(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def post(self):
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

		if not obj_users:
			status_code = HTTPStatus.UNAUTHORIZED.value
			return make_response(jsonify(response), status_code)

		obj_users.update({"password": password})
		return make_response(jsonify({'msg': "TROCA FOI HEIM"}), HTTPStatus.OK.value)
