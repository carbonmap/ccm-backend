import sqlite3

id = "uk.ac.cam.kings"

conn = sqlite3.connect("db.sqlite")

cursor = conn.cursor()
print("Connected to SQLite")

##produces a list of tuples where tuple elements are row elements
cursor.execute("SELECT * FROM reporting_entity")
print("Instruction executed successfully")

result = cursor.fetchall()
print(result)
##if we just want the first tuple/row of the list:
#print(result[0])

##if we want the first element of each tuple in a list
#first = []
#for tup in result:
    #first.append(tup[0])
#print(first)    

conn.commit()
conn.close()