from flask import Blueprint
from .views import (GetAluno, GetAllAlunos)


get_aluno_view = GetAluno.as_view("get_aluno")
get_all_aluno_view = GetAllAlunos.as_view("get_all_aluno")

import_data_views = (
	("/v1/intern_records/records/record", get_aluno_view, ["GET"]),
	("/v1/intern_records/all", get_all_aluno_view, ["GET"]),

)

intern_record_blueprint = Blueprint("intern_record", __name__)

for uri, view_func, methods in import_data_views:
	intern_record_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)