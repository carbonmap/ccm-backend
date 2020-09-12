from admin import sqliteExecute
from . import db

from profile import my_entities

def map_view():
    list_of_expanded_entities = ["uk.ac.cam.kings"]
    # Want this to be a list of strings so for loop below works!!! 

    primary_entities = sqliteExecute("db.sqlite", "SELECT id FROM reporting_entity WHERE primary_display = 1")
    ### Function 1 on database
    return primary_entities

#displayed_subentities = []
#for ent in list_of_expanded_entities:
##displayed_subentities.append(sqliteExecute("db.sqlite", "SELECT subentity_id FROM entity_to_subentity WHERE entity_id={}".format(ent)))
##### Function 2 on database for all relevant entities

### i.e. when the user first enters the map, the will have url .../mapview
### This means displayed_subentities is empty and they only return primary_entities

## Return list of entitiy that combines primary_entities and displayed_subentities
#return primary_entities + displayed_subentities
