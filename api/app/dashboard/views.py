from flask.views import MethodView
from flask import make_response, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from app.helpers import decorator_check_user_status, interns_by_companies


class InterByCompanies(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def get(self):
		try:
			companies_contracts = interns_by_companies()
			return make_response(jsonify({'interns_by_companies': companies_contracts}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'error': 'ouve um erro ao pegar os dados.'}), HTTPStatus.BAD_REQUEST.value)
