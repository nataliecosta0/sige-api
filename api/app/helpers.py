from app import jwt as jwt_app
import os
import datetime
from flask import json, Response, request, g, jsonify, make_response
from functools import wraps
from app.config import BaseConfig
import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.models import User, UserPermission, InternRecord, InternSchema
from http import HTTPStatus


intern_schema = InternSchema(many=True)
JWT_SECRET_KEY = BaseConfig().JWT_SECRET_KEY


def master_required(func):
	"""
	docstring
	1 == user
	2 == master
	"""
	def wrapper(*args, **kwargs):
		try:
			current_tk = get_jwt_identity()
			current_id = current_tk.get('sub')
			user_permition = UserPermission.get_one_permission(current_id)
			if user_permition.permission_id == 2:
				return func(*args, **kwargs)
			else:
				return make_response(jsonify({"error": "User sem permissao"}), HTTPStatus.UNAUTHORIZED.value)
		except Exception as e:
			return make_response(jsonify({"error": "Usuario nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
	return wrapper


def decorator_check_user_status(func):
	"""
	decorator inativo
	docstring
	1 - Ativo
	2 - Inativo
	3 - Pendente
	"""
	def wrapper(*args, **kwargs):
		try:
			current_tk = get_jwt_identity()
			current_id = current_tk.get('sub')
			current_user = User.get_one_user(current_id)
			user_status = current_user.status_id
			if user_status == 1:
				return func(*args, **kwargs)
			elif user_status == 2:
				return make_response(jsonify({"error": "Usuario Inativo"}), HTTPStatus.UNAUTHORIZED.value)
			elif user_status == 3:
				return make_response(jsonify({"error": "Usuario Pendente de aprovacao"}), HTTPStatus.UNAUTHORIZED.value)
		except Exception as e:
			return make_response(jsonify({"error": "status nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
	return wrapper

def check_user_status(user_status) -> (None):
	"""
	docstring
	1 - Ativo
	2 - Inativo
	3 - Pendente
	"""
	try:
		if user_status == 1:
			return None
		elif user_status == 2:
			return make_response(jsonify({"error": "Usuario Inativo"}), HTTPStatus.UNAUTHORIZED.value)
		elif user_status == 3:
			return make_response(jsonify({"error": "Usuario Pendente de aprovacao"}), HTTPStatus.UNAUTHORIZED.value)
	except Exception as e:
		return make_response(jsonify({"error": "Permissao nao encontrada"}), HTTPStatus.BAD_REQUEST.value)
	

@jwt_app.token_in_blacklist_loader
def check_token_in_blacklist(token):
	"""
	docstring
	"""
	jti = token['jti']
	return TokenBlacklist.check_blacklist(token_id=jti)


@jwt_app.user_identity_loader
def user_identity_lookup(user):
	"""
	docstring
	"""
	return str(user.id)

class Auth():
	"""
	Auth Class
	"""
	@staticmethod
	def generate_token(user_id) -> str:
		"""
		Generate Token Method
		"""
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
				'iat': datetime.datetime.utcnow(),
				'sub': user_id
  			}
			return create_access_token(payload)
			# return jwt.encode(payload, JWT_SECRET_KEY, 'HS256').decode('utf-8')
		except Exception as e:
			return Response(
				mimetype="application/json",
				response=json.dumps({'error': 'error in generating user token'}),
				status=400
				)

	# @staticmethod
	# def decode_token(token):
	# 	"""
	# 	Decode token method
	# 	"""
	# 	re = {'data': {}, 'error': {}}
	# 	try:
  	# 		payload = jwt.decode(token, JWT_SECRET_KEY)
  	# 		re['data'] = {'user_id': payload['sub']}
  	# 		return re
	# 	except jwt.ExpiredSignatureError as e1:
  	# 		re['error'] = {'message': 'token expired, please login again'}
  	# 		return re
	# 	except jwt.InvalidTokenError:
  	# 		re['error'] = {'message': 'Invalid token, please try again with a new token'}
  	# 		return re


	# decorator
	# @staticmethod
	# def auth_required(func):
	# 	"""
	# 	Auth decorator
	# 	"""
	# 	@wraps(func)
	# 	def decorated_auth(*args, **kwargs):
	# 		if 'api-token' not in request.headers:
	# 			return Response(
	# 				mimetype="application/json",
	# 				response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
	# 				status=400
	# 			)
	# 		token = request.headers.get('api-token')
	# 		data = Auth.decode_token(token)
	# 		if data['error']:
	# 			return Response(
	# 				mimetype="application/json",
	# 				response=json.dumps(data['error']),
	# 				status=400
	# 			)
	# 		user_id = data['data']['user_id']
	# 		check_user = User.get_one_user(user_id)
	# 		if not check_user:
	# 			return Response(
	# 				mimetype="application/json",
  	# 				response=json.dumps({'error': 'user does not exist, invalid token'}),
  	# 				status=400
	# 			)
	# 		g.user = {'id': user_id}
	# 		return func(*args, **kwargs)
	# 	return decorated_auth

def custom_response(res, status_code):
  		"""
  		Custom Response Function
  		"""
  		return Response(
    		mimetype="application/json",
    		response=json.dumps(res),
    		status=status_code
  		)


def save_in_intern_record(studants):
	all_studants = []
	current_tk = get_jwt_identity()
	current_id = current_tk.get('sub')
	for studant in studants:
		studant_register = {
			'ra': int(studant.get('RA')),
			'name': studant.get('Nome'),
			'birth_date': studant.get('Data de Nascimento'), 
			'mother_name': studant.get('Nome da Mãe'),
			'spouse_name': studant.get('Nome do Cônjuge'), 
			'course_name': studant.get('Nome do Curso'),
			'period': studant.get('Turno (por extenso)'),
			'email': studant.get('Email'),
			'residential_address': studant.get('Endereço Residencial'),
			'residential_city': studant.get('Cidade Residencial'), 
			'residential_neighbourhood': studant.get('Bairro Familiar'), 
			'residential_cep': studant.get('CEP Residencial'), 
			'residential_phone_number': studant.get('Telefone Residencial'), 
			'phone_number': studant.get('Telefone'),
			'user_id': current_id
		}
		all_studants.append(studant_register)

	InternSchema(many=True).load(all_studants)

	for studant_data in all_studants:
		records = InternRecord(studant_data)
		student_by_ra = records.get_intern_by_ra(studant_data.get('ra'))
		if student_by_ra:
			student_by_ra.update(studant_data)
		else:
			records.save()
