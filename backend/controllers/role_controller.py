from flask import Blueprint, request, jsonify
from models import db, RoleMaster, RoleMapping, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

role_bp = Blueprint('role', __name__)


@role_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_all_roles():
    """Get all roles"""
    try:
        roles = RoleMaster.query.all()
        return jsonify({
            'success': True,
            'data': [role.to_dict() for role in roles]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@role_bp.route('/roles/<int:role_id>', methods=['GET'])
@jwt_required()
def get_role(role_id):
    """Get single role by ID"""
    try:
        role = RoleMaster.query.get_or_404(role_id)
        return jsonify({
            'success': True,
            'data': role.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@role_bp.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    """Create a new role"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data or 'role_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Role name is required'
            }), 400
        
        # Check if role already exists
        existing_role = RoleMaster.query.filter_by(role_name=data['role_name']).first()
        if existing_role:
            return jsonify({
                'success': False,
                'error': 'Role already exists'
            }), 409
        
        data['created_by'] = current_user_id
        role = RoleMaster.from_dict(data)
        db.session.add(role)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Role created successfully',
            'data': role.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Role already exists'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    """Update a role"""
    try:
        current_user_id = int(get_jwt_identity())
        role = RoleMaster.query.get_or_404(role_id)
        data = request.get_json()
        
        if 'role_name' in data:
            role.role_name = data['role_name']
        if 'role_description' in data:
            role.role_description = data['role_description']
        if 'is_active' in data:
            role.is_active = data['is_active']
        
        role.updated_by = current_user_id
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Role updated successfully',
            'data': role.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    """Delete a role"""
    try:
        role = RoleMaster.query.get_or_404(role_id)
        
        # Check if role is assigned to any users
        active_mappings = RoleMapping.query.filter_by(
            role_id=role_id,
            is_active=True
        ).count()
        
        if active_mappings > 0:
            return jsonify({
                'success': False,
                'error': f'Cannot delete role. It is assigned to {active_mappings} user(s)'
            }), 400
        
        db.session.delete(role)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Role deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@role_bp.route('/role-mappings', methods=['POST'])
@jwt_required()
def assign_role_to_user():
    """Assign a role to a user"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'role_id' not in data:
            return jsonify({
                'success': False,
                'error': 'user_id and role_id are required'
            }), 400
        
        # Verify user and role exist
        user = User.query.get_or_404(data['user_id'])
        role = RoleMaster.query.get_or_404(data['role_id'])
        
        # Check if mapping already exists
        existing_mapping = RoleMapping.query.filter_by(
            user_id=data['user_id'],
            role_id=data['role_id']
        ).first()
        
        if existing_mapping:
            if existing_mapping.is_active:
                return jsonify({
                    'success': False,
                    'error': 'User already has this role'
                }), 409
            else:
                # Reactivate existing mapping
                existing_mapping.is_active = True
                existing_mapping.revoked_at = None
                existing_mapping.assigned_by = current_user_id
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Role reactivated for user',
                    'data': existing_mapping.to_dict()
                }), 200
        
        # Create new mapping
        data['assigned_by'] = current_user_id
        role_mapping = RoleMapping.from_dict(data)
        db.session.add(role_mapping)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Role assigned to user successfully',
            'data': role_mapping.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@role_bp.route('/role-mappings/<int:mapping_id>', methods=['DELETE'])
@jwt_required()
def revoke_role_from_user(mapping_id):
    """Revoke a role from a user"""
    try:
        current_user_id = int(get_jwt_identity())
        role_mapping = RoleMapping.query.get_or_404(mapping_id)
        
        role_mapping.is_active = False
        role_mapping.revoked_at = db.func.now()
        role_mapping.revoked_by = current_user_id
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Role revoked from user successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@role_bp.route('/users/<int:user_id>/roles', methods=['GET'])
@jwt_required()
def get_user_roles(user_id):
    """Get all roles for a specific user"""
    try:
        user = User.query.get_or_404(user_id)
        
        role_mappings = RoleMapping.query.filter_by(
            user_id=user_id,
            is_active=True
        ).all()
        
        roles = []
        for mapping in role_mappings:
            role = RoleMaster.query.get(mapping.role_id)
            if role:
                role_data = role.to_dict()
                role_data['mapping_id'] = mapping.id
                role_data['assigned_at'] = mapping.assigned_at.isoformat()
                roles.append(role_data)
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user_id,
                'username': user.username,
                'roles': roles
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@role_bp.route('/roles/<int:role_id>/users', methods=['GET'])
@jwt_required()
def get_role_users(role_id):
    """Get all users with a specific role"""
    try:
        role = RoleMaster.query.get_or_404(role_id)
        
        role_mappings = RoleMapping.query.filter_by(
            role_id=role_id,
            is_active=True
        ).all()
        
        users = []
        for mapping in role_mappings:
            user = User.query.get(mapping.user_id)
            if user:
                user_data = user.to_dict()
                user_data['mapping_id'] = mapping.id
                user_data['assigned_at'] = mapping.assigned_at.isoformat()
                users.append(user_data)
        
        return jsonify({
            'success': True,
            'data': {
                'role_id': role_id,
                'role_name': role.role_name,
                'users': users
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
