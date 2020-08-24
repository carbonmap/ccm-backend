import sqlite3

def updateSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('db.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        cursor.execute("UPDATE user SET admin = 'Y' WHERE id = '2'")
        sqliteConnection.commit()
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

updateSqliteTable()