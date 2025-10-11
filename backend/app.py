import mysql.connector
import os
from flask import request, jsonify
from flask_cors import CORS
from config import app
from Task import Task
from dotenv import load_dotenv

load_dotenv()

# connecting to db
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1103",
        db="testdatabase"
    )

# ---- general query commands for mysql ---- #

def execute_qry(sql_cmd, params):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql_cmd, params)
        if sql_cmd.strip().upper().startswith(("INSERT")):
            conn.commit()
            print("Insertion committed to the database.")
            return cur.lastrowid if cur.lastrowid else None
        elif sql_cmd.strip().upper().startswith(("UPDATE", "DELETE")):
            conn.commit()
            print("Changes committed to the database.")
            return cur.rowcount if cur.rowcount else None
        else:
                result = cur.fetchall()
                return result
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"failed to query: {e}")
        return None
    finally: 
        cur.close()
        conn.close()

def insert_into_table(table_name:str, column1, column2, value1, value2):
    sql_cmd =f"INSERT INTO {table_name} ({column1}, {column2}) values (%s,%s);"
    execute_qry(sql_cmd, (value1,value2))
    print("insert success")

def get_all_tasks():
    sql_cmd = f"SELECT * FROM task;"
    results = execute_qry(sql_cmd, ())
    return results if results else None

def get_task_by_id(task_id: str):
    sql_cmd = f"SELECT * FROM task WHERE task_id = %s"
    results = execute_qry(sql_cmd,(task_id,))
    return results[0] if results else None

def delete_task_by_id(task_id: str):
    sql_cmd = f"DELETE FROM task WHERE task_id = %s"
    results = execute_qry(sql_cmd, (task_id,))
    if results:
        return {"success": True, 
                "message": "Task deleted.",
                "rows_deleted": results}
    else:
        return {"success": False, 
                "message": "Task not found"}

def toggle_task_by_id(task_id:str):
    sql_cmd =f"UPDATE task SET completed = NOT completed where task_id = %s"
    results = execute_qry(sql_cmd, (task_id,))
    if results:
        return {
            "success": True,
            "message": f"Task {task_id} toggeled sucessfully."
        }
    else: 
        return{
            "success": False,
            "message" : "Task not found or no change made."
        }
    
    

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
    
@app.route("/tasks/<task_id>", methods=['GET'])
def get_tasks_by_id(task_id):
    task_data = get_task_by_id(task_id)
    if task_data:
        return jsonify(task_data), 200
    else: 
        return jsonify({"error": "task not found."}), 404

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
    result = toggle_task_by_id(task_id)
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@app.route( "/tasks/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    result = delete_task_by_id(task_id)
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

if __name__ == '__main__':
    app.run(debug=True)
