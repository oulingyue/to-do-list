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
    json_tasks = list(map(lambda task:task.to_json(), tasks))
    return jsonify({"tasks": json_tasks})


@app.route("/tasks", methods=['POST'])
def add_task():
    content = request.json.get("content")
    if not content:
        return jsonify({"error": "content is required"}), 400
    new_contact = Task(content=content);
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

    task.completed = not task.completed
    db.session.commit()
    return jsonify({"message": "Task updated successfully"}), 200

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
