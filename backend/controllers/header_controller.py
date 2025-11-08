from flask import Blueprint, request, jsonify
from models import db, ColumnHeader
from sqlalchemy.exc import IntegrityError

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
