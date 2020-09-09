from flask.views import MethodView
from flask import make_response, jsonify, request, Response
from app.models import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required
import datetime
from app.import_data.load_file import loadfile


class Upload(MethodView):
	decorators = []
	def post(self):
		"""
 		Upload file
  		"""
		try:
			import ipdb; ipdb.sset_trace()
			file = request.files.getlist('file')
			path = f"/tmp/{datetime.datetime.timestamp}"
			for f in file:
				extention = f.filename.split(".")[1]
				f.save(f"{path}.{extention}")
				loadfile(f"{path}.{extention}")
			return make_response(jsonify({'message': 'Upload realizado com sucesso'}), HTTPStatus.OK.value)
		except Exception as e:
			return make_response(jsonify({'error': 'ouve um erro ao carregar o arquivo'}), HTTPStatus.BAD_REQUEST.value)
