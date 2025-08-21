import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [tasks, setTasks] = useState([]);
      const [newTask, setNewTask] = useState("");
  
      useEffect(() => {
          fetchTasks()
      }, []);
  
      const fetchTasks = async () => {
          const response = await fetch("http://127.0.0.1:5000/tasks", { method: "GET" });
          const data = await response.json();
          setTasks(data)
          console.log(data)
      }
  
      const updateTask = async (id) => {
          const options = { 
              method: "PUT" 
          }
          try {
              const response = await fetch(`http://127.0.0.1:5000/tasks/${id}`, options)
              if (response.status == 200) {
                  fetchTasks()
              }
              else {
                  console.error("failed to update task")
              }
          } catch (error) {
              alert(error)
          }
      }
  
      const deleteTask = async (id) => {
          try {
              const options = {
                  method: "DELETE"
              }
              const response = await fetch(`http://127.0.0.1:5000/tasks/${id}`, options)
              if (response.status == 200) {
                  fetchTasks()
              } else {
                  console.error("failed to delete dask")
              }
          }
          catch (error) {
              alert(error)
          }
  
      }
  
      const addTask = async (e) => {
          e.preventDefault();
          if (!newTask.trim()) {
              alert("oops- you just entered an empty to-do... What do you want to do? nothing!? ");
              return;
          }
  
          const data = { content: newTask };
          const url = "http://127.0.0.1:5000/tasks";
          const options = {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(data)
          };
          const response = await fetch(url, options);
          if (response.status !== 201 && response.status !== 200) {
              const data = await response.json();
              alert(data.message || "Failed to add task");
              return;
          }
          fetchTasks()
      }
  
      return (
          <div className="todo-list-container">
              <div className="todo-list">
                  <h2>to-do list:</h2>
                  <div className="add-task-section">
                      <input type="text"
                          id="input-box"
                          value={newTask}
                          onChange={(e) => setNewTask(e.target.value)}
                          placeholder="enter new task.."
                      />
                      <button onClick={addTask}>add</button>
                  </div>
                  <ul id="task-list-container">
                      {tasks.map((task) => (
                          <li key={task.id}>
                              <span id = "update" onClick={() => updateTask(task.id)}
                                  style={{ textDecoration: task.completed ? "line-through" : "none", cursor: "pointer" }}
                              >{task.content}</span>
                              <span id="delete" onClick={() => deleteTask(task.id)}>&times;</span>
  
                          </li>
                      ))}
                  </ul>
              </div>
          </div>)
  }

export default App;
