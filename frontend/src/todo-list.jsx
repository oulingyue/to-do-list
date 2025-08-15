import React, {useState} from "react";

function TodoList(){
    const [tasks, setTasks] = useState([]);
    const [newTask, setNewTask] = useState("");
  return (
    <div class = "todo-list-container">
        <div className="todo-list">
            <h2>⋆𐙚₊˚⊹♡ Grace's To-Do List 𐙚₊˚⊹♡</h2>
                <div className="row">
                    <input type="text" id="input-box" placeholder="enter new task.."/>
                    <button>add</button>
                </div>
            <ul id="task-list-container">
                {tasks.map((tasks) => (
                <li key={tasks.id}>
                    {tasks.title}
                    </li>
                ))}
            </ul>
            </div>
  </div>);
}

export default TodoList;