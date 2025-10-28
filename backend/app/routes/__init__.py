# Import all routes here for easy access
from .bill_routes import bills_bp
from .header_config_routes import header_config_bp

__all__ = ['bills_bp', 'header_config_bp']