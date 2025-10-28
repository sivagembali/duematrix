from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from config.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=['http://localhost:4200'])  # Allow Angular frontend
    
    # Register blueprints
    from app.routes.bill_routes import bills_bp
    from app.routes.header_config_routes import header_config_bp
    app.register_blueprint(bills_bp, url_prefix='/api')
    app.register_blueprint(header_config_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Credit Bill Tracker API is running'}
    
    return app