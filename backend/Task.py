"""
to-do list project
This file contains the task class that represents
individual to-do task s in a to-do list.
"""

class Task:
    """
    this class represents an individual to-do task.
    """
    def __init__(self, title):
        self.owner = None
        self.title = title
        self.completed = False
        self.due_date = None

    def set_owner(self, owner):
        self.owner = owner

    def set_due_date(self, due_date):
        self.due_date = due_date

    def toggle_completed(self):
        self.completed = not self.completed

    def get_task(self):
        return self

    def get_title(self):
        return self.title