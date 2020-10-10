from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from .decorators import confirm_required
import json
import os
from .models import ReportingEntity, EntityToSubentity

main = Blueprint("main", __name__)
app_dir = os.path.dirname(os.path.abspath(__file__))
database_dir = os.path.join(app_dir, "db.sqlite")

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/admin")
@login_required
@confirm_required
def admin():
    if current_user.admin == "Y":
        return render_template("admin.html")
    else:
        return render_template("index.html")


def is_sub(entity_id):
    entity = ReportingEntity.query.filter_by(id=entity_id).first()
    if entity:
        return entity.primary_display
    return False

def is_approved(entity_id):
    entity = ReportingEntity.query.filter_by(id=entity_id).first()
    if entity:
        return entity.status == 'accepted'
    return False

def get_geojson_addr(entity_id):
    if is_approved(entity_id):
        root_addr = 'geojson/approved'
    else:
        root_addr = 'geojson/not_approved'

    geojson_name = f"{entity_id}.geojson"
    geojson_path = os.path.join(app_dir, root_addr, geojson_name)

    return geojson_path


def get_primary_entity(subentity_id):
    e_to_s = ReportingEntity.query.filter_by(subentity_id=subentity_id).first()
    if e_to_s:
        return e_to_s.entity_id
    return None

def get_all_subentites(entity_id):
    e_to_s = ReportingEntity.query.filter_by(entity_id=entity_id).all()
    return e_to_s

def read_geojson(geojson_addr):
    with open(geojson_addr, "r") as jfile:
        jdata = json.load(jfile)
    return jdata

def save_geojson(geojson, geojson_addr):
    with open(geojson_addr) as jfile:
        json.dump(geojson, jfile)

def make_fresh_geojson(geojson_addr, entity_id, location):
    fresh_geojson = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "id": entity_id,
            "subentities": []
            },
          "geometry": {
            "type": "MultiPoint",
            "coordinates": [location]
          }
        }
      ]
    }

    with open(geojson_addr) as jfile:
        json.dump(fresh_geojson, jfile)  


def reconfig_geojson_subentities(entity_id):
    geojson_addr = get_geojson_addr(entity_id)

    if is_sub(entity_id):
        primary_entity_id = get_primary_entity(entity_id)
        primary_entity_addr = get_geojson_addr(primary_entity_id)
        primary_entity_geojson = read_geojson(primary_entity_addr)
        primary_entity_geojson["features"][0]["properties"]["subentities"].append(entity_id)
        primary_entity_geojson["features"][0]["properties"]["subentities"] = list(set(primary_entity_geojson["features"][0]["properties"]["subentities"]))
        save_geojson(primary_entity_geojson, primary_entity_addr)

    else:
        subentities = get_all_subentites(entity_id)
        entity_geojson = read_geojson(geojson_addr)
        entity_geojson["features"][0]["properties"]["subentities"] += subentities
        entity_geojson["features"][0]["properties"]["subentities"] = list(set(entity_geojson["features"][0]["properties"]["subentities"]))
        save_geojson(entity_geojson, geojson_addr)

    

