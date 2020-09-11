import sqlite3

def updateSqliteTable(database, table, email, flag):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        cursor.execute(
            "UPDATE "
            + table
            + " SET admin = '"
            + flag
            + "' WHERE email = '"
            + email
            + "'"
        )
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def sqliteExecute(database, instruction):
    conn = None
    try:
        conn = sqlite3.connect(database)
        # fetchall() returns a list of tuples, and the second element is redundant,
        # so the lambda below takes only the first element
        conn.row_factory = lambda cursor, row: row[0] 
        cursor = conn.cursor()
        print("Connected to SQLite")
        result = cursor.execute(instruction).fetchall()
        print("Instruction executed successfully")
        conn.commit()
        conn.close()
    
    except sqlite3.Error as error:
        print("Failed to update sqlite database", error)

    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")
            
    return result
    

#Example instructions: 
#
# "CREATE TABLE reporting_entities(id int, Name varchar(32), Prime varchar(32), status varchar(32), osm_id varchar(32), geohash varchar(32))"    
# ----> Creates table called reporting_entities with columns id, Name, Prime, status, osm_id and geohash
#
# "UPDATE user SET admin = 'Y' WHERE email = 'email@email.com'"
# ----> Updates entry in the admin column to the value 'Y' for the row with email 'email@email.com' in the user table