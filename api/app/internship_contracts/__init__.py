from flask import Blueprint
from .views import (Contract)


contracts_view = Contract.as_view("contracts")

internship_contracts_views = (
	("/v1/internship_contracts/contracts/<contract_id>", contracts_view, ["GET", "POST"]),
	("/v1/internship_contracts/contracts/", contracts_view, ["GET", "POST"]),
	("/v1/internship_contracts/contracts", contracts_view, ["GET", "POST"]),

)

internship_contracts_blueprint = Blueprint("internship_contracts", __name__)

for uri, view_func, methods in internship_contracts_views:
	internship_contracts_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)