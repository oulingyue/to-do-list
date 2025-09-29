from config import db
import uuid
"""
to-do list project
This file contains the task class that represents
individual to-do task s in a to-do list.
"""

class Task():
    """
    this class represents an individual to-do task.
    """
    # id = db.Column(db.Integer, primary_key=True)
    # content = db.Column(db.String(100), nullable=False)
    # completed = db.Column(db.Boolean, default=False)
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    def __init__(self, content:str, id = str(uuid.uuid4), completed = False):
        self.content = content
        self.completed = False
        self.id = id
        
    def toggle_task(self):
        self.completed = not self.completed

    def to_dict(self):
        """
        Convert the task to a dictionary representation for json formatting.
        """
        return {
            "id": self.id,
            "content": self.content,
            "completed": self.completed,
        }
    
        