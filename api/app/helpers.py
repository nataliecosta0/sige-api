from datetime import datetime, timedelta

from dateutil import parser
from flask import json, Response, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity
from http import HTTPStatus

from app import jwt as jwt_app
from app.config import BaseConfig
from app.models import (
	User, 
	UserPermission, 
	InternRecord, 
	InternSchema, 
	Contracts, 
	SubContracts, 
	Company
)


intern_schema = InternSchema(many=True)
JWT_SECRET_KEY = BaseConfig().JWT_SECRET_KEY
blacklist = BaseConfig().blacklist


def master_required(func):
	"""
	docstring
	1 == user
	2 == master
	"""
	def wrapper(*args, **kwargs):
		try:
			current_id = get_jwt_identity()
			# current_id = current_tk.get('sub')
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
			current_id = get_jwt_identity()
			# current_id = current_tk.get('sub')
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
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@jwt_app.user_loader_callback_loader
def load_user_on_login(identity):
	user = User.get_one_user(identity)
	if user:
		return user
	else:
		return None


@jwt_app.user_identity_loader
def user_identity_lookup(user):
	"""
	docstring
	"""
	return user.get("sub")


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
				'exp': datetime.utcnow() + timedelta(days=1),
				'iat': datetime.utcnow(),
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


def custom_response(res, status_code):
  		"""
  		Custom Response Function
  		"""
  		return Response(
    		mimetype="application/json",
    		response=json.dumps(res),
    		status=status_code
  		)


def save_in_intern_record(studants, curse_id):
	all_studants = []
	current_id = get_jwt_identity()
	# current_id = current_tk.get('sub')
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
			'curse_id': curse_id,
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


def make_dict_studants(registro_aluno, simple=False):
    if simple:
        dict_aluno = dict(
            ra=registro_aluno.ra,
            name=registro_aluno.name,
            course_name=registro_aluno.course_name,
        )
    else:
        dict_aluno = dict(
            ra=registro_aluno.ra,
            name=registro_aluno.name,
            birth_date=registro_aluno.birth_date,
            mother_name=registro_aluno.mother_name,
            spouse_name=registro_aluno.spouse_name,
            course_name=registro_aluno.course_name,
            period=registro_aluno.period,
            email=registro_aluno.email,
            residential_address=registro_aluno.residential_address,
            residential_city=registro_aluno.residential_city,
            residential_neighbourhood=registro_aluno.residential_neighbourhood,
            residential_cep=registro_aluno.residential_cep,
            residential_phone_number=registro_aluno.residential_phone_number,
            phone_number=registro_aluno.phone_number,
        )
    return dict_aluno


def get_all_studants_helper(registro_alunos):
    list_alunos = [make_dict_studants(each, simple=True) for each in registro_alunos]
    dict_alunos = dict(intern_records=list_alunos)
    return dict_alunos


def get_one_studant_helper(registro_aluno):
    dict_aluno = dict(intern_record=make_dict_studants(registro_aluno))
    return dict_aluno


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

		subcontracts = [
			{
				"start_date": split_dates(start_date), 
				"ending_date": split_dates(ending_date)
		}]

		dict_contracts= dict(
			company_id=record_contracts.company_id,
			intern_ra=record_contracts.intern_ra,
			status=status,
			subcontracts=subcontracts,
		)
	else:
		dict_contracts = {}
		
	return dict_contracts


def get_all_contracts_helper(record_contracts):
	list_contracts = []
	for each in record_contracts:
		dict_contract = make_dict_contracts(each, simple=True)
		list_contracts.append(dict_contract)

	dict_contracts = dict(internship_contracts=list_contracts)
	return dict_contracts


def get_one_contract_helper(record_contract):
	last_sub_contr = get_last_contracts(record_contract.id)
	dict_contracts = dict(internship_contract=make_dict_contracts(record_contract, last_sub_contr))
	return dict_contracts


def split_dates(current_date):
	if current_date:
		current_date = current_date.split("T")
		current_date = current_date[0] if current_date else ""
	else:
		current_date = ""

	return current_date


def validate_date(start_date, ending_date):
	start = parser.parse(start_date).replace(tzinfo=None)
	ending = parser.parse(ending_date).replace(tzinfo=None)
	current_data = datetime.utcnow()
	if all([current_data > start, current_data < ending]):
		return True
	else:
		return False


def get_last_contracts(contract_id):
	sub_contracts = SubContracts.get_one_sub_contract(contract_id)
	if isinstance(sub_contracts, list):
		chosen = sub_contracts[0]
		if chosen:
			chosen_date = parser.parse(chosen.ending_date)
			for sub_contract in sub_contracts:
				current_date = parser.parse(sub_contract.ending_date)
				if current_date > chosen_date:
					chosen = sub_contract
					chosen_date = current_date
	elif sub_contracts:
		chosen = sub_contracts
	else:
		return False

	return chosen


def interns_by_companies():
	# [{"company_name": nome, "interns_count": 1}]
	all_interns_count = []
	import ipdb; ipdb.sset_trace()
	all_companies = Company.get_all_company()
	if not all_companies or isinstance(all_companies, list):
		return None
	for each_company in all_companies:
		interns_count = 0
		dict_company = {"company_name": each_company.company_name}

		contracts = Contracts.get_company_contracts(each_company.id)
		if not contracts:
			dict_company.update({"interns_count": interns_count})
			all_interns_count.append(dict_company)
			continue
		
		for each_contract in  contracts:
			dict_contract = get_one_contract_helper(each_contract)
			if dict_contract.get("status"):
				interns_count += 1
		dict_company.update({"interns_count": interns_count})
		all_interns_count.append(dict_company)

