from flask.views import MethodView
from flask import make_response, jsonify, request
from app.models import User, UserPermission
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from app.helpers import master_required
from werkzeug.exceptions import BadRequest



class DeleteUser(MethodView):
	decorators = [master_required, jwt_required]
	def delete(self, user_id=None):
		"""
 		Delete a user
  		"""
		try:
			user = User.get_one_user(user_id)
			if not user:
				return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
			user.delete()
			return make_response(jsonify({'message': 'deleted'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)


class DisableUser(MethodView):
	decorators = [master_required, jwt_required]
	def put(self, user_id=None):
		"""
 		Disable a user
  		"""
		try:
			# TODO: Validar para o usuario n poder disativar o proprio usuario

			user = User.get_one_user(user_id)
			if not user:
				return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
			if user.status_id ==  2:
				return make_response(jsonify({'message': 'O usuario ja esta inativo.'}), HTTPStatus.BAD_REQUEST.value) 

			user.update({"status_id": 2})
			return make_response(jsonify({'message': 'Usuario desativado com sucesso.'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)



class RoleUser(MethodView):
	decorators = [master_required, jwt_required]
	def put(self, user_id=None):
		"""
 		Altera o nivel do usuario.
  		"""
		try:
			# TODO: Validar para o usuario n poder mudar a propria permissao
			response = dict(status="fail")

			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)

		try:
			role = post_data.get("user_new_data", {}).get("role")
			user_permission = UserPermission.get_one_permission(user_id)
			if not user_permission:
				return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
			user_permission_id = user_permission.permission_id
			if user_permission_id ==  role:
				return make_response(jsonify({'message': 'O usuario ja esta com esta permissao.'}), HTTPStatus.BAD_REQUEST.value) 

			user_permission.update({"permission_id": role})
			return make_response(jsonify({'message': 'Permissao de usuario alterada com sucesso.'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)

class GetUsers(MethodView):
	decorators = [master_required, jwt_required]
	def get(self):
		"""
		Retorna users ativos 
		"""
		try:
			active_users = User.get_active_user()
			response = {"users" : [f"{each_user.id} - {each_user.name}" for each_user in active_users]}
			return make_response(jsonify(response), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'Nenhum user emcontrado'}), HTTPStatus.BAD_REQUEST.value)
