from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.helpers import decorator_check_user_status
from flask import make_response, jsonify, request, Response
from http import HTTPStatus
from app.models import Contracts, ContractSchema
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from app.helpers import custom_response
from datetime import datetime


contracts_schema = ContractSchema()

def make_dict_contracts(record_contracts, simple=False):
    if simple:
        dict_contracts = dict(
			id=record_contracts.id
            company_id=record_contracts.company_id,
            intern_ra=record_contracts.intern_ra
        )
    else:
        dict_contracts= dict(
            company_id=record_contracts.company_id,
            intern_ra=record_contracts.intern_ra,
            start_date=record_contracts.start_date,
            ending_date=record_contracts.ending_date
        )
    return dict_contracts


def validate_date(start_date, ending_date):
	current_data = datetime.utcnow()
	if all([current_data > start_date, current_data < ending_date]):
		return True
	else:
		return False


def get_all_contratos(record_contracts):
    list_contracts = [make_dict_contracts(each, simple=True) for each in record_contracts]
    dict_contracts = dict(internship_contracts=list_contracts)
    return dict_contracts


def get_one_contrato(record_contracts):
    dict_contracts = dict(internship_contracts=make_dict_contracts(record_contracts))
    return dict_contracts


class Contract(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def get(self):
		try:
			all_contracts = Contracts.get_all_contracts()
			dict_contracts = get_all_contratos(all_contracts)
			if dict_contracts:
				return make_response(jsonify(dict_contracts), HTTPStatus.OK.value)
			return make_response(jsonify({"error": "Contrato não encontrado"}), HTTPStatus.BAD_REQUEST.value)
		except Exception as e:
			return make_response(jsonify({"error": "Contrato não encontrado"}), HTTPStatus.BAD_REQUEST.value)
	
	def post(self):
		
		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)

		try:
			data = contracts_schema.load(post_data)
		except ValidationError as err:
			print(err.messages)
			print(err.valid_data)
			return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

		# check if user already exist in the db
		company_in_db = Company.get_one_contract(data.get("company_name"))

		if contract_in_db:
			message = {'error': 'Contract already exist.'}
			return custom_response(message, HTTPStatus.BAD_REQUEST.value)

		contract = Contracts(data)
		contract.save()

		return make_response(jsonify({'msg': "Empresa Criada com sucesso."}), HTTPStatus.OK.value)
