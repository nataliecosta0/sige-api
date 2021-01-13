from flask.views import MethodView
from flask_jwt_extended import jwt_required
from app.helpers import decorator_check_user_status, get_one_studant_helper, get_all_studants_helper
from app.models import InternRecord
from flask import make_response, jsonify, request, Response
from http import HTTPStatus


class GetAluno(MethodView):
    decorators = [decorator_check_user_status, jwt_required]
    def get(self):
        try:
            ra_aluno = request.args.get("intern_ra")
            registro_aluno = InternRecord.get_intern_by_ra(ra_aluno)
            if registro_aluno:
                return make_response(jsonify(get_one_studant_helper(registro_aluno)), HTTPStatus.OK.value)
            return make_response(jsonify({"error": "Aluno nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
        except Exception as e:
            return make_response(jsonify({"error": "Usuario nao encontrado"}), HTTPStatus.BAD_REQUEST.value)

class GetAllAlunos(MethodView):
    decorators = [decorator_check_user_status, jwt_required]
    def get(self):
        try:
            registros_alunos = InternRecord.get_all_interns()
            if registros_alunos:
                return make_response(jsonify(get_all_studants_helper(registros_alunos)), HTTPStatus.OK.value)
            return make_response(jsonify({"error": "Alunos nao encontrado"}), HTTPStatus.BAD_REQUEST.value)
        except Exception as e:
            return make_response(jsonify({"error": "Usuario nao encontrado"}), HTTPStatus.BAD_REQUEST.value)