from flask import request, jsonify
from flask_cors import CORS
from config import app, db
from Task import Task
from TdsModel import ToDoListModel


@app.route('/', methods=['GET'])
def get_check():
    return "welcome to the To-Do List API!"

@app.route("/tasks", methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    json_contacts = list(map(lambda task:task.to_json(), tasks))
    return jsonify({"contacts": json_contacts})


@app.route("/tasks", methods=['POST'])
def add_task():
    title = request.json.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    new_contact = Task(title=title);
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Task created successfully"}), 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    completed = request.json.get("completed")
    if completed is not None:
        task.completed = not task.completed

    db.session.commit()
    return jsonify({"message": "Task updated successfully"}), 200

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
    with app.app_context():
        db.create_all()

    app.run(debug=True)
