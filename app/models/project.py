from app.extensions import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref='projects')


# {
#     'firstname': 'Gina',
#     'lastname': 'Jonathan',
#     'username': 'gina',
#     'email': 'gina@gmail.com',
#     'password': '0000',
# }
# http://127.0.0.1:5000/api/auth/register
# http://127.0.0.1:5000/api/projects
# http://127.0.0.1:5000/api/projects/3
# {
#     'title': 'Task Tracker APP',
#     'description': 'i am told to create a task tracker app',
# }