from flask import Blueprint, jsonify


home_bp = Blueprint('homepage', __name__, url_prefix='')

@home_bp.route("/")
def home():
    return jsonify({'message': 'Welcome to the to Tracker Api!', 'doc': 'do vist /docs for more info'}), 200