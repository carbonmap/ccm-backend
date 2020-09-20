import sqlite3
from admin import sqliteExecute


## Function 1: SELECT id FROM reporting_entity WHERE primary_display=1;
## Function 2: SELECT subentity_id FROM entity_to_subentity WHERE entity_id=entity_id_variable;
## Function 3: SELECT entity_id,role FROM user_to_entity WHERE user_id=user_id_variable;
## Function 4: SELECT numb_value FROM entity_property WHERE is_numeric=1 AND id=id_variable;
##             SELECT string_value FROM entity_property WHERE is_numeric=0 AND id=id_variable;
## Function 5: SELECT id FROM superusers WHERE id=id_variable
## Function 6: SELECT name FROM reporting_entity WHERE id=id_variable

id = "uk.ac.cam.kings"      ## For primary entities, entity_id and id are the same, for non-primary entities the entity_id is that of the primary and the id is that of the individual building
user_id = "john_id"         ## The user that controls the entities


## Use a ? where the variable should be, and then list the variables in a tuple as the 3rd argument of sqliteExecute
answer = sqliteExecute("db.sqlite", "SELECT name FROM reporting_entity WHERE id=?", (id, ))

## This produces a list of tuples where tuple elements are row elements
print(answer)

## If we just want the first tuple/row of the list:
#print(answer[0])

## If we want the first element of each tuple in a list - useful for functions 1,2:
first = []
for tup in answer:
    first.append(tup[0])
print(first)    
