from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile = Blueprint("profile", __name__)


@profile.route("/my_entities")
@login_required
def my_entities():
    user_id = current_user.id

    # TODO: 050920
    # Make a request to database
    # Return all entities in the table `user_to_entity` where the `user_id` is the user_id (function 3)
    # Return a list of just the user's entities in this form:
    [
        ("uk.ac.cam.kings", "metadata"),
        ("uk.ac.cam.kings.k1", "metadata"),
        ("uk.ac.cam.kings.k2", "emissions"),
        ("uk.ac.cam.kings.k3", "emissions"),
    ]

    # This will be used by both the map entity dashboard, and the popup function (popup_options)


@auth.route("/add_entity")
def add_entity():
    # TODO: 050920
    # Make this template (quick job, since it's just a html prototype)
    # Set up another form, like with registration, but with the options:
    # Checkbox: is this a subentity?
    # Dropdown: If it is a subentity, what primary entity is it related to? Query my_entities to get a list of entities allowed
    # Textfield: What is its id? (assume users know this right now)
    # Geohash (entered in for now, in the next version this will be a point selection on the map)

    # If it is a subentity, the final id is actually entity_id.id, otherwise it's just id

    return render_template("add_entity.html")


@profile.route("/add_entity", methods=["POST"])
@login_required
def add_entity_post():

    # TODO: 050920

    # Receive the form above

    # Enter all the right entity fields into reporting_entity (keep status as "accepted" for now, and keep OSM ID null)
    # If new entity is a subentity, enter the right row values into entity_to_subentity table
    # Similarily add a row to use_to_entity

    # Ignore all the other tables for now
    pass


@profile.route("/edit_entity_metadata", methods=["POST"])
@login_required
def edit_entity_metadata():
    # Leave for now, as it requires dynamic form building which we need the angular app for
    pass
