from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import jwt_user_only
from app.utils.task import get_user_project, is_valid_transition
from app.extensions import db
from app.models.task import Task
from app.models.tag import Tag
from app.models.project import Project
from app.utils.logger import log_task_action
from flasgger.utils import swag_from


task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')




@task_bp.route('/', methods=['GET'])
@jwt_required()
@jwt_user_only
def list_task(user_id):
    status = request.args.get('status')
    query = Task.query.join(Project).filter(Project.user_id == user_id, Project.is_deleted == False)

    if status:
        query = query.filter(Task.status == status)
    tasks = query.all()
    result = []
    for task in tasks:
        result.append({
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'tags': [tag.name for tag in task.tags],
        })
    return jsonify(result), 200


@task_bp.route('/', methods=['POST'])
@jwt_required()
@jwt_user_only
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Create a new task',
    'summary': 'Create a task under a given project and dynamically assigns tags.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'project_id': {'type': 'integer'},
                'title': {'type': 'string'},
                'description': {'type': 'string'},
                'tags': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
            },
            'required': ['project_id', 'title']
        }
    }],
    'responses': {
        201: {'description': 'Task Created'},
        400: {'description': 'Validation failed'},
        404: {'description': 'Project not found'},
    }
})
def create_task(user_id):
    data = request.get_json()
    project_id = data.get('project_id')
    title = data.get('title')
    description = data.get('description')
    tag_names = data.get('tags', [])

    project = get_user_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Invalid project'}), 404
    task = Task(title=title, description=description, project_id=project_id)

    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first
        if not tag:
            tag = Tag(name=tag_name).first()
            db.session.add(tag)
        task.tag.append(tag)
    db.session.add(task)
    log_task_action(task_id=task.id, action='created')
    db.session.commit()

    return jsonify({'message': 'Task Created', 'id': task.id}), 201


@task_bp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
@jwt_user_only
def update_task(user_id, id):
    task = Task.query.join(Project).filter(Task.id == id, Project.user_id == user_id, Project.is_deleted == False).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    new_status = data.get('status')

    if new_status and new_status != task.status:
        if task.status == 'done':
            return jsonify({'error': 'Cannot change status after "done"'}), 400
        if not is_valid_transition(task.status, new_status):
            return jsonify({'error': f'Invalid status transition from {task.status} to {new_status}'}), 400
        task.status = new_status
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)

    log_task_action(task_id=task.id, action='updated')
    db.session.commit()
    return jsonify({'message': 'Task updated'}), 200


@task_bp.route('/<int:id>/', methods=['PUT'])
@jwt_required()
@jwt_user_only
def delete_task(user_id, id):
    task = Task.query.join(Project).filter(Task.id == id, Project.user_id == user_id, Project.is_deleted == False).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    log_task_action(task_id=task.id, action='deleted')
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200