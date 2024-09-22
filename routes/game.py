from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import MathProblem, UserProgress
from services.openai_service import generate_math_problem
import logging

bp = Blueprint('game', __name__)

@bp.route('/play')
def play():
    logging.debug(f"User accessed /play route")
    return render_template('game.html')

@bp.route('/get_problem', methods=['POST'])
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
        'question': problem['question']
    })

@bp.route('/check_answer', methods=['POST'])
def check_answer():
    problem_id = request.json.get('problem_id')
    user_answer = request.json.get('answer')
    
    problem = MathProblem.query.get(problem_id)
    
    try:
        user_answer_int = int(user_answer)
        correct_answer_int = int(problem.answer)
        is_correct = user_answer_int == correct_answer_int
    except ValueError:
        is_correct = str(user_answer).strip() == str(problem.answer).strip()
    
    if current_user.is_authenticated:
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
        'score': current_user.score if current_user.is_authenticated else 0
    })
