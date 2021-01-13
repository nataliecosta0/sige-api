from flask.views import MethodView
from flask import make_response, jsonify, request
from app.models import User, UserPermission
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.helpers import master_required, decorator_check_user_status
from werkzeug.exceptions import BadRequest



class DeleteUser(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def delete(self, user_id=None):
		"""
 		Delete a user
  		"""
		try:
			current_id = get_jwt_identity()
			# current_id = current_tk.get('sub')
			if current_id == int(user_id):
				return make_response(jsonify({'message': 'Não é possivel deletar esse usuario'}), HTTPStatus.BAD_REQUEST.value) 

			user = User.get_one_user(user_id)
			# permission = UserPermission.get_one_permission(user_id)
			if not all([user]):
				return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
			user.update({"status_id": 2})
			# permission.delete()
			# user.delete()
			return make_response(jsonify({'message': 'deleted'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)


class DisableUser(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def put(self, user_id=None):
		"""
 		Disable a user
  		"""
		try:
			current_id = get_jwt_identity()
			# current_id = current_tk.get('sub')
			if current_id == int(user_id):
				return make_response(jsonify({'message': 'Não é possivel desativar esse usuario'}), HTTPStatus.BAD_REQUEST.value) 


			user = User.get_one_user(user_id)
			if not user:
				return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
			if user.status_id ==  3:
				return make_response(jsonify({'message': 'O usuario ja esta pendente de ativacao.'}), HTTPStatus.BAD_REQUEST.value) 

			user.update({"status_id": 3})
			return make_response(jsonify({'message': 'Usuario desativado com sucesso.'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)


class EnableUser(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def put(self, user_id=None):
		"""
 		Enable a user
  		"""
		try:
			user = User.get_one_user(user_id)
			if not user:
				return make_response(jsonify({'message': 'id nao tem'}), HTTPStatus.BAD_REQUEST.value) 
			if user.status_id ==  1:
				return make_response(jsonify({'message': 'O usuario ja esta ativo.'}), HTTPStatus.BAD_REQUEST.value) 

			user.update({"status_id": 1})
			return make_response(jsonify({'message': 'Usuario ativo com sucesso.'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'precisa de um parametro inteiro'}), HTTPStatus.BAD_REQUEST.value)


class RoleUser(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def put(self, user_id=None):
		"""
 		Altera o nivel do usuario.
  		"""
		response = dict(status="fail")
		try:
			current_id = get_jwt_identity()
			# current_id = current_tk.get('sub')
			if current_id == int(user_id):
				return make_response(jsonify({'message': 'Não é possivel alterar a permissao desse usuario'}), HTTPStatus.BAD_REQUEST.value) 

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


class GetEnableUsers(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def get(self):
		"""
		Retorna users ativos 
		"""
		try:
			active_users = User.get_status_user(status=1)
			response = {"users" : [{
							"id": each_user.id, "name": each_user.name, "email": each_user.email} 
							for each_user in active_users
							]
						}
			return make_response(jsonify(response), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'Nenhum usuario encontrado'}), HTTPStatus.BAD_REQUEST.value)


class GetDisableUsers(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def get(self):
		"""
		Retorna users inativos 
		"""
		try:
			disable_users = User.get_status_user(status=2)
			response = {"users" : [{
				"id": each_user.id, "name": each_user.name, "email": each_user.email} 
				for each_user in disable_users
				]
			}
			return make_response(jsonify(response), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'Nenhum usuario encontrado'}), HTTPStatus.BAD_REQUEST.value)


class GetPendingUsers(MethodView):
	decorators = [master_required, decorator_check_user_status, jwt_required]
	def get(self):
		"""
		Retorna users ativos 
		"""
		try:
			pending_users = User.get_status_user(status=3)
			
			response = {"users" : [{
				"id": each_user.id, "name": each_user.name, "email": each_user.email} 
				for each_user in pending_users
				]
			}
			return make_response(jsonify(response), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'message': 'Nenhum usuario encontrado'}), HTTPStatus.BAD_REQUEST.value)

