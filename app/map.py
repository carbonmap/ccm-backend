from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import json
import sqlite3

from .admin import sqliteExecute
from . import db
from .profile import my_entities



map = Blueprint("map", __name__)


@map.route("/map_view")
def map_view():
    # TODO: 050920
    # User will enter a url that looks like:
    # .../map_view?reveal[]=uk.ac.cam.kings&reveal[]=uk.ac.cam.christs

    # We want to reveal all entities which have primary_display = True (function 1),
    # AND any subentities which belong to the list of top level entities in
    # the url (function 2 for each of the url arguments)

    # This gets the list of entities from the url:
    list_of_expanded_entities = request.args.get("reveal[]")
    # Want this to be a list of strings so for loop below works!!! 
    print(list_of_expanded_entities) 

    primary_entities = sqliteExecute("app/db.sqlite", "SELECT id FROM reporting_entity WHERE primary_display=1", ())
    ### Function 1 on database

    displayed_subentities = []
    for ent in list_of_expanded_entities:
        displayed_subentities.append(sqliteExecute("app/db.sqlite", "SELECT subentity_id FROM entity_to_subentity WHERE entity_id=?", (entity_id, )))
        ### Function 2 on database for all relevant entities

        # i.e. when the user first enters the map, the will have url .../mapview
        # This means displayed_subentities is empty and they only return primary_entities

    # Return list of entitiy that combines primary_entities and displayed_subentities
    return primary_entities + displayed_subentities


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

    ### Function 6?
    entity_name = sqliteExecute("app/db.sqlite", "SELECT name FROM reporting_entity WHERE id=?", (id, ))

    ### Function 4 ...... I'm assuming each sqliteExecute makes a list so I can add the two together to make a bigger list
    entity_meta_data = sqliteExecute("app/db.sqlite", "SELECT numb_value FROM entity_property WHERE is_numeric=1 AND id=?", (id, ))  + sqliteExecute("app/db.sqlite", "SELECT string_value FROM entity_properties WHERE is_numeric=0 AND id=?", (id, ))

    ### Function 3 and 5?
    user_entities = (
        my_entities
    )  ### Send a request to .../my_entities which returns a list of entity ids the user has access to, and their permission to each
    user_permission = None  ### None/"emissions"/"metadata"

    # Return soemthing like this:
    return {
        "entity_name": entity_name,
        "entity_metadata": entity_metadata,
        "user_permission": user_permission,
    }
    # The front end can then receive this and produce a popup with the name and metadata

@map.route("/mapstart", methods=["POST"])
def primary_entities():
    db = "C:/Users/Jeevs/ccm-backend/app/db.sqlite"
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        print("Connected to SQLite")

        cursor.execute("SELECT id FROM reporting_entity WHERE primary_display = 1")
        rows = cursor.fetchall()
        print(rows)
        lst = []
        for row in rows:
            print(row[0])
            lst.append(row[0])
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
        return jsonify(lst)


    #with open("C:/Users/Jeevs/ccm-backend/app/geojson/uk.ac.cam.kings.geojson") as f:
        #status = json.load(f)
    
    #return status

@map.route("/mapchild", methods=["POST"])
def secondary_entities():
    db = "C:/Users/Jeevs/ccm-backend/app/db.sqlite"
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        print("Connected to SQLite")

        cursor.execute("SELECT id FROM reporting_entity WHERE primary_display = 0")
        rows = cursor.fetchall()
        print(rows)
        lst = []
        for row in rows:
            print(row[0])
            lst.append(row[0])
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
        return jsonify(lst)