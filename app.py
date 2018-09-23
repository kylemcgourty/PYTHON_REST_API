from flask import Flask
from flask import request
from flask import abort, jsonify
import sqlite3
import uuid

app = Flask(__name__)

conn = sqlite3.connect("DFS.db")

cursor = conn.cursor()

dropTableStatement = "DROP TABLE LISTS"

cursor.execute(dropTableStatement)

dropTableStatement = "DROP TABLE TASKS"

cursor.execute(dropTableStatement)

conn.execute('''CREATE TABLE IF NOT EXISTS LISTS 
(ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
DESCRIPTION TEXT NOT NULL);
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS TASKS
(ID INT NOT NULL,
NAME TEXT NOT NULL,
COMPLETED INT NOT NULL,
LISTID INT NOT NULL,
PRIMARY KEY(ID, LISTID),
FOREIGN KEY(LISTID) REFERENCES LISTS(ID));
''')


class Lists:
    def __init__(self):
        self.ListID = 0
        self.taskIDs = {}
    def create_id(self):
        self.ListID += 1
        self.taskIDs[str(self.ListID)] = 0
        return self.ListID
    def create_task_id(self, list_id):
        list_id = str(list_id)
        self.taskIDs[list_id] += 1
        return self.taskIDs[list_id]

# class Lists:
#
#     def create_id(self):
#         return uuid.uuid4()



ListManagement = Lists()



@app.route('/lists', methods=['POST'])
def create_list():

    if not request.json:
        abort(400)
    list = {
        'name': request.json['name'],
        'description': request.json['description'],
        'id': ListManagement.create_id(),
        "tasks": request.json["tasks"]
    }
    conn = sqlite3.connect("DFS.db")
    c = conn.cursor()

    """insert new list"""

    print('value to be inserted', list['id'], list['name'], list['description'])
    conn.execute("INSERT INTO LISTS(ID, NAME, DESCRIPTION) VALUES (?, ?, ?)",
                 (str(list['id']), list['name'], list['description']));

    for task in list["tasks"]:
        task["id"] = ListManagement.create_task_id(list['id'])
        task["list_id"] = list["id"]

    """insert multiple tasks"""
    conn.executemany('INSERT INTO TASKS(ID, NAME, COMPLETED, LISTID) VALUES (?, ?, ?, ?)', [(task['id'], task['name'], task['completed'], task['list_id']) for task in list["tasks"]]);
    conn.commit()
    return jsonify(list), 201




@app.route('/lists', methods=['GET'])
def return_list():

    lists = []
    conn = sqlite3.connect("DFS.db")
    cursor = conn.execute("SELECT * FROM LISTS")
    for main_list in cursor:
        main_list_organizer = {"id": main_list[0], "name": main_list[1], "description": main_list[2], "tasks":  list()}
        lists.append(main_list_organizer)

    cursor = conn.execute("SELECT * FROM TASKS")
    for task in cursor:
        task_organizer = {"id": task[0], "name": task[1], "completed": task[2]}
        lists[task[3]-1]["tasks"].append(task_organizer)
    return jsonify(lists)


@app.route('/list/<int:list_id>', methods=['GET'])
def get_single_list(list_id):
    lists = []
    conn = sqlite3.connect("DFS.db")
    cursor = conn.execute("SELECT * FROM LISTS WHERE ID = ?", (list_id,))
    for main_list in cursor:
        main_list_organizer = {"id": main_list[0], "name": main_list[1], "description": main_list[2], "tasks": list()}
        lists.append(main_list_organizer)

    cursor = conn.execute("SELECT * FROM TASKS WHERE LISTID = ?", (list_id,))
    for task in cursor:
        task_organizer = {"id": task[0], "name": task[1], "completed": task[2]}
        lists[0]["tasks"].append(task_organizer)
    return jsonify(lists)


@app.route('/list/<int:list_id>/task', methods=['POST'])
def add_task(list_id):

    if not request.json:
        abort(400)
    task = {
        'name': request.json['name'],
        'completed': request.json['completed'],
        'id': ListManagement.create_task_id(list_id),
        "list_id": list_id
    }
    conn = sqlite3.connect("DFS.db")
    c = conn.cursor()
    conn.execute("INSERT INTO TASKS(ID, NAME, COMPLETED, LISTID) VALUES (?, ?, ?, ?)",
                 (task['id'], task['name'], task['completed'], task['list_id']));
    conn.commit()
    return jsonify(task), 201


@app.route('/list/<int:list_id>/task/<int:task_id>/complete', methods=['POST'])
def set_to_complete(list_id, task_id):

    conn = sqlite3.connect("DFS.db")
    c = conn.cursor()
    conn.execute("UPDATE TASKS SET COMPLETED = ? WHERE ID = ? AND LISTID = ?", (1, task_id, list_id));
    conn.commit()
    return jsonify({"Status": "Completed"}), 200

if __name__ == '__main__':
    app.run()
