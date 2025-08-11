from app.extensions import db
from datetime import datetime


class TaskActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    task = db.relationship('Task', backref='logs')