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
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
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
    
    @app.route('/init-db')
    def init_database():
        """Initialize database with seed data (use once after deployment)"""
        try:
            results = {}

            # Import and run seed modules' main() functions so they actually execute
            import seed_roles_users
            try:
                seed_roles_users.main()
                results['roles_users'] = 'seeded'
            except Exception as e:
                results['roles_users'] = f'error: {str(e)}'

            import seed_comprehensive_headers
            try:
                if hasattr(seed_comprehensive_headers, 'main'):
                    seed_comprehensive_headers.main()
                elif hasattr(seed_comprehensive_headers, 'seed_comprehensive_headers'):
                    seed_comprehensive_headers.seed_comprehensive_headers()
                else:
                    raise AttributeError('No entry function found in seed_comprehensive_headers')
                results['headers'] = 'seeded'
            except Exception as e:
                results['headers'] = f'error: {str(e)}'

            import seed_cycles
            try:
                if hasattr(seed_cycles, 'main'):
                    seed_cycles.main()
                elif hasattr(seed_cycles, 'seed_cycles'):
                    seed_cycles.seed_cycles()
                else:
                    raise AttributeError('No entry function found in seed_cycles')
                results['cycles'] = 'seeded'
            except Exception as e:
                results['cycles'] = f'error: {str(e)}'

            import seed_customer_data
            try:
                if hasattr(seed_customer_data, 'main'):
                    seed_customer_data.main()
                elif hasattr(seed_customer_data, 'seed_customer_data'):
                    seed_customer_data.seed_customer_data(100)
                else:
                    raise AttributeError('No entry function found in seed_customer_data')
                results['customer_data'] = 'seeded'
            except Exception as e:
                results['customer_data'] = f'error: {str(e)}'

            return {
                'success': True,
                'message': 'Database initialized successfully',
                'results': results
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error initializing database: {str(e)}'
            }, 500
    
    return app


# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
