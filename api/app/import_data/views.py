from flask.views import MethodView
from flask import make_response, jsonify, request, Response
from app.models import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required
import datetime
from app.import_data.load_file import loadfile
from marshmallow import ValidationError
from app.helpers import decorator_check_user_status



class Upload(MethodView):
	decorators = [decorator_check_user_status, jwt_required]
	def post(self, curse_id=None):
		"""
 		Upload file
  		"""
		try:
			if not curse_id or not int(curse_id):
				return make_response(jsonify({'error': 'Curso não identificado.'}), HTTPStatus.BAD_REQUEST.value) 
		except ValueError as e:
			return make_response(jsonify({'error': 'O curso id deve conter apenas numeros.'}), HTTPStatus.BAD_REQUEST.value) 
		
		try:
			file_import = request.files.getlist('file')
			path = f"/tmp/{datetime.datetime.timestamp}"
			for each_file in file_import:
				extention = each_file.filename.split(".")[1]
				each_file.save(f"{path}.{extention}")
				try:
					loadfile(f"{path}.{extention}", curse_id)

				except ValidationError as err:

					user_msg = ""
					for line, content_line  in err.messages.items():
						for column in content_line.keys():
							if user_msg:
								user_msg += ", "
							msg = f"Erro na linha {line + 1} coluna {column}"

							user_msg += msg

					return make_response(jsonify({'error': user_msg + "."}), HTTPStatus.BAD_REQUEST.value)

			return make_response(jsonify({'message': 'Upload realizado com sucesso'}), HTTPStatus.OK.value)
		except ValueError as e:
			# TODO: (entando aqui pelo RA) verificar outros casos que podem entrar nesta excecao (outros campos da tabela).
			return make_response(jsonify({'error': 'O RA deve conter apenas numeros.'}), HTTPStatus.BAD_REQUEST.value) 
		except Exception as e:
			return make_response(jsonify({'error': 'ouve um erro ao carregar o arquivo'}), HTTPStatus.BAD_REQUEST.value)
