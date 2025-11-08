from . import db
from datetime import datetime


class ColumnHeader(db.Model):
    """
    Model for storing column header configurations
    This defines how columns should be displayed in the frontend table
    """
    
    __tablename__ = 'column_headers'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Column Configuration
    col_header = db.Column(db.String(100), nullable=False, unique=True, index=True)
    col_label = db.Column(db.String(200), nullable=False)
    is_editable = db.Column(db.Boolean, default=True, nullable=False)
    is_multi_select = db.Column(db.Boolean, default=False, nullable=False)
    col_width = db.Column(db.Float, default=12.5, nullable=False)  # Width in rem
    display = db.Column(db.Boolean, default=True, nullable=False)
    default_display = db.Column(db.Boolean, default=False, nullable=False)
    is_frozen = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, nullable=True, index=True)  # Role association
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100), default='system')
    updated_by = db.Column(db.String(100), default='system')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('col_width > 0', name='check_col_width_positive'),
        db.CheckConstraint('display_order >= 0', name='check_display_order_non_negative'),
    )
    
    def __repr__(self):
        return f"<ColumnHeader {self.col_header}: {self.col_label}>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'col_header': self.col_header,
            'col_label': self.col_label,
            'is_editable': self.is_editable,
            'is_multi_select': self.is_multi_select,
            'col_width': self.col_width,
            'display': self.display,
            'default_display': self.default_display,
            'is_frozen': self.is_frozen,
            'display_order': self.display_order,
            'role_id': self.role_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
    
    @staticmethod
    def from_dict(data):
        """Create model instance from dictionary"""
        return ColumnHeader(
            col_header=data.get('col_header'),
            col_label=data.get('col_label'),
            is_editable=data.get('is_editable', True),
            is_multi_select=data.get('is_multi_select', False),
            col_width=data.get('col_width', 12.5),
            display=data.get('display', True),
            default_display=data.get('default_display', False),
            is_frozen=data.get('is_frozen', False),
            display_order=data.get('display_order', 0),
            role_id=data.get('role_id'),
            created_by=data.get('created_by', 'system'),
            updated_by=data.get('updated_by', 'system')
        )
