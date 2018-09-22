from flask import Flask
from flask import request
from flask import abort, jsonify
import sqlite3


app = Flask(__name__)

conn = sqlite3.connect("DFS.db")

cursor = conn.cursor()

dropTableStatement = "DROP TABLE LISTS"

cursor.execute(dropTableStatement)

dropTableStatement = "DROP TABLE TODOS"

cursor.execute(dropTableStatement)

conn.execute('''CREATE TABLE IF NOT EXISTS LISTS 
(ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
DESCRIPTION TEXT NOT NULL);
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS TODOS
(ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
COMPLETED INT NOT NULL,
LISTID INT NOT NULL,
FOREIGN KEY(LISTID) REFERENCES LISTS(ID));
''')

print("Table created succesfuly")

# conn.execute("INSERT INTO KYLE(ID, NAME) VALUES (11, 'DR. REDWOOD')");
#
# conn.commit()

print("Record successfully inserted")

class Lists:
    def __init__(self):
        self.ListID = 0
    def create_id(self):
        self.ListID += 1
        return self.ListID

ListManagement = Lists()

# @app.route('/')
# def hello_world():
#     conn = sqlite3.connect("DFS.db")
#     cursor = conn.execute("SELECT ID, NAME FROM KYLE WHERE ID = 11")
#     for individual in cursor:
#         string = "KYLES STATS:\n" + str(individual[0]) + "\n" + individual[1]
#     return string

@app.route('/lists', methods=['POST'])
def create_list():

    if not request.json:
        abort(400)
    list = {
        'name': request.json['name'],
        'description': request.json['description'],
        'id': ListManagement.create_id()
    }
    conn = sqlite3.connect("DFS.db")
    c = conn.cursor()
    conn.execute("INSERT INTO LISTS(ID, NAME, DESCRIPTION) VALUES (?, ?, ?)",
                 (list['id'], list['name'], list['description']));
    conn.commit()
    return jsonify(list), 201




@app.route('/lists', methods=['GET'])
def return_list():

    lists = []
    conn = sqlite3.connect("DFS.db")
    cursor = conn.execute("SELECT * FROM LISTS")
    for list in cursor:
        list_organizer = {"id": list[0], "name":list[1], "description": list[2]}
        lists.append(list_organizer)
    return jsonify(lists)



if __name__ == '__main__':
    app.run()
