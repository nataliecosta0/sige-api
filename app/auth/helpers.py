from app import jwt as jwt_app
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from app.models import User
from app.config import BaseConfig
import jwt
from flask_jwt_extended import create_access_token


JWT_SECRET_KEY = BaseConfig().JWT_SECRET_KEY


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
	# 		import ipdb; ipdb.sset_trace()
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