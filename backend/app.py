from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #Allow requests from react

# in-memory "database"
# task attributes: id, title, completed, created at, due date
tasks = []
task_id = 1


@app.route('/', methods=['GET'])
def get_check():
    return "hello world"

@app.route("/tasks", methods=['GET'])
def get_tasks(): #code for application
    return jsonify(tasks)

@app.route("/tasks", methods=['POST'])
def add_task():
    global task_id
    global tasks
    data = request.get_json()
    task = {"id": task_id,
            "title":data["title"],
            "completed": False}
    tasks.append(task)
    task_id = task_id + 1
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    global tasks
    ## tasks = [t for t in tasks if t["id"] != task_id]
    new_tasks = []
    for task in tasks:
        if task["id"] != task_id:
            new_tasks.append(task)
    tasks = new_tasks
    return jsonify({"result": True})


if __name__ == '__main__':
    app.run(debug=True)
