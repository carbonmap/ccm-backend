from flask import Blueprint, render_template
from flask_login import login_required, current_user
from data_access_functions import user_map_dashboard

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    user_email_domain = \
        user_map_dashboard.get_user_email_domain(current_user.email)
    user_subentities = user_map_dashboard.get_subentities(user_email_domain)
    return render_template("profile.html", name=current_user.name,
                          subentities=user_subentities)