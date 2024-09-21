from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_babel import _
from models import MultiplayerSession, MultiplayerGame, User
from app import db
from services.math_service import generate_math_problem

bp = Blueprint('multiplayer', __name__)

@bp.route('/multiplayer')
@login_required
def multiplayer():
    return render_template('multiplayer.html')

@bp.route('/multiplayer/create_session', methods=['POST'])
@login_required
def create_session():
    new_session = MultiplayerSession(creator_id=current_user.id)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'session_id': new_session.id})

@bp.route('/join_session', methods=['POST'])
@login_required
def join_session():
    session_id = request.json.get('session_id')
    multiplayer_session = MultiplayerSession.query.get(session_id)
    if multiplayer_session and multiplayer_session.player2_id is None:
        multiplayer_session.player2_id = current_user.id
        db.session.commit()
        return jsonify({'success': True, 'session_id': session_id})
    return jsonify({'success': False, 'message': 'Session not found or already full'})

@bp.route('/multiplayer/game/<int:session_id>')
@login_required
def multiplayer_game(session_id):
    session = MultiplayerSession.query.get_or_404(session_id)
    if current_user.id not in [session.creator_id, session.player2_id]:
        flash(_('You are not part of this game session.'))
        return redirect(url_for('multiplayer.multiplayer'))
    
    # Get or create a multiplayer game instance
    game = MultiplayerGame.query.filter_by(session_id=session_id).first()
    if not game:
        game = MultiplayerGame(session_id=session_id)
        db.session.add(game)
        db.session.commit()
    
    player1 = User.query.get(session.creator_id)
    player2 = User.query.get(session.player2_id)
    
    return render_template('multiplayer_game.html', game=game, session=session, player1=player1, player2=player2)

@bp.route('/multiplayer/get_problem', methods=['POST'])
@login_required
def get_multiplayer_problem():
    session_id = request.json.get('session_id')
    game = MultiplayerGame.query.filter_by(session_id=session_id).first()
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    problem = generate_math_problem(game.difficulty)
    game.current_problem = problem['question']
    game.current_answer = problem['answer']
    db.session.commit()
    
    return jsonify({
        'question': problem['question'],
        'game_id': game.id
    })

@bp.route('/multiplayer/check_answer', methods=['POST'])
@login_required
def check_multiplayer_answer():
    game_id = request.json.get('game_id')
    user_answer = request.json.get('answer')
    player_id = current_user.id
    
    game = MultiplayerGame.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    is_correct = str(user_answer) == game.current_answer
    
    if player_id == game.session.creator_id:
        game.player1_score += 1 if is_correct else 0
    elif player_id == game.session.player2_id:
        game.player2_score += 1 if is_correct else 0
    
    db.session.commit()
    
    return jsonify({
        'correct': is_correct,
        'player1_score': game.player1_score,
        'player2_score': game.player2_score
    })
