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
        date_since, date_until = get_dates(registro_empresa)

        dict_empresa = dict(
            cnpj=registro_empresa.cnpj,
            company_name=registro_empresa.company_name,
            opening_date=registro_empresa.opening_date,
            contact_email=registro_empresa.contact_email,
            zip_code=registro_empresa.zip_code,
            address=registro_empresa.address,
            contact_phone=registro_empresa.contact_phone,
            # contact_person=registro_empresa.contact_person,
            associated_since=date_since,
            associated_until=date_until,
        )
    return dict_empresa

def get_dates(registro_empresa):
	associated_since = registro_empresa.associated_since
	if associated_since:
		date_since = associated_since.split("T")
		date_since = date_since[0] if date_since else ""
	else:
		date_since = ""
	
	associated_until = registro_empresa.associated_until
	if associated_until:
		date_until = associated_until.split("T")
		date_until = date_until[0] if date_since else ""
	else:
		date_until = ""
	return date_since, date_until


def get_all_empresas(registro_empresas):
    list_empresas = [make_dict_empresas(each, simple=True) for each in registro_empresas]
    dict_empresas = dict(associated_companies=list_empresas)
    return dict_empresas


def get_one_empresa(registro_empresa):
    dict_empresa = dict(associated_company=make_dict_empresas(registro_empresa))
    return dict_empresa


class Companies(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def get(self, company_id=None):
		try:
			if company_id:
				one_company = Company.get_one_id_company(company_id)
				if not one_company:
					return make_response(jsonify({"error": "Empresa nao encontrada"}), HTTPStatus.BAD_REQUEST.value)
				dict_empresas = get_one_empresa(one_company)

			else:
				all_companies = Company.get_all_company()
				if not all_companies:
					return make_response(jsonify({"error": "Empresa nao encontrada"}), HTTPStatus.BAD_REQUEST.value)
				dict_empresas = get_all_empresas(all_companies)

			if dict_empresas:
				return make_response(jsonify(dict_empresas), HTTPStatus.OK.value)
			return make_response(jsonify({"error": "Empresa nao encontrada"}), HTTPStatus.BAD_REQUEST.value)
		except Exception as e:
			return make_response(jsonify({"error": "Empresa nao encontrada"}), HTTPStatus.BAD_REQUEST.value)
	
	def post(self):
		
		response = dict(status="fail")

		try:
			post_data = request.get_json(force=True)
			new_company_data = post_data.get("new_company_data")
		except BadRequest:
			response.update(dict(message="O dado informado não foi aceito"))
			status_code = HTTPStatus.BAD_REQUEST.value
			return make_response(jsonify(response), status_code)

		try:
			data = company_schema.load(new_company_data)
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
