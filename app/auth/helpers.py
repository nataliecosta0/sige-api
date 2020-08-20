from app import jwt
from app.models import TokenBlacklist


@jwt.token_in_blacklist_loader
def check_token_in_blacklist(token):
	"""
	docstring
	"""
	jti = token['jti']
	return TokenBlacklist.check_blacklist(token_id=jti)


@jwt.user_identity_loader
def user_identity_lookup(user):
	"""
	docstring
	"""
	return str(user.id)
