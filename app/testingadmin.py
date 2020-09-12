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
print(result[0])

conn.commit()
conn.close()