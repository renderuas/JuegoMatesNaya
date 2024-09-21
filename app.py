from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

babel = Babel(app)

def get_locale():
    return request.accept_languages.best_match(['es', 'en'])

babel.init_app(app, locale_selector=get_locale)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import auth, game, api, multiplayer
app.register_blueprint(auth.bp)
app.register_blueprint(game.bp)
app.register_blueprint(api.bp)
app.register_blueprint(multiplayer.bp)

@app.route('/')
def index():
    return render_template('index.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
