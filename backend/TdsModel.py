"""
To-Do list Project

This is the model for a single to-do list.
"""
from Task import Task

class ToDoListModel:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task_title):
        task = Task(task_title)
        if task_title not in self.tasks:
            self.tasks[task_title] = task
        else:
            self.tasks[task_title].append(task)

    def get_tasks(self):
        return self.tasks

    def delete_task(self, task):
        if task.get_title in self.tasks:
            self.tasks[task.get_title].remove(task)
        else:
            return
