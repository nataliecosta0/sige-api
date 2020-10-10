from flask import Blueprint
from .views import (Contracts)


contracts_view = Contracts.as_view("contracts")

associated_companies_views = (
	("/v1/internship_contracts/contracts", contracts_view, ["GET", "POST"]),
)

internship_contracts_blueprint = Blueprint("internship_contracts", __name__)

for uri, view_func, methods in internship_contracts_views:
	internship_contracts_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)