@main.route("/populate_database_1234")
def populate_dummy_values():

    monster_query = """

    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('net.theleys', 'The Leys School', TRUE, 'submitted', 'osm', 'cp');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.cai', 'Gonville & Caius College', TRUE, 'submitted', 'osm1', 'cp1');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.dow', 'Downing College', TRUE, 'submitted', 'osm2', 'cp2');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.jesus', 'Jesus College', TRUE, 'submitted', 'osm3', 'cp3');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.a-staircase', 'Kings College a-staircase', FALSE, 'submitted', 'osm4', 'cp4');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.bodleys', 'Kings College bodleys', FALSE, 'submitted', 'osm5', 'cp5');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.cranmer', 'Kings College cranmer', FALSE, 'submitted', 'osm6', 'cp6');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.garden', 'Kings College garden', FALSE, 'submitted', 'osm7', 'cp7');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings', 'Kings College', TRUE, 'submitted', 'osm8', 'cp8');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.grasshopper', 'Kings College grasshopper', FALSE, 'submitted', 'osm9', 'cp9');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.keynes', 'Kings College keynes', FALSE, 'submitted', 'osm10', 'cp10');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.kingsfield', 'Kings College kingsfield', FALSE, 'submitted', 'osm11', 'cp11');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.kingsparade', 'Kings College kingsparade', FALSE, 'submitted', 'osm12', 'cp12');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.market', 'Kings College market', FALSE, 'submitted', 'osm13', 'cp13');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.old-site', 'Kings College old-site', FALSE, 'submitted', 'osm14', 'cp14');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.plodge', 'Kings College plodge', FALSE, 'submitted', 'osm15', 'cp15');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.provosts-lodge', 'Kings College provosts-lodge', FALSE, 'submitted', 'osm16', 'cp16');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.spalding', 'Kings College spalding', FALSE, 'submitted', 'osm17', 'cp17');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.st-edwards', 'Kings College st-edwards', FALSE, 'submitted', 'osm18', 'cp18');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.tcr', 'Kings College tcr', FALSE, 'submitted', 'osm19', 'cp19');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.webbs', 'Kings College webbs', FALSE, 'submitted', 'osm20', 'cp20');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.wilkins', 'Kings College wilkins', FALSE, 'submitted', 'osm21', 'cp21');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.queens', 'Queens College', TRUE, 'submitted', 'osm22', 'cp22');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.st-edmunds', 'St. Edmunds College', TRUE, 'submitted', 'osm23', 'cp23');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.st-edmunds.norfolk-building', 'St. Edmunds College norfolk-building', FALSE, 'submitted', 'osm24', 'cp24');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.st-edmunds.richard-laws', 'St. Edmunds College richard-laws', FALSE, 'submitted', 'osm25', 'cp25');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.st-edmunds.white-cottage', 'St. Edmunds College white-cottage', FALSE, 'submitted', 'osm26', 'cp26');
    INSERT INTO reporting_entity(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.trin', 'Trinity College', TRUE, 'submitted', 'osm27', 'cp27');

    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('net.theleys', 'The Leys School',TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.cai', 'Gonville & Caius College', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.dow', 'Downing College', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.jesus', 'Jesus College', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.a-staircase', 'Kings College a-staircase', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.bodleys', 'Kings College bodleys', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.cranmer', 'Kings College cranmer', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.garden', 'Kings College garden', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings', 'Kings College', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.grasshopper', 'Kings College grasshopper', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.keynes', 'Kings College keynes', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.kingsfield', 'Kings College kingsfield', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.kingsparade', 'Kings College kingsparade', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.market', 'Kings College market', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.old-site', 'Kings College old-site', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.plodge', 'Kings College plodge', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.provosts-lodge', 'Kings College provosts-lodge', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.spalding', 'Kings College spalding', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.st-edwards', 'Kings College st-edwards', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.tcr', 'Kings College tcr', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.webbs', 'Kings College webbs', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.kings.wilkins', 'Kings College wilkins', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.queens', 'Queens College', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.st-edmunds', 'St. Edmunds College', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.st-edmunds.norfolk-building', 'St. Edmunds College norfolk-building', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.st-edmunds.richard-laws', 'St. Edmunds College richard-laws', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.st-edmunds.white-cottage', 'St. Edmunds College white-cottage', TRUE, 4000, NULL);
    INSERT INTO entity_property(id,property,is_numeric,numb_value,str_value) VALUES ('uk.ac.cam.trin', 'Trinity College', TRUE, 4000, NULL);
    
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.a-staircase');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.bodleys');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.cranmer');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.garden');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.grasshopper');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.keynes');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.kingsfield');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.kingsparade');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.market');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.old-site');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.plodge');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.provosts-lodge');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.spalding');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.st-edwards');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.tcr');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.webbs');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.kings', 'uk.ac.cam.kings.wilkins');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.st-edmunds', 'uk.ac.cam.st-edmunds.norfolk-building');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.st-edmunds', 'uk.ac.cam.st-edmunds.richard-laws');
    INSERT INTO entity_to_subentity(entity_id,subentity_id) VALUES ('uk.ac.cam.st-edmunds', 'uk.ac.cam.st-edmunds.white-cottage');

    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('alex_id', 'net.theleys', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('betty_id', 'uk.ac.cam.cai', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('carl_id', 'uk.ac.cam.dow', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('daisy_id', 'uk.ac.cam.jesus', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.a-staircase', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.bodleys', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.cranmer', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.garden', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.grasshopper', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.keynes', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.kingsfield', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.kingsparade', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.market', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.old-site', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.plodge', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.provosts-lodge', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.spalding', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.st-edwards', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.tcr', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.webbs', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id', 'uk.ac.cam.kings.wilkins', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('ellie_id', 'uk.ac.cam.queens', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('fred_id', 'uk.ac.cam.st-edmunds', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('fred_id', 'uk.ac.cam.st-edmunds.norfolk-building', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('fred_id', 'uk.ac.cam.st-edmunds.richard-laws', 'metadata');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('fred_id', 'uk.ac.cam.st-edmunds.white-cottage', 'emission');
    INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('gill_id', 'uk.ac.cam.trin', 'metadata');
    

    """

    queries_list = monster_query.split(";")

    for q in queries_list:
        sqliteExecute(database=database_dir, instruction=q, params=())

    print("wow")

    return "Hi there"
