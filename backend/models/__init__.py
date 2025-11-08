from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models here to make them available
from .header_model import ColumnHeader

__all__ = ['db', 'ColumnHeader']
