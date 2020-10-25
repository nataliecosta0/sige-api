from flask import Blueprint
from .views import (InterByCompanies)


intern_by_companies_view = InterByCompanies.as_view("intern_by_companies")

dashboard_views = (
	("/v1/dashboard/interns_by_companies", intern_by_companies_view, ["GET"]),
)

dashboard_blueprint = Blueprint("dashboard", __name__)

for uri, view_func, methods in dashboard_views:
	dashboard_blueprint.add_url_rule(uri, view_func=view_func, methods=methods)