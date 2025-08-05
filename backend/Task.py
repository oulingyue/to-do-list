from config import db
"""
to-do list project
This file contains the task class that represents
individual to-do task s in a to-do list.
"""

class Task(db.Model):
    """
    this class represents an individual to-do task.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "user": self.user,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }
    
        