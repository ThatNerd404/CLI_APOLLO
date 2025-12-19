import json
import mysql.connector
from mysql.connector import errorcode

# TODO: create table with conversation id or name, the conversation, the timestamp of when it was saved and other metadata like length, model used,etc
# TODO: add basic error handling to worker
# TODO: go over notes on SQL

class MySql_Worker():
    def __init__(self, host, user, password, port, database):
        self.mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            port= port,
            database= database
)
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        if tables == []:
            self.cursor.execute("""CREATE TABLE Conversations (
                Conversation_ID INT NOT NULL AUTO_INCREMENT,
                Conversation JSON NOT NULL,
                Model VARCHAR(255) NOT NULL,
                Timestamp TIMESTAMP NOT NULL,
                PRIMARY KEY (Conversation_ID)
                );""")
            print("new tables created bitch!")

    def Execute_Command(self, command):

        try:

            self.cursor.execute(command)
            result = self.cursor.fetchall()
            return result

        except mysql.connector.Error as e:
            print(f"bro we ran into an error {e}\n Error number: {e.errno}")

        except Exeception as e:
            raise Exception(f"Unexpected error occured: {e}")

    def Close_Database(self):
        self.mydb.close()

if __name__ == "__main__":
    msw = MySql_Worker(host="100.111.62.92", user="root", password = "Secret_PW", port =8000, database="Conversation_Storage")
    print(msw.Execute_Command("SHOW TABLES"))
    print(msw.Execute_Command("DESCRIBE Conversations"))
