from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .admin import sqliteExecute
from . import db

from .profile import my_entities

map = Blueprint("map", __name__)


@map.route("/map_view")
def map_view():

    # User will enter a url that looks like:
    # .../map_view?reveal[]=uk.ac.cam.kings&reveal[]=uk.ac.cam.christs

    # We want to reveal all entities which have primary_display = True (function 1),
    # AND any subentities which belong to the list of top level entities in
    # the url (function 2 for each of the url arguments)

    expanded_entities = request.args.get("reveal[]")
    #This is a dictionary where key is reveal[] but key can't be same for both entities?

    primary_entities = sqliteExecute("app/db.sqlite", "SELECT id FROM reporting_entity WHERE primary_display=1", ())
    ### Function 1 on database

    displayed_subentities = []
    for ent in expanded_entities.values():
        displayed_subentities.append(sqliteExecute("app/db.sqlite", "SELECT subentity_id FROM entity_to_subentity WHERE entity_id=?", (ent, )))
        ### Function 2 on database for all relevant entities

    return primary_entities, displayed_subentities


@map.route("/popup_options")
def popup_options():

    # Refering to map.cambridgecarbonmap.org: when a user hovers over any entity (primary or sub)
    # They have a popup with the name on it. When they click on it, the popup stays in place (i.e. doesn't follow mouse).
    # If they click on a primary entity, it also explodes, but if it's a subentity that's it

    # The initial popup is easy to do on the front end - it's just a name
    # The `permanent` popup will have to dig into the database.
    # It will display: college's human name (function 6), the college metadata (function 4),
    # and, whether or not the current user can edit the entity (later on we will a button to do this)

    # For this last bit, you will have to check if the id is in the list returned by profile.my_entities

    # The popup will send a request to a route of url .../popup_options?id=uk.ac.cam.kings
    # Therefore, you can get the relevant entity's id with:
    id = request.args.get("id")

    ### Function 6
    entity_name = sqliteExecute("app/db.sqlite", "SELECT name FROM reporting_entity WHERE id=?", (id, ))

    ### Function 4
    entity_meta_data = sqliteExecute("app/db.sqlite", "SELECT numb_value FROM entity_property WHERE is_numeric=1 AND id=? UNION SELECT str_value FROM entity_property WHERE is_numeric=0 AND id=?", (id, id, ))

    ### Function 3 and 5
    user_entities = (
        my_entities()
    )  ### Send a request to .../my_entities which returns a list of entity ids the user has access to, and their permission to each
    user_permission = None  ### None/"emissions"/"metadata"

    # Return soemthing like this:
    return {
        "entity_name": entity_name,
        "entity_metadata": entity_metadata,
        "user_permission": user_permission,
    }
    # The front end can then receive this and produce a popup with the name and metadata
