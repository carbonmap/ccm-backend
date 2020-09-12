import sqlite3

## Function 1: SELECT id FROM reporting_entity WHERE primary_display=1;
## Function 2: SELECT subentity_id FROM entity_to_subentity WHERE entity_id=entity_id_variable;
## Function 3: SELECT entity_id,role FROM user_to_entity WHERE user_id=user_id_variable;
## Function 4: SELECT numb_value FROM entity_property WHERE is_numeric=1 AND id=id_variable;
##             SELECT string_value FROM entity_property WHERE is_numeric=0 AND id=id_variable;
## Function 5: ? this is a check to see if a user is a superuser
## Function 6: SELECT name FROM reporting_entity WHERE id=id_variable

id = "uk.ac.cam.kings"

conn = sqlite3.connect("db.sqlite")

cursor = conn.cursor()
print("Connected to SQLite")

## Insert function here from list above
cursor.execute("SELECT id FROM reporting_entity WHERE primary_display=1")
print("Instruction executed successfully")

## This produces a list of tuples where tuple elements are row elements
result = cursor.fetchall()
print(result)

## If we just want the first tuple/row of the list:
#print(result[0])

## If we want the first element of each tuple in a list - useful for functions 1,2:
first = []
for tup in result:
    first.append(tup[0])
print(first)    

conn.commit()
conn.close()