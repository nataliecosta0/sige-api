from flask import Blueprint
from .views import (
	LoginApi, SignUpApi, TestLogin, 
	ResetPassword, GetRoleUser, 
	BeginAccessRecovery,
	VerifyAccessRecoveryCode
)


login_view = LoginApi.as_view("login_api")
sign_up_view = SignUpApi.as_view("sign_up_api")
test_login_view = TestLogin.as_view("test_login")
reset_password_view = ResetPassword.as_view("reset_password")
get_role_user_view = GetRoleUser.as_view("get_role_user")

begin_access_recovery_view = BeginAccessRecovery.as_view("begin_access_recovery")
verify_access_recovery_code_view = VerifyAccessRecoveryCode.as_view("verify_access_recovery_code")


auth_views = (
	("/v1/auth/authenticate", login_view, ["POST"]),
	("/v1/auth/sign_up", sign_up_view, ["POST"]),
	("/v1/auth/test_login", test_login_view, ["GET"]),
	("/v1/auth/reset_password", reset_password_view, ["POST"]),
	("/v1/auth/user", get_role_user_view, ["GET"]),
	("/v1/auth/begin_access_recovery", begin_access_recovery_view, ["POST"]),
	("/v1/auth/verify_access_recovery_code", verify_access_recovery_code_view, ["POST"])
)

auth_blueprint = Blueprint("auth", __name__)

for uri, view_func, methods in auth_views:
	auth_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)