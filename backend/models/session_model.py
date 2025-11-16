from datetime import datetime
from . import db


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    # Reference the `users` table which is defined in user_model.py
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    jti = db.Column(db.String(128), unique=True, nullable=False)
    user_agent = db.Column(db.String(512), nullable=True)
    ip_address = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    revoked = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'jti': self.jti,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'expires_at': self.expires_at.isoformat() + 'Z' if self.expires_at else None,
            'revoked': self.revoked
        }
