from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.helpers import decorator_check_user_status
from flask import make_response, jsonify, request, Response
from http import HTTPStatus
from app.models import Company, CompanySchema
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError
from app.helpers import custom_response


company_schema = CompanySchema()


def make_dict_empresas(registro_empresa, simple=False):
    if simple:
        dict_empresa = dict(
            cnpj=registro_empresa.cnpj,
            company_name=registro_empresa.company_name,
            id=registro_empresa.id,
        )
    else:
        dict_empresa = dict(
            cnpj=registro_empresa.cnpj,
            company_name=registro_empresa.company_name,
            opening_date=registro_empresa.opening_date,
            contact_email=registro_empresa.contact_email,
            zip_code=registro_empresa.zip_code,
            address=registro_empresa.address,
            contact_phone=registro_empresa.contact_phone,
            contact_person=registro_empresa.contact_person,
            associated_since=registro_empresa.associated_since,
            associated_until=registro_empresa.associated_until,
        )
    return dict_empresa


def get_all_empresas(registro_empresas):
    list_empresas = [make_dict_empresas(each, simple=True) for each in registro_empresas]
    dict_empresas = dict(associated_companies=list_empresas)
    return dict_empresas


def get_one_empresa(registro_empresa):
    dict_empresa = dict(associated_companies=make_dict_empresas(registro_empresa))
    return dict_empresa


class Companies(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def get(self):
		try:
			all_companies = Company.get_all_company()
			dict_empresas = get_all_empresas(all_companies)
			if dict_empresas:
				return make_response(jsonify(dict_empresas), HTTPStatus.OK.value)
			return make_response(jsonify({"error": "Empresa nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
		except Exception as e:
			return make_response(jsonify({"error": "Empresa nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
	
	def post(self):
		
		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True) 
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)

		try:
			data = company_schema.load(post_data)
		except ValidationError as err:
			print(err.messages)
			print(err.valid_data)
			return custom_response(err.messages, HTTPStatus.BAD_REQUEST.value)

		# check if user already exist in the db
		company_in_db = Company.get_one_company(data.get("company_name"))

		if company_in_db:
			message = {'error': 'Company already exist.'}
			return custom_response(message, HTTPStatus.BAD_REQUEST.value)

		empresa = Company(data)
		empresa.save()

		# user_id = empresa.id

		# permission = UserPermission.get_one_permission(user_id)
		# if not permission:
		# 	user_permission = UserPermission(
		# 		data={"permission_id": 1, "user_id": user_id}
		# 		)
		# 	user_permission.save()

		# token = Auth.generate_token(user_id)

		return make_response(jsonify({'msg': "Empresa Criada com sucesso."}), HTTPStatus.OK.value)
