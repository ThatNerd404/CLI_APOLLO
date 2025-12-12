import json
import mysql.connector
from mysql.connector import errorcode

# TODO: create table with conversation id or name, the conversation, the timestamp of when it was saved and other metadata like length, model used,etc
# TODO: add basic error handling to worker

class MySql_Worker():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = "100.111.62.92",
            user = "root",
            password = "Secret_PW",
            port=8000,
            database="Conversation_Storage"
)
        self.cursor = self.mydb.cursor()
        try:
            self.cursor.execute("SHOW DATABASES")
            result = self.cursor.fetchall()
            print(result)

        except mysql.connector.Error as e:
            print(f"bro we ran into an error {e}\n Error number: {e.errno}")

        self.mydb.close()
if __name__ == "__main__":
    msw = MySql_Worker()
