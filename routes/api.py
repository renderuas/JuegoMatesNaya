from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import UserProgress

bp = Blueprint('api', __name__)

@bp.route('/api/user_progress')
@login_required
def user_progress():
    progress = UserProgress.query.filter_by(user_id=current_user.id).order_by(UserProgress.timestamp.desc()).limit(10).all()
    return jsonify([
        {
            'problem_id': p.problem_id,
            'is_correct': p.is_correct,
            'timestamp': p.timestamp.isoformat()
        } for p in progress
    ])

@bp.route('/api/leaderboard')
def leaderboard():
    top_users = User.query.order_by(User.score.desc()).limit(10).all()
    return jsonify([
        {
            'username': user.username,
            'score': user.score
        } for user in top_users
    ])
