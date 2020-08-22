from flask import make_response, jsonify, request
from http import HTTPStatus
from app import bcrypt
from models import User
from flask.views import MethodView
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required
from datetime import timedelta


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

		js_user = {
			"name": obj_users.name,
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

		return make_response(jsonify(response), HTTPStatus.OK.value)