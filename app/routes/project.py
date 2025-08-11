from flask import Blueprint, jsonify, request
from app.models.project import Project
from app.extensions import db
from flask_jwt_extended import jwt_required
from app.utils.decorators import jwt_user_only

project_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@project_bp.route('/', methods=['GET'])
@jwt_required()
@jwt_user_only
def get_project(user_id):
    projects = Project.query.filter_by(user_id=user_id, is_deleted=False).all()
    result = [{'id': p.id, 'title':p.title, 'description': p.description} for p in projects]
    return jsonify(result), 200

@project_bp.route('/', methods=['POST'])
@jwt_required()
@jwt_user_only
def create_project(user_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'error': 'Title is required'})
    
    project = Project(user_id=user_id, title=title, description=description)
    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Project Created', 'id': project.id}), 201

@project_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
@jwt_user_only
def update_project(user_id, project_id):
    project = Project.query.filter_by(id=project_id, user_id=user_id, is_deleted=False).first()
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    project.title =data.get("title", project.title)
    project.description = data.get("description", project.description)
    
    db.session.commit()

    return jsonify({'message': 'Project Updated'}), 200


@project_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
@jwt_user_only
def delete_project(user_id, project_id):
    project = Project.query.filter_by(id=project_id, user_id=user_id, is_deleted=False).first()
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Project soft-deleted'}), 200
