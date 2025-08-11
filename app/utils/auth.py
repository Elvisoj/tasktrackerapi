from app.models.user import User
from app.extensions import db

def create_user(firstname, lastname, username, email, password):
    user = User(firstname=firstname, lastname=lastname, username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def find_user_by_email(email):
    return User.query.filter_by(email=email).first()