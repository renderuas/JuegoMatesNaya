from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from flask_babel import _
from app import db
from models import User
import logging

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash(_('Oops! That superhero name is already taken. Try another one!'))
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash(_("Yay! You're now part of our Math Adventure. Let's play!"))
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    logging.info("Login route accessed")
    if current_user.is_authenticated:
        logging.info(f"User {current_user.username} is already authenticated, redirecting to game.play")
        return redirect(url_for('game.play'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"Login attempt for user: {username}")
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            logging.info(f"User {username} logged in successfully")
            flash(_('Welcome back, Math Star! Ready for some fun?'))
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('game.play')
            logging.info(f"Redirecting to: {next_page}")
            return redirect(next_page)
        else:
            logging.warning(f"Failed login attempt for user: {username}")
            flash(_('Oops! Your superhero name or secret code is not right. Try again!'))
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('See you next time, Math Star!'))
    return redirect(url_for('index'))
