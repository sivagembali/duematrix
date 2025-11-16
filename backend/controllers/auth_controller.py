from flask import Blueprint, request, jsonify
from models import db, User, Session
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    decode_token
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
        
        # Detect existing active sessions for this user before issuing new tokens
        try:
            existing_sessions = Session.query.filter_by(user_id=user.id, revoked=False).all()
        except Exception:
            existing_sessions = []

        force = bool(data.get('force', False)) if isinstance(data, dict) else False
        if existing_sessions and not force:
            sessions_info = [s.to_dict() for s in existing_sessions]
            return jsonify({
                'success': False,
                'error': 'Existing active session(s) detected',
                'existing_sessions': sessions_info
            }), 409

        # If force is true, revoke other sessions before continuing
        if existing_sessions and force:
            for s in existing_sessions:
                s.revoked = True
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
        
        # Detect existing active sessions for this user before issuing new tokens
        try:
            existing_sessions = Session.query.filter_by(user_id=user.id, revoked=False).all()
        except Exception as e:
            print(f'Warning: could not query sessions: {str(e)}')
            existing_sessions = []

        force = bool(data.get('force', False)) if isinstance(data, dict) else False
        if existing_sessions and not force:
            sessions_info = [s.to_dict() for s in existing_sessions]
            return jsonify({
                'success': False,
                'error': 'Existing active session(s) detected',
                'existing_sessions': sessions_info
            }), 409

        # If force is true, revoke other sessions before continuing
        if existing_sessions and force:
            for s in existing_sessions:
                s.revoked = True
            db.session.commit()
        
        # Create tokens (convert user.id to string for JWT)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Persist session record for this login
        try:
            decoded = decode_token(access_token)
            jti = decoded.get('jti')
            sess = Session(
                user_id=user.id,
                jti=jti,
                user_agent=request.headers.get('User-Agent'),
                ip_address=request.remote_addr
            )
            db.session.add(sess)
            db.session.commit()
        except Exception as e:
            # If session persistence fails, log it but continue to return tokens
            db.session.rollback()
            print('Warning: could not persist session record:', str(e))

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


# Temporary debug endpoint - returns non-sensitive user existence info
# REMOVE or protect this in production once debugging is complete
@auth_bp.route('/debug/user/<string:username>', methods=['GET'])
def debug_user(username):
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'exists': False}), 200
        return jsonify({
            'exists': True,
            'username': user.username,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'created_at': user.created_at.isoformat() + 'Z' if user.created_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    try:
        # Mark the session (by jti) revoked so token is blocked
        jti = get_jwt().get('jti')
        if jti:
            sess = Session.query.filter_by(jti=jti).first()
            if sess:
                sess.revoked = True
                db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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


@auth_bp.route('/users/<int:user_id>/password', methods=['PATCH'])
@jwt_required()
def change_user_password(user_id):
    """Change another user's password (admin only)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Prevent users from changing their own password through this endpoint
        if current_user_id == user_id:
            return jsonify({
                'success': False,
                'error': 'Use /change-password endpoint to change your own password'
            }), 400
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if not data or 'new_password' not in data:
            return jsonify({
                'success': False,
                'error': 'new_password is required'
            }), 400
        
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


@auth_bp.route('/users/export', methods=['GET'])
@jwt_required()
def export_users():
    """Export users to CSV"""
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        users = User.query.all()
        
        # Create CSV in memory
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow(['id', 'username', 'email', 'first_name', 'last_name', 'role_id', 'is_active', 'is_verified', 'created_at'])
        
        # Write data
        for user in users:
            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.role_id,
                user.is_active,
                user.is_verified,
                user.created_at.isoformat() if user.created_at else ''
            ])
        
        # Create response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=users.csv"
        output.headers["Content-type"] = "text/csv"
        
        return output
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/users/import', methods=['POST'])
@jwt_required()
def import_users():
    """Import users from CSV"""
    try:
        import csv
        from io import StringIO
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'error': 'Only CSV files are allowed'
            }), 400
        
        # Read CSV
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        created_count = 0
        updated_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Check if user exists by email or username
                existing_user = User.query.filter(
                    (User.email == row['email']) | (User.username == row['username'])
                ).first()
                
                if existing_user:
                    # Update existing user
                    existing_user.first_name = row.get('first_name', existing_user.first_name)
                    existing_user.last_name = row.get('last_name', existing_user.last_name)
                    existing_user.role_id = int(row['role_id']) if row.get('role_id') else existing_user.role_id
                    existing_user.is_active = row.get('is_active', 'True').lower() in ['true', '1', 'yes']
                    existing_user.is_verified = row.get('is_verified', 'False').lower() in ['true', '1', 'yes']
                    updated_count += 1
                else:
                    # Create new user (requires password)
                    if 'password' not in row or not row['password']:
                        errors.append(f"Row {row_num}: New user requires password")
                        continue
                    
                    # Validate required fields
                    if not row.get('username') or not row.get('email'):
                        errors.append(f"Row {row_num}: username and email are required")
                        continue
                    
                    new_user = User(
                        username=row['username'],
                        email=row['email'],
                        first_name=row.get('first_name', ''),
                        last_name=row.get('last_name', ''),
                        role_id=int(row['role_id']) if row.get('role_id') else None,
                        is_active=row.get('is_active', 'True').lower() in ['true', '1', 'yes'],
                        is_verified=row.get('is_verified', 'False').lower() in ['true', '1', 'yes']
                    )
                    new_user.set_password(row['password'])
                    db.session.add(new_user)
                    created_count += 1
                    
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Import completed: {created_count} created, {updated_count} updated',
            'created': created_count,
            'updated': updated_count,
            'errors': errors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
