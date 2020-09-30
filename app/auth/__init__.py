from flask import Blueprint
from .views import (LoginApi, SignUpApi, TestLogin, ResetPassword, GetRoleUser)


login_view = LoginApi.as_view("login_api")
sign_up_view = SignUpApi.as_view("sign_up_api")
test_login_view = TestLogin.as_view("test_login")
reset_password_view = ResetPassword.as_view("reset_password")
get_role_user_view = GetRoleUser.as_view("get_role_user")

auth_views = (
	("/v1/auth/authenticate", login_view, ["POST"]),
	("/v1/auth/sign_up", sign_up_view, ["POST"]),
	("/v1/auth/test_login", test_login_view, ["GET"]),
	("/v1/auth/reset_password", reset_password_view, ["POST"]),
	("/v1/auth/user", get_role_user_view, ["GET"])
)

auth_blueprint = Blueprint("auth", __name__)

for uri, view_func, methods in auth_views:
	auth_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)