from app.models.task import Task
from app.models.project import Project
from app.extensions import db

STATUS_FLOW = {
    'todo': ['in_progress'],
    'in_progress': ['done'],
    'done': [],
}

def is_valid_transition(current, new):
    return new in STATUS_FLOW.get(current, [])

def get_user_project(project_id, user_id):
    return Project.query.filter_by(id=project_id, user_id=user_id, is_deleted=False).first()