from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from models import User
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    from routes import auth, game, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(api.bp)

    return app

# Create the Flask app instance
flask_app = create_app()

# Ensure the app context is pushed when running the application
if __name__ == '__main__':
    with flask_app.app_context():
        flask_app.run(host='0.0.0.0', port=5000, debug=True)
