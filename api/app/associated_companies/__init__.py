from flask import Blueprint
from .views import (Companies)


companies_view = Companies.as_view("companies")

associated_companies_views = (
	("/v1/associated_companies/companies", companies_view, ["GET", "POST"]),
	("/v1/associated_companies/companies/<company_id>", companies_view, ["GET"]),

)

associated_companies_blueprint = Blueprint("associated_companies", __name__)

for uri, view_func, methods in associated_companies_views:
	associated_companies_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)