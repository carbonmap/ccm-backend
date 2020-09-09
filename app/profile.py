from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import ReportingEntity, EntityToSubentity, UserToEntity

from .admin import sqliteExecute
from . import db


profile = Blueprint("profile", __name__)


@profile.route("/my_entities")
@login_required
def my_entities():
    user_id = current_user.id

    # TODO: 050920
    # Make a request to database
    # Return all entities in the table `user_to_entity` where the `user_id` is the user_id (function 3)
    # Return a list of just the user's entities in this form:

    # [
    #     ("uk.ac.cam.kings", "metadata"),
    #     ("uk.ac.cam.kings.k1", "metadata"),
    #     ("uk.ac.cam.kings.k2", "emissions"),
    #     ("uk.ac.cam.kings.k3", "emissions"),
    # ]

    # This will be used by both the map entity dashboard, and the popup function (popup_options)
    ### Function 3
    user_entities = sqliteExecute(db, "SELECT entity_id,role FROM user_to_entity WHERE user_id = %s'", (user_id, ))
    return user_entities


@profile.route("/add_entity")
def add_entity():
    # TODO: 050920
    # Make this template (quick job, since it's just a html prototype)
    # Set up another form, like with registration, but with the options:
    # Entity human name
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

    human_name = request.form.get("human_name") # String from textfield
    is_sub = request.form.get("is_sub") # Boolean from the checkbox
    new_id = request.form.get("new_id") # String from textfield
    location = request.form.get("location") # String from textfield

    # All of these are required, so let's flash when one isn't given
    if not all([human_name, is_sub, new_id, location]):
        flash("Please fill in form properly")
        return redirect(url_for("profile.add_entity"))

    if is_sub:
        primary_id = request.form.get("primary_id") # Selection from dropdown
        primary = False
        entity_id = ".".join([primary_id, new_id])
    else:
        primary = True
        entity_id = new_id

    new_entity = ReportingEntity(
        id = entity_id,
        name = human_name,
        primary = primary,
        status = "accepted", # Assume for now
        geohash = location,
    )
    # Make committing a bulk job somehow?
    db.session.add(new_entity)
    db.session.commit()

    new_entity_for_user = UserToEntity(
        user_id = current_user.id,
        entity_id = entity_id
    )
    db.session.add(new_entity_for_user)
    db.session.commit()

    if is_sub:
        new_subentity_for_entity = EntityToSubentity(
            entity_id = primary_id,
            subentity_id = entity_id
        )
        db.session.add(new_subentity_for_entity)
        db.session.commit()

    # What else is required?
    pass


@profile.route("/edit_entity_metadata", methods=["POST"])
@login_required
def edit_entity_metadata():
    # Leave for now, as it requires dynamic form building which we need the angular app for
    pass
