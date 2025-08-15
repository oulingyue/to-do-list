from flask import request, jsonify
from flask_cors import CORS
from config import app
from Task import Task

todos = []

@app.route('/', methods=['GET'])
def get_welcome():
    return "welcome to the To-Do List API!"

@app.route("/tasks", methods=['GET'])
def get_tasks():
    return jsonify([task.to_dict() for task in todos]), 200

@app.route("/tasks", methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_task = Task(content=data['content'])
    todos.append(new_task)
    return jsonify(new_task.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    for task in todos:
        if task.id == task_id:
            task.toggle_task()
            return jsonify(task.to_dict()), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    for task in todos:
        if task.id == task_id:
            todos.remove(task)
            return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
