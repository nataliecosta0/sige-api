import re
from sys import intern
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.helpers import decorator_check_user_status
from app.models import InternRecord
from flask import make_response, jsonify, request, Response
from http import HTTPStatus


def make_dict(registro_aluno, simple=False):
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

def get_all_alunos(registro_alunos):
    list_alunos = [make_dict(each, simple=True) for each in registro_alunos]
    dict_alunos = dict(intern_record=list_alunos)
    return dict_alunos


def get_one_aluno(registro_aluno):
    dict_aluno = dict(intern_record=make_dict(registro_aluno))
    return dict_aluno


class GetAluno(MethodView):
    decorators = [decorator_check_user_status, jwt_required]
    def get(self):
        try:
            ra_aluno = request.args.get("intern_ra")
            registro_aluno = InternRecord.get_intern_by_ra(ra_aluno)
            if registro_aluno:
                return make_response(jsonify(get_one_aluno(registro_aluno)), HTTPStatus.OK.value)
            return make_response(jsonify({"error": "Aluno nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
        except Exception as e:
            return make_response(jsonify({"error": "Usuario nao encontrado"}), HTTPStatus.BAD_REQUEST.value)

class GetAllAlunos(MethodView):
    decorators = [decorator_check_user_status, jwt_required]
    def get(self):
        try:
            registros_alunos = InternRecord.get_all_interns()
            if registros_alunos:
                return make_response(jsonify(get_all_alunos(registros_alunos)), HTTPStatus.OK.value)
            return make_response(jsonify({"error": "Alunos nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
        except Exception as e:
            return make_response(jsonify({"error": "Usuario nao encontrado"}), HTTPStatus.BAD_REQUEST.value)