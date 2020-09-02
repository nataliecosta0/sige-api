from flask import Blueprint
from .views import (DeleteApi)


delete_view = DeleteApi.as_view("delete_view")

management_views = (
	("/v1/auth/management/users/<user_id>/delete", delete_view, ["DELETE"]),
)

management_blueprint = Blueprint("management", __name__)

for uri, view_func, methods in management_views:
	management_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)