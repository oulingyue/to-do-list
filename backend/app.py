import mysql.connector
import os
from flask import request, jsonify
from flask_cors import CORS
from config import app
from Task import Task
from dotenv import load_dotenv

load_dotenv()

# connecting to db
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1103",
        db="testdatabase"
    )
    print("connection successful")

except mysql.connector.Error as e:
    print(f"fail to connect: {e}")

# general query commands for mysql

def execute_qry(sql_cmd, params):
    cur = db.cursor(dictionary=True)
    try:
        cur.excecute(sql_cmd, params)
        if sql_cmd.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            db.commit()
            print("Changes committed to the database.")
            return cur.lastrowid if cur.lastrowid else None
        else:
                result = cur.fetchall()
                return result
    except mysql.connector.error as e:
        db.rollback()
        print(f"failed to query: {e}")
    finally: 
        cur.close()

def insert_into_table(table_name:str, column1, column2, value1, value2):
    sql_cmd =f"INSERT INTO {table_name} ({column1}, {column2}) values (%s,%s);"
    execute_qry(sql_cmd, (value1,value2))
    print("insert success")

def get_all_tasks():
    sql_cmd = f"SELECT * FROM task;"
    results = execute_qry(sql_cmd, ())
    return results if results else None

def get_task_by_id(task_id: str):
    sql_cmd = f"SELECT * FROM task WHERE id = %s"
    results = execute_qry(sql_cmd,())
    return results[0] if results else None

def delete_task_by_id(task_id: str):
    sql_cmd = f"DELETE"
def toggle_task_by_id(task_id:str):
    pass

# ------- api with endpoints ----------- #

@app.route('/')
def landing_page():
    return "welcome to the To-Do List API!"

@app.route("/tasks", methods=['GET'])
def get_tasks():
    task_data = get_all_tasks()
    if task_data:
        return jsonify(task_data), 200
    else: 
        return jsonify({"error": "no tasks found."}), 404

@app.route("/tasks", methods=['POST'])
def add_task():
    # requesting from frontend 
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_task = Task(content=data['content'])
    insert_into_table("task", "content", "task_id", new_task.content, new_task.id)
    return jsonify(new_task.to_dict()), 201

@app.route("/tasks/<task_id>", methods=['PUT'])
def update_task(task_id):
    for task in todos:
        if task.id == task_id:
            task.toggle_task()
            return jsonify(task.to_dict()), 200
    return jsonify({"error": "Task not found"}), 404

@app.route( "/tasks/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    for task in todos:
        if task.id == task_id:
            todos.remove(task)
            return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
