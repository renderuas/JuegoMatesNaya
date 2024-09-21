from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User, UserProgress, MathProblem
from app import db
from sqlalchemy import func

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get the current user's progress
    user_progress = UserProgress.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total problems attempted and correct answers
    total_problems = len(user_progress)
    correct_answers = sum(1 for progress in user_progress if progress.is_correct)
    
    # Calculate accuracy
    accuracy = (correct_answers / total_problems * 100) if total_problems > 0 else 0
    
    # Get problem difficulty distribution
    difficulty_distribution = db.session.query(
        MathProblem.difficulty,
        func.count(MathProblem.id)
    ).join(UserProgress).filter(UserProgress.user_id == current_user.id).group_by(MathProblem.difficulty).all()
    
    # Get recent progress (last 10 problems)
    recent_progress = UserProgress.query.filter_by(user_id=current_user.id).order_by(UserProgress.timestamp.desc()).limit(10).all()
    
    return render_template('dashboard.html',
                           total_problems=total_problems,
                           correct_answers=correct_answers,
                           accuracy=accuracy,
                           difficulty_distribution=difficulty_distribution,
                           recent_progress=recent_progress)
