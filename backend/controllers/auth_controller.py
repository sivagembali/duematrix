from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Validate password
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 409
        
        # Create new user
        user = User.from_dict(data)
        db.session.add(user)
        db.session.commit()
        
        # Create tokens (convert user.id to string for JWT)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'User already exists or database constraint violation'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        if 'username' not in data and 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Username or email is required'
            }), 400
        
        if 'password' not in data:
            return jsonify({
                'success': False,
                'error': 'Password is required'
            }), 400
        
        # Find user by username or email
        user = None
        if 'username' in data:
            user = User.query.filter_by(username=data['username']).first()
        elif 'email' in data:
            user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create tokens (convert user.id to string for JWT)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Get user data with role information
        user_dict = user.to_dict()
        
        # Get active role mapping
        from models import RoleMapping, RoleMaster
        role_mapping = RoleMapping.query.filter_by(
            user_id=user.id,
            is_active=True
        ).first()
        
        if role_mapping:
            role = RoleMaster.query.get(role_mapping.role_id)
            user_dict['role_id'] = role.id if role else None
            user_dict['role_name'] = role.role_name if role else None
        else:
            user_dict['role_id'] = None
            user_dict['role_name'] = None
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user_dict,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'access_token': access_token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get_or_404(current_user_id)
        
        user_dict = user.to_dict()
        
        # Get active role mapping
        from models import RoleMapping, RoleMaster
        role_mapping = RoleMapping.query.filter_by(
            user_id=user.id,
            is_active=True
        ).first()
        
        if role_mapping:
            role = RoleMaster.query.get(role_mapping.role_id)
            user_dict['role_id'] = role.id if role else None
            user_dict['role_name'] = role.role_name if role else None
        else:
            user_dict['role_id'] = None
            user_dict['role_name'] = None
        
        return jsonify({
            'success': True,
            'data': user_dict
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get_or_404(current_user_id)
        
        data = request.get_json()
        
        if not data or 'current_password' not in data or 'new_password' not in data:
            return jsonify({
                'success': False,
                'error': 'Current password and new password are required'
            }), 400
        
        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 401
        
        # Validate new password
        is_valid, message = validate_password(data['new_password'])
        if not is_valid:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Update password
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client should delete tokens)"""
    # In a production app, you might want to blacklist the token
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    try:
        users = User.query.all()
        users_data = []
        
        for user in users:
            user_dict = user.to_dict()
            
            # Get active role mapping
            from models import RoleMapping, RoleMaster
            role_mapping = RoleMapping.query.filter_by(
                user_id=user.id,
                is_active=True
            ).first()
            
            if role_mapping:
                role = RoleMaster.query.get(role_mapping.role_id)
                user_dict['role_id'] = role.id if role else None
                user_dict['role_name'] = role.role_name if role else None
            else:
                user_dict['role_id'] = None
                user_dict['role_name'] = None
            
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'data': users_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/users/<int:user_id>/status', methods=['PATCH'])
@jwt_required()
def update_user_status(user_id):
    """Update user active status (admin only)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Prevent users from deactivating themselves
        if current_user_id == user_id:
            return jsonify({
                'success': False,
                'error': 'You cannot change your own status'
            }), 400
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'is_active' not in data:
            return jsonify({
                'success': False,
                'error': 'is_active field is required'
            }), 400
        
        user.is_active = data['is_active']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f"User {'activated' if data['is_active'] else 'deactivated'} successfully",
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
