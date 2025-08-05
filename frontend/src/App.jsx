import { useEffect, useState } from 'react'
import './App.css'
import TodoList from './todo-list.jsx'

function App() {
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    fetchTasks()
  }, [])
  const fetchTasks = async () => {
    const response = await fetch('http://127.0.0.1:5000/tasks')
    const data = await response.json()
    setTasks(data.tasks)
    console.log(data.tasks)
  }
  return <TodoList tasks={tasks} />
}

export default App;
