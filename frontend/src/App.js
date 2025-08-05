import React, {useState, useEffect, use} from 'react';
import './App.css'
import axios from 'axios';

function App() {

  //data pulled from back end as an array.
  const [tasks, setTasks] = useState ([]);

  //user input of a new task as a string
  const [newTasks, setNewTask] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  //sends GET request to flask in the back end.
  const fetchTasks = async () => {
      const res = await fetch("http://127.0.0.1:5000/tasks");
      const data = await res.json();
      //updates tasks state with response from frontend
      setTasks(data.tasks);
      console.log(data.tasks);
  }

  //Load tasks on page
  useEffect(() => {
    //fetching backend data
    fetchTasks();
  }, [])

  //posts new task to the task array in the back end
  const addTask = async () => {
    await axios.post("http://127.0.0.1:5000/tasks", {title: newTasks});
    setNewTask("");
    await fetchTasks();
  };

  const toggleTask = async (id) =>{
    await axios.put(`http://127.0.0.1:5000/tasks/${id}`);
    await fetchTasks();
  };

  const deleteTask = async (id) => {
    await axios.delete(`http://127.0.0.1:5000/tasks/${id}`);
    await fetchTasks();
  };

  return (
      <div style={{ padding: "50px"}}>
      <h1>Grace's To-Do List</h1>

      <input
        value={newTasks}
        onChange={(e) => setNewTask(e.target.value)}
        placeholder="enter new task.."
        />
      <button onClick={addTask}>add task</button>


      <ul>
        {tasks.map((task)=> (
            <li key={task.title}>
            <span
            style={{
              textDecoration: task.completed ? "line-through" : "none",
              cursor: "pointer",
            }}
            onClick={() => toggleTask(task.title)}
    >
            {task.title}
          </span>

          <button onClick={() => deleteTask(task.title)}>delete task</button>

            </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
