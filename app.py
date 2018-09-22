from flask import Flask
import sqlite3


app = Flask(__name__)

conn = sqlite3.connect("DFS.db")


conn.execute('''CREATE TABLE IF NOT EXISTS KYLE 
(ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL);''')

print("Table created succesfuly")

# conn.execute("INSERT INTO KYLE(ID, NAME) VALUES (11, 'DR. REDWOOD')");
#
# conn.commit()

print("Record successfully inserted")

@app.route('/')
def hello_world():
    conn = sqlite3.connect("DFS.db")
    cursor = conn.execute("SELECT ID, NAME FROM KYLE WHERE ID = 11")
    for individual in cursor:
        string = "KYLES STATS:\n" + str(individual[0]) + "\n" + individual[1]
    return string


if __name__ == '__main__':
    app.run()
