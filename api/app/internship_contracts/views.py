from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import make_response, jsonify, request, Response
from http import HTTPStatus
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError

from app.helpers import decorator_check_user_status
from app.models import Contracts, ContractSchema, SubContracts, SubContractSchema
from app.helpers import custom_response, get_one_contract_helper, get_all_contracts_helper


contracts_schema = ContractSchema()
sub_contract_schema = SubContractSchema()


class Contract(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def get(self, contract_id=None):
		try:
			if contract_id:
				one_contract = Contracts.get_one_contract(contract_id)
				dict_contracts = get_one_contract_helper(one_contract)
			else:
				all_contracts = Contracts.get_all_contracts()
				dict_contracts = get_all_contracts_helper(all_contracts)

			if dict_contracts:
				return make_response(jsonify(dict_contracts), HTTPStatus.OK.value)
			return make_response(jsonify({"error": "Contrato não enocntrado"}), HTTPStatus.BAD_REQUEST.value)
		except Exception as e:
			return make_response(jsonify({"error": "Erro ao pegar contratos"}), HTTPStatus.BAD_REQUEST.value)
	
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
				new_subcontract_data = post_data.get("new_subcontract_data")
				new_subcontract_data.update({"internship_contract_id": int(contract_id)})
				data = sub_contract_schema.load(new_subcontract_data)
			except ValidationError as err:
				print(err.messages)
				print(err.valid_data)
				return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

			sub_contract = SubContracts(data)
			sub_contract.save()

			return make_response(jsonify({'msg': "Sub contrato criado com sucesso."}), HTTPStatus.OK.value)

		else:

			try:
				new_contract_data = post_data.get("new_contract_data")
				data = contracts_schema.load(new_contract_data)
			except ValidationError as err:
				print(err.messages)
				print(err.valid_data)
				return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

			contract = Contracts(data)
			contract.save()
			current_id = Contracts.get_specific_contract(data).id

			return make_response(jsonify({'internship_contract': {"id": current_id}}), HTTPStatus.OK.value)
