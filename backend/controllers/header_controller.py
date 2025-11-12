from flask import Blueprint, request, jsonify
from models import db, ColumnHeader, User, RoleMapping, RoleMaster
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

header_bp = Blueprint('headers', __name__)


@header_bp.route('/headers', methods=['GET'])
def get_all_headers():
    """Get all column headers"""
    try:
        headers = ColumnHeader.query.order_by(ColumnHeader.display_order).all()
        return jsonify({
            'success': True,
            'data': [header.to_dict() for header in headers],
            'count': len(headers)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/<int:header_id>', methods=['GET'])
def get_header(header_id):
    """Get a specific column header by ID"""
    try:
        header = ColumnHeader.query.get_or_404(header_id)
        return jsonify({
            'success': True,
            'data': header.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@header_bp.route('/headers', methods=['POST'])
def create_header():
    """Create a new column header"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['col_header', 'col_label', 'display_order']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Create new header
        header = ColumnHeader.from_dict(data)
        db.session.add(header)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': header.to_dict(),
            'message': 'Column header created successfully'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Column header already exists or constraint violation'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/<int:header_id>', methods=['PUT'])
def update_header(header_id):
    """Update an existing column header"""
    try:
        header = ColumnHeader.query.get_or_404(header_id)
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update fields
        updatable_fields = [
            'col_label', 'is_editable', 'is_multi_select', 'col_width',
            'display', 'default_display', 'is_frozen', 'display_order', 'updated_by'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(header, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': header.to_dict(),
            'message': 'Column header updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/<int:header_id>', methods=['DELETE'])
def delete_header(header_id):
    """Delete a column header"""
    try:
        header = ColumnHeader.query.get_or_404(header_id)
        db.session.delete(header)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Column header deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/bulk', methods=['POST'])
def create_headers_bulk():
    """Create multiple column headers at once"""
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return jsonify({
                'success': False,
                'error': 'Data must be a list of header objects'
            }), 400
        
        headers = []
        for item in data:
            header = ColumnHeader.from_dict(item)
            headers.append(header)
        
        db.session.bulk_save_objects(headers)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(headers)} column headers created successfully',
            'count': len(headers)
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Duplicate column headers or constraint violation'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/default', methods=['GET'])
def get_default_headers():
    """Get only headers marked as default_display=true"""
    try:
        headers = ColumnHeader.query.filter_by(default_display=True).order_by(ColumnHeader.display_order).all()
        return jsonify({
            'success': True,
            'data': [header.to_dict() for header in headers],
            'count': len(headers)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_headers():
    """
    Get column headers for the authenticated user's dashboard
    Returns headers based on user's role or all headers if no role-specific headers exist
    """
    try:
        # Get current user
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get user's role
        role_mapping = RoleMapping.query.filter_by(user_id=user.id).first()
        
        if role_mapping:
            # Get headers for user's role and generic headers (role_id=null)
            headers = ColumnHeader.query.filter(
                (ColumnHeader.role_id == role_mapping.role_id) | 
                (ColumnHeader.role_id == None)
            ).filter_by(display=True).order_by(ColumnHeader.display_order).all()
        else:
            # No role assigned, return only generic headers
            headers = ColumnHeader.query.filter_by(
                role_id=None, 
                display=True
            ).order_by(ColumnHeader.display_order).all()
        
        return jsonify({
            'success': True,
            'data': [header.to_dict() for header in headers],
            'count': len(headers),
            'user': {
                'id': user.id,
                'username': user.username,
                'role_id': role_mapping.role_id if role_mapping else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/role/<int:role_id>', methods=['GET'])
@jwt_required()
def get_headers_by_role(role_id):
    """
    Get column headers for a specific role
    Admin endpoint to preview headers for any role
    """
    try:
        # Get current user to check if admin
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Check if role exists
        role = RoleMaster.query.get(role_id)
        if not role:
            return jsonify({
                'success': False,
                'error': 'Role not found'
            }), 404
        
        # Get headers for the specified role and generic headers
        headers = ColumnHeader.query.filter(
            (ColumnHeader.role_id == role_id) | 
            (ColumnHeader.role_id == None)
        ).filter_by(display=True).order_by(ColumnHeader.display_order).all()
        
        return jsonify({
            'success': True,
            'data': [header.to_dict() for header in headers],
            'count': len(headers),
            'role': {
                'id': role.id,
                'name': role.role_name,
                'description': role.role_description
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@header_bp.route('/headers/export', methods=['GET'])
@jwt_required()
def export_headers():
    """Export headers to CSV"""
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        headers = ColumnHeader.query.all()
        
        # Create CSV in memory
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow(['id', 'col_header', 'col_label', 'is_editable', 'is_multi_select', 'col_width', 'display', 'default_display', 'is_frozen', 'display_order', 'role_id'])
        
        # Write data
        for header in headers:
            writer.writerow([
                header.id,
                header.col_header,
                header.col_label,
                header.is_editable,
                header.is_multi_select,
                header.col_width,
                header.display,
                header.default_display,
                header.is_frozen,
                header.display_order,
                header.role_id
            ])
        
        # Create response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=headers.csv"
        output.headers["Content-type"] = "text/csv"
        
        return output
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@header_bp.route('/headers/import', methods=['POST'])
@jwt_required()
def import_headers():
    """Import headers from CSV"""
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
        
        current_user_id = get_jwt_identity()
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Check if header exists by col_header
                existing_header = ColumnHeader.query.filter_by(col_header=row['col_header']).first()
                
                if existing_header:
                    # Update existing header
                    existing_header.col_label = row.get('col_label', existing_header.col_label)
                    existing_header.is_editable = row.get('is_editable', 'True').lower() in ['true', '1', 'yes']
                    existing_header.is_multi_select = row.get('is_multi_select', 'False').lower() in ['true', '1', 'yes']
                    existing_header.col_width = int(row.get('col_width', existing_header.col_width))
                    existing_header.display = row.get('display', 'True').lower() in ['true', '1', 'yes']
                    existing_header.default_display = row.get('default_display', 'True').lower() in ['true', '1', 'yes']
                    existing_header.is_frozen = row.get('is_frozen', 'False').lower() in ['true', '1', 'yes']
                    existing_header.display_order = int(row.get('display_order', existing_header.display_order))
                    existing_header.role_id = int(row['role_id']) if row.get('role_id') and row['role_id'] != '' else None
                    existing_header.updated_by = current_user_id
                    updated_count += 1
                else:
                    # Create new header
                    if not row.get('col_header'):
                        errors.append(f"Row {row_num}: col_header is required")
                        continue
                    
                    new_header = ColumnHeader(
                        col_header=row['col_header'],
                        col_label=row.get('col_label', ''),
                        is_editable=row.get('is_editable', 'True').lower() in ['true', '1', 'yes'],
                        is_multi_select=row.get('is_multi_select', 'False').lower() in ['true', '1', 'yes'],
                        col_width=int(row.get('col_width', 150)),
                        display=row.get('display', 'True').lower() in ['true', '1', 'yes'],
                        default_display=row.get('default_display', 'True').lower() in ['true', '1', 'yes'],
                        is_frozen=row.get('is_frozen', 'False').lower() in ['true', '1', 'yes'],
                        display_order=int(row.get('display_order', 0)),
                        role_id=int(row['role_id']) if row.get('role_id') and row['role_id'] != '' else None,
                        created_by=current_user_id,
                        updated_by=current_user_id
                    )
                    db.session.add(new_header)
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
