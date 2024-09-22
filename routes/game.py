from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import MathProblem, UserProgress
from services.openai_service import generate_math_problem
import logging

bp = Blueprint('game', __name__)

@bp.route('/play')
@login_required
def play():
    logging.debug(f"User {current_user.username} accessed /play route")
    return render_template('game.html')

@bp.route('/get_problem', methods=['POST'])
@login_required
def get_problem():
    difficulty = request.json.get('difficulty', 1)
    problem = generate_math_problem(difficulty)
    
    new_problem = MathProblem(
        question=problem['question'],
        answer=problem['answer'],
        difficulty=difficulty,
        explanation=problem['explanation']
    )
    db.session.add(new_problem)
    db.session.commit()
    
    return jsonify({
        'id': new_problem.id,
        'text_question': problem['question'],
        'numerical_question': problem['question']  # For now, we'll use the same question for both
    })

@bp.route('/check_answer', methods=['POST'])
@login_required
def check_answer():
    problem_id = request.json.get('problem_id')
    user_answer = request.json.get('answer')
    
    problem = MathProblem.query.get(problem_id)
    
    # Convert both answers to integers for comparison
    try:
        user_answer_int = int(user_answer)
        correct_answer_int = int(problem.answer)
        is_correct = user_answer_int == correct_answer_int
    except ValueError:
        # If conversion fails, fall back to string comparison
        is_correct = str(user_answer).strip() == str(problem.answer).strip()
    
    progress = UserProgress(
        user_id=current_user.id,
        problem_id=problem_id,
        is_correct=is_correct
    )
    db.session.add(progress)
    
    if is_correct:
        current_user.score += problem.difficulty
    
    db.session.commit()
    
    return jsonify({
        'correct': is_correct,
        'explanation': problem.explanation,
        'score': current_user.score
    })
