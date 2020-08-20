from flask import make_response, jsonify
from http import HTTPStatus

from flask.views import MethodView
from werkzeug.exceptions import BadRequest


class LoginApi(MethodView):
	def post(self):
		"""
		docstring
		"""
		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O Dado informado nao foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)
		
		email = post_data.get("email")
		password = post_data.get("password")