from app.models.log import TaskActionLog
from app.extensions import db

def log_task_action(task_id, action):
    log = TaskActionLog(task_id=task_id, action=action)
    db.session.add(log)