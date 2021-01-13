from flask import Blueprint
from .views import (Upload)


upload_view = Upload.as_view("upload_file")

import_data_views = (
	("/v1/import_data/upload/<curse_id>", upload_view, ["POST"]),
)

import_data_blueprint = Blueprint("import_data", __name__)

for uri, view_func, methods in import_data_views:
	import_data_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)