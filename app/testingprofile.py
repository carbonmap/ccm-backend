import sqlite3
from admin import sqliteExecute


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

def my_entities():
    user_id = "john_id"
    user_entities_db = sqliteExecute("db.sqlite", "SELECT entity_id FROM user_to_entity WHERE user_id=?", (user_id, ))
    user_entities = []
    for tup in user_entities_db:
        user_entities.append(tup[0]) 

    return user_entities


def entity_name(id):
    entity_name_db = sqliteExecute("db.sqlite", "SELECT name FROM reporting_entity WHERE id=?", (id, ))
    entity_name = (entity_name_db[0])[0]

    return entity_name


def parent_entity(id):
    parent_entity_db = sqliteExecute("db.sqlite", "SELECT entity_id FROM entity_to_subentity WHERE subentity_id=?", (id, ))
    if len(parent_entity_db) != 0:
        parent_entity = (parent_entity_db[0])[0]
    else:
        parent_entity = "null"

    return parent_entity

def properties(id):
    properties = {}
    properties_db = sqliteExecute("db.sqlite", "SELECT property,numb_value FROM entity_property WHERE is_numeric=1 AND id=? UNION SELECT property,str_value FROM entity_property WHERE is_numeric=0 AND id=?", (id, id, ))
    for tup in properties_db:
        properties[tup[0]] = tup[1]

    return properties


def entities_full_info():
    ids = my_entities()
    full_info = []
    for id in ids:
        info = {}
        info['name'] = entity_name(id)
        info['id'] = id
        info['joined'] = None
        info['latest_data'] = None
        info['parent_entity'] = parent_entity(id)
        info['properties'] = properties(id)
        full_info.append(info)

    return full_info

print(my_entities())
print(entities_full_info())