import os
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from .models import ReportingEntity, EntityToSubentity, UserToEntity

profile = Blueprint("profile", __name__)
app_dir = os.path.dirname(os.path.abspath(__file__))

# Final format
# [
#     {
#         name: "King's College, Cambridge",
#         id: "uk.ac.cam.kings",
#         joined: 1234568,
#         latest_data: 1234568,
#         parent_entity: null,
#         properties: {
#             "Year Established": 1350,
#             "Number of Students": 1500
#         }
#     },
#     {
#         name: "King's College Gardens",
#         id: "uk.ac.cam.kings.gardens",
#         joined: 1234568,
#         latest_data: 1234568,
#         parent_entity: "uk.ac.cam.kings",
#         properties: {
#             "Year Established": 1350,
#             "Number of Employees": 8
#         }
#     },
# ]


#@profile.route("/entities")
#@login_required
#def entities_full_info():
#
#    entites = my_entities()  # Send request/just call to my_entities(), get a list of entity ids


@profile.route("/my_entities")
@login_required
def my_entities():
    user_id = current_user.id
    print('user_id:')
    print(user_id)
    # [
    #     ("uk.ac.cam.kings", "metadata"),
    #     ("uk.ac.cam.kings.k1", "metadata"),
    #     ("uk.ac.cam.kings.k2", "emissions"),
    #     ("uk.ac.cam.kings.k3", "emissions"),
    # ]
    user_entities = UserToEntity.query.filter_by(user_id=user_id).all()
    print('user_entities:')
    print(user_entities)
    #sqliteExecute(
    #    "app/db.sqlite",
    #    "SELECT entity_id,role FROM user_to_entity WHERE user_id=?",
    #    (user_id,),
    #)
    return jsonify(user_entities)

@profile.route("/add_entity")
def add_entity():
    return render_template("add_entity.html")


@profile.route("/add_entity", methods=["POST"])
@login_required
def add_entity_post():

    # These mught be changed
    human_name = request.form.get("human_name")  # String from textfield
    is_sub = request.form.get("is_sub")  # Boolean from the checkbox
    new_id = request.form.get("new_id")  # String from textfield
    location = request.form.get("location")  # String from textfield

    # All of these are required, so let's flash when one isn't given
    if not all([human_name, is_sub, new_id, location]):
        flash("Please fill in form properly")
        return redirect(url_for("profile.add_entity"))

    # Database
    if is_sub:
        primary_id = request.form.get("primary_id")  # Selection from dropdown
        primary = False
        entity_id = ".".join([primary_id, new_id])
    else:
        primary = True
        entity_id = new_id

    new_entity = ReportingEntity(
        id=entity_id,
        name=human_name,
        primary=primary,
        status="submitted",  # Assume for now
        geohash=location,
    )
    # Make committing a bulk job somehow?
    db.session.add(new_entity)
    db.session.commit()

    new_entity_for_user = UserToEntity(user_id=current_user.id, entity_id=entity_id)
    db.session.add(new_entity_for_user)
    db.session.commit()

    if is_sub:
        new_subentity_for_entity = EntityToSubentity(
            entity_id=primary_id, subentity_id=entity_id
        )
        db.session.add(new_subentity_for_entity)
        db.session.commit()

    # Make geojson
    geojson_name = f"{entity_id}.geojson"
    geojson_addr = os.path.join(app_dir, "geojson/not_approved")
    make_fresh_geojson(geojson_addr, entity_id, location)


@profile.route("/edit_entity_metadata", methods=["POST"])
@login_required
def edit_entity_metadata():
    # Leave for now, as it requires dynamic form building which we need the angular app for
    pass
