from flask import Blueprint
from .views import (LoginApi, SignUpApi)


login_view = LoginApi.as_view("login_api")
sign_up_view = SignUpApi.as_view("sign_up_api")

auth_views = (
	("/v1/auth/authenticate", login_view, ["POST"]),
	("/v1/auth/sign_up", sign_up_view, ["POST"])
)

auth_blueprint = Blueprint("auth", __name__)

for uri, view_func, methods in auth_views:
	auth_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)