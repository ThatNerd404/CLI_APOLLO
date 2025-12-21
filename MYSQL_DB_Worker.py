import json
import mysql.connector
from datetime import datetime
from mysql.connector import errorcode

# TODO: add basic error handling to worker
# TODO: go over notes on SQL
# TODO: to fix everything you fucked over by being lazy remove the execute comamand function and make a function for whatever we want to do you ijiot!
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

    def Insert_Conversation(self, conversation, model):
        now = datetime.now()
        timestamp_str = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        try:
            self.cursor.execute("INSERT INTO Conversations (Conversation, Model, Timestamp) VALUES (%s, %s, %s)", [json.dumps(conversation), model, timestamp_str])
            self.mydb.commit()

        except mysql.connector.Error as e:
            raise Exception(f"bro we ran into an error {e}\n Error number: {e.errno}")

        except Exception as e:
            raise Exception(f"Unexpected error occured: {e}")

    def Show_Table_Info(self):
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            self.cursor.execute("SELECT * FROM Conversations")
            conversation_data = self.cursor.fetchall()
            return tables, conversation_data

        except mysql.connector.Error as e:
            raise Exception(f"bro we ran into an error {e}\n Error number: {e.errno}")

        except Exception as e:
            raise Exception(f"Unexpected error occured: {e}")

    def Clear_Table(self):
        self.cursor.execute("TRUNCATE TABLE Conversations")
        self.mydb.commit()
    def Query_Table(self):
        pass

    def Close_Database(self):
        self.mydb.close()

if __name__ == "__main__":
    msw = MySql_Worker(host="100.111.62.92", user="root", password = "Secret_PW", port =8000, database="Conversation_Storage")
    #msw.Clear_Table()
    print(msw.Show_Table_Info())
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp_str)

