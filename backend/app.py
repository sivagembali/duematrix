from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import config
from models import db
from flask_migrate import Migrate
import os

def create_app(config_name=None):
    """Application factory pattern"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    Migrate(app, db)
    JWTManager(app)
    Bcrypt(app)
    
    # Register blueprints
    from controllers.header_controller import header_bp
    from controllers.auth_controller import auth_bp
    from controllers.role_controller import role_bp
    from controllers.data_controller import data_bp
    
    app.register_blueprint(header_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(role_bp, url_prefix='/api')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return {
            'message': 'DueMatrix API is running',
            'version': '1.0.0',
            'status': 'healthy'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'database': 'connected'}
    
    return app


# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
