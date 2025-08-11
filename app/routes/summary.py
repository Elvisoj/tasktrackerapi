from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import jwt_user_only
from app.utils.task import get_user_project

summary_bp = Blueprint('summary', __name__, url_prefix='/api')

@summary_bp.route('/projects/<int:project_id>/summary/', methods=['GET'])
@jwt_required()
@jwt_user_only
def project_summary(user_id, project_id):
    project = get_user_project(project_id, user_id)

    if not project:
        return jsonify({'error': 'Project not found'}), 404
    status_count = {'todo': 0, 'in_progress': 0, 'done': 0}

    for task in project.tasks:
        if task.status in status_count:
            status_count[task.status] += 1
    return jsonify({'project_id': project_id, 'summary': status_count}), 200