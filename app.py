from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

from routes import auth, game, api
app.register_blueprint(auth.bp)
app.register_blueprint(game.bp)
app.register_blueprint(api.bp)

@app.route('/')
def index():
    return render_template('index.html')

with app.app_context():
    db.create_all()
    # This will create new tables if they don't exist, but won't modify existing ones
    # For the password_hash change to take effect, you might need to drop and recreate the user table
    # or use a migration tool like Alembic for production environments

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
