from flask import Blueprint
from .views import (DeleteUser, DisableUser, RoleUser, GetUsers)


delete_view = DeleteUser.as_view("delete_view")
disable_view = DisableUser.as_view("disable_view")
role_user_view = RoleUser.as_view("role_user_view")
get_users_view = GetUsers.as_view("get_users_view")



management_views = (
	("/v1/management/users/<user_id>", delete_view, ["DELETE"]),
	("/v1/management/users/<user_id>/disable", disable_view, ["PUT"]),
	("/v1/management/users/<user_id>/role", role_user_view, ["PUT"]),
	("/v1/management/users/active", get_users_view, ["GET"]),
)

management_blueprint = Blueprint("management", __name__)

for uri, view_func, methods in management_views:
	management_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)