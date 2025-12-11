import json
import mysql.connector

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
        self.mydb.close()
if __name__ == "__main__":
    msw = MySql_Worker()
