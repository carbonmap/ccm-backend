import sqlite3

def updateSqliteTable(database, table, email):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        cursor.execute("UPDATE " + table + " SET admin = 'Y' WHERE email = '" + email + "'")
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

updateSqliteTable("db.sqlite", "user", "jsb212@cam.ac.uk")