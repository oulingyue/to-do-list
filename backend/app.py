from flask import Flask, request, jsonify
from flask_cors import CORS
from Task import Task
from TdsModel import ToDoListModel

app = Flask(__name__)
CORS(app) #Allow requests from react

# in-memory "database"
# task attributes: id, title, completed, created at, due date
tasks = ToDoListModel()
# task1 = Task("Task 1")
# tasks.add_task(task1)


@app.route('/', methods=['GET'])
def get_check():
    return jsonify(tasks.get_tasks())

@app.route("/tasks", methods=['GET'])
def get_tasks(): #code for application
    return jsonify(tasks.get_tasks())

@app.route("/tasks", methods=['POST'])
def add_task():
    global tasks
    data = request.get_json()
    task = Task(data['title'])
    tasks.add_task(task)
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_title):
    for task in tasks.get_tasks():
        if task.get_title == task_title:
            task["completed"] = not task["completed"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_title):
    global tasks
    ## tasks = [t for t in tasks if t["id"] != task_id]
    new_tasks = ToDoListModel()
    for task in tasks.get_tasks():
        if task.title != task.get_title():
            new_tasks.add_task(task)
    tasks = new_tasks
    return jsonify({"result": True})


if __name__ == '__main__':
    app.run(debug=True)
