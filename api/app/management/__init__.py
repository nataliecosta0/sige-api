from flask import Blueprint
from .views import (DeleteUser, DisableUser, EnableUser, 
RoleUser, GetEnableUsers, GetDisableUsers, GetPendingUsers)


delete_view = DeleteUser.as_view("delete_user")
disable_view = DisableUser.as_view("disable_user")
enable_view = EnableUser.as_view("enable_user")
role_user_view = RoleUser.as_view("role_user_user")
get_enable_view = GetEnableUsers.as_view("get_enable_user")
get_disable_view = GetDisableUsers.as_view("get_disable_user")
get_pending_view = GetPendingUsers.as_view("get_pending_user")

management_views = (
	("/v1/management/users/<user_id>", delete_view, ["DELETE"]),
	("/v1/management/users/<user_id>/disable", disable_view, ["PUT"]),
	("/v1/management/users/<user_id>/enable", enable_view, ["PUT"]),
	("/v1/management/users/<user_id>/role", role_user_view, ["PUT"]),
	("/v1/management/users/active", get_enable_view, ["GET"]),
	("/v1/management/users/disable", get_disable_view, ["GET"]),
	("/v1/management/users/pending", get_pending_view, ["GET"]),
)

management_blueprint = Blueprint("management", __name__)

for uri, view_func, methods in management_views:
	management_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)