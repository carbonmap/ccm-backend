from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import os
from .models import ReportingEntity, EntityToSubentity, UserToEntity, EntityProperty
import dataclasses

app_dir = os.path.dirname(os.path.abspath(__file__))

map = Blueprint("map", __name__)

@map.route("/map_view")
def map_view():
    # We want to reveal all entities which have primary_display = True
    # AND any subentities which belong to the list of top level entities in
    # the url 

    # This gets the list of entities from the url:
    list_of_expanded_entities = []
    if request.args.get("reveal[]") is not None:
        list_of_expanded_entities = request.args.to_dict(flat=False)['reveal[]']

    # Get all primary entities
    primary_entities = ReportingEntity.query.filter_by(primary_display=1).all()
    
    # Get subentities of entities passed in params
    displayed_subentities = []
    for entity_id in list_of_expanded_entities:
        subentities = EntityToSubentity.query.filter_by(entity_id=entity_id).all()
        print(len(subentities))
        for subentity in subentities:
            displayed_subentities.append(ReportingEntity.query.filter_by(id=subentity.subentity_id).all())
    return jsonify(primary_entities + displayed_subentities)


@map.route("/popup_options")
def popup_options():

    # TODO: 050920
    # Refering to map.cambridgecarbonmap.org: when a user hovers over any entity (primary or sub)
    # They have a popup with the name on it. When they click on it, the popup stays in place (i.e. doesn't follow mouse).
    # If they click on a primary entity, it also explodes, but if it's a subentity that's it

    # The initial popup is easy to do on the front end - it's just a name
    # The `permanent` popup will have to dig into the database.
    # It will display: college's human name (function 6), the college metadata (function 4),
    # and, whether or not the current user can edit the entity (later on we will a button to do this)

    # For this last bit, you will have to check if the id is in the list returned by profile.my_entities

    # The popup will send a request to a route of url .../popup_options?entity_id=uk.ac.cam.kings
    # Therefore, you can get the relevant entity with:
    entity_id = request.args.get("entity_id")

    # Get entity and convert to object
    entity = dataclasses.asdict(ReportingEntity.query.filter_by(id=entity_id).first())
    # Get all entity properties
    entity_property_list = EntityProperty.query.filter_by(id=entity_id).all()
    editable = False

    if len(UserToEntity.query.filter_by(user_id=current_user.id, entity_id=entity_id).all()) > 0:
        editable = True

    entity['properties'] = entity_property_list
    entity['editable'] = editable
    return entity
 
@map.route("/mapstart")
def primary_entities():
    entities = []
    for entity in ReportingEntity.query.filter_by(primary_display=1).all():
        entities.append(entity.id)
    return jsonify(entities)

@map.route("/mapchild")
def secondary_entities():
    entities = []
    for entity in ReportingEntity.query.filter_by(primary_display=0).all():
        entities.append(entity.id)
    return jsonify(entities)
