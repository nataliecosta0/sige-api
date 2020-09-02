from flask.views import MethodView
from flask import make_response, jsonify
from app.models import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required


class DeleteApi(MethodView):
	decorators = [jwt_required]
	def delete(self, user_id=None):
		"""
 		Delete a user
  		"""
		if not isinstance(user_id, int):
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)
		user = User.get_one_user(user_id)
		if not user:
			return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
		user.delete()
		return make_response(jsonify({'message': 'deleted'}), HTTPStatus.OK.value)
