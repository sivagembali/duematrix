from . import db
from datetime import datetime


class RoleMaster(db.Model):
    """
    Role Master model for role definitions
    """
    
    __tablename__ = 'role_master'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Role Information
    role_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    role_description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Audit Fields
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    
    # Relationships
    role_mappings = db.relationship('RoleMapping', backref='role', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<RoleMaster {self.role_name}>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'role_name': self.role_name,
            'role_description': self.role_description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
    
    @staticmethod
    def from_dict(data):
        """Create model instance from dictionary"""
        return RoleMaster(
            role_name=data.get('role_name'),
            role_description=data.get('role_description'),
            is_active=data.get('is_active', True),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by')
        )


class RoleMapping(db.Model):
    """
    Role Mapping model for user-role assignments
    """
    
    __tablename__ = 'role_mapping'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role_master.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = db.Column(db.DateTime)
    
    # Audit Fields
    assigned_by = db.Column(db.Integer)
    revoked_by = db.Column(db.Integer)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='unique_user_role'),
    )
    
    def __repr__(self):
        return f"<RoleMapping user_id={self.user_id} role_id={self.role_id}>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'is_active': self.is_active,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'revoked_at': self.revoked_at.isoformat() if self.revoked_at else None,
            'assigned_by': self.assigned_by,
            'revoked_by': self.revoked_by
        }
    
    @staticmethod
    def from_dict(data):
        """Create model instance from dictionary"""
        return RoleMapping(
            user_id=data.get('user_id'),
            role_id=data.get('role_id'),
            is_active=data.get('is_active', True),
            assigned_by=data.get('assigned_by'),
            revoked_by=data.get('revoked_by')
        )
