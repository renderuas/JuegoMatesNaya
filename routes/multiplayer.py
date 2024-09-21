from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from models import MultiplayerSession
from app import db

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
