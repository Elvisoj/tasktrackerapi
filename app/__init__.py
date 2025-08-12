from flask import Flask
from .extensions import db, migrate, jwt
from .config import Config
from flasgger import Swagger

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # include all routes
            "model_filter": lambda tag: True,  # include all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
    # "openapi": "3.0.2",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Tracker API",
        "description": "API for managing users, projects, tasks, and summaries.",
        "version": "1.0.0",
        "contact": {
            "name": "EOJ",
            "url": "https://github.com/Elvisoj",
            "email": "ighoelvis8@email.com"
        }
    },
    "basePath": "/api",
    "schemes": ["http", "https"],
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Swagger Setup
    swagger = Swagger(app, config=swagger_config, template=swagger_template)

    # Import models so Alembic can detect them
    from .models.user import User

    # Register Blueprint
    from .routes.auth import auth_bp
    from app.routes.project import project_bp
    from app.routes.task import task_bp
    from app.routes.summary import summary_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(summary_bp)

    return app