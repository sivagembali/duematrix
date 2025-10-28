from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, JSON

class HeaderConfig(db.Model):
    """Header Configuration model for managing table column settings"""
    __tablename__ = 'header_config'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Column configuration fields
    col_name = Column(String(100), nullable=False, unique=True)  # Column name from credit_bills table
    label = Column(String(200), nullable=False)  # Display label for the column
    status = Column(Boolean, default=True, nullable=False)  # Visibility status (True=visible, False=hidden)
    multi_select_filter = Column(JSON, default=list)  # Available filter options for multi-select
    
    # Additional configuration options
    data_type = Column(String(50), default='text')  # Data type: text, number, date, select, etc.
    width = Column(Integer, default=120)  # Column width in pixels
    sortable = Column(Boolean, default=True)  # Whether column is sortable
    searchable = Column(Boolean, default=True)  # Whether column is searchable
    filter_type = Column(String(50), default='text')  # Filter type: text, select, date_range, number_range
    display_order = Column(Integer, default=0)  # Order of column display
    
    # Formatting options
    format_options = Column(JSON, default=dict)  # Formatting options (currency, date format, etc.)
    
    # Audit fields
    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100), default='system')
    updated_by = Column(String(100), default='system')
    
    def __repr__(self):
        return f'<HeaderConfig {self.col_name}: {self.label}>'
    
    def to_dict(self):
        """Convert model instance to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'colName': self.col_name,
            'label': self.label,
            'status': self.status,
            'multiSelectFilter': self.multi_select_filter or [],
            'dataType': self.data_type,
            'width': self.width,
            'sortable': self.sortable,
            'searchable': self.searchable,
            'filterType': self.filter_type,
            'displayOrder': self.display_order,
            'formatOptions': self.format_options or {},
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'createdBy': self.created_by,
            'updatedBy': self.updated_by
        }
    
    @classmethod
    def get_visible_columns(cls):
        """Get all visible columns ordered by display_order"""
        return cls.query.filter_by(status=True).order_by(cls.display_order).all()
    
    @classmethod
    def get_column_config(cls, col_name):
        """Get configuration for a specific column"""
        return cls.query.filter_by(col_name=col_name).first()
    
    @classmethod
    def toggle_visibility(cls, col_name, visible=None):
        """Toggle or set visibility status for a column"""
        config = cls.query.filter_by(col_name=col_name).first()
        if config:
            if visible is not None:
                config.status = visible
            else:
                config.status = not config.status
            config.updated_at = datetime.utcnow()
            db.session.commit()
            return config
        return None
    
    @classmethod
    def update_filter_options(cls, col_name, filter_options):
        """Update multi-select filter options for a column"""
        config = cls.query.filter_by(col_name=col_name).first()
        if config:
            config.multi_select_filter = filter_options
            config.updated_at = datetime.utcnow()
            db.session.commit()
            return config
        return None