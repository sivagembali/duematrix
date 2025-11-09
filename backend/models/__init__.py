from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models here to make them available
from .header_model import ColumnHeader
from .user_model import User
from .role_model import RoleMaster, RoleMapping
from .customer_data_model import CustomerData

__all__ = ['db', 'ColumnHeader', 'User', 'RoleMaster', 'RoleMapping']
