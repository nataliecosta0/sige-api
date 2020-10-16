from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.helpers import decorator_check_user_status
from flask import make_response, jsonify, request, Response
from http import HTTPStatus
from app.models import Contracts, ContractSchema, SubContracts, SubContractSchema
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from app.helpers import custom_response
from datetime import datetime
from dateutil import parser


contracts_schema = ContractSchema()
sub_contract_schema = SubContractSchema()

def make_dict_contracts(record_contracts, sub_contr=None, simple=False):
	if simple:
		dict_contracts = dict(
			id=record_contracts.id,
			company_id=record_contracts.company_id,
			intern_ra=record_contracts.intern_ra
		)
	elif not simple and sub_contr:
		start_date = sub_contr.start_date
		ending_date = sub_contr.ending_date
		if validate_date(start_date, ending_date):
			status = 1
		else:
			status = 0

		dict_contracts= dict(
			company_id=record_contracts.company_id,
			intern_ra=record_contracts.intern_ra,
			status=status,
			start_date=start_date,
			ending_date=ending_date
		)
	else:
		dict_contracts = {}
		
	return dict_contracts


def validate_date(start_date, ending_date):
	current_data = datetime.utcnow()
	if all([current_data > parser.parse(start_date), current_data < parser.parse(ending_date)]):
		return True
	else:
		return False

def get_last_contracts(contract_id):
	import ipdb; ipdb.sset_trace()

	sub_contracts = SubContracts.get_one_sub_contract(contract_id)
	chosen = sub_contracts[0]
	if chosen:
		chosen_date = parser.parse(chosen.ending_date)
		for sub_contract in sub_contracts:
			current_date = parser.parse(sub_contract.ending_date)
			if current_date > chosen_date:
				chosen = sub_contract
				chosen_date = current_date

		return chosen

	return False


def get_all_contratos(record_contracts):
	list_contracts = []
	for each in record_contracts:
		dict_contract = make_dict_contracts(each, simple=True)
		list_contracts.append(dict_contract)

	dict_contracts = dict(internship_contracts=list_contracts)
	return dict_contracts


def get_one_contrato(record_contracts):
	last_sub_contr = get_last_contracts(record_contracts.id)
	dict_contracts = dict(internship_contracts=make_dict_contracts(record_contracts, last_sub_contr))
	return dict_contracts


class Contract(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def get(self, contract_id=None):
		try:
			import ipdb; ipdb.sset_trace()

			if contract_id:
				all_contract = Contracts.get_one_contract(contract_id)
				dict_contracts = get_one_contrato(all_contract)
			else:
				all_contracts = Contracts.get_all_contracts()
				dict_contracts = get_all_contratos(all_contracts)

			if dict_contracts:
				return make_response(jsonify(dict_contracts), HTTPStatus.OK.value)
			return make_response(jsonify({"error": "Contrato não encontrado"}), HTTPStatus.BAD_REQUEST.value)
		except Exception as e:
			return make_response(jsonify({"error": "Contrato não encontrado"}), HTTPStatus.BAD_REQUEST.value)
	
	def post(self, contract_id=None):

		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)
				
		if contract_id:

			try:
				post_data.update({"internship_contract_id": int(contract_id)})
				data = sub_contract_schema.load(post_data)
			except ValidationError as err:
				print(err.messages)
				print(err.valid_data)
				return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

			sub_contract = SubContracts(data)
			sub_contract.save()

			return make_response(jsonify({'msg': "Sub contrato criado com sucesso."}), HTTPStatus.OK.value)


		else:

			try:
				data = contracts_schema.load(post_data)
			except ValidationError as err:
				print(err.messages)
				print(err.valid_data)
				return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

			contract = Contracts(data)
			contract.save()
			current_id = Contracts.get_specific_contract(data).id

			return make_response(jsonify({'internship_contract': {"id": current_id}}), HTTPStatus.OK.value)
