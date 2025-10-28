from flask import Blueprint, request, jsonify
from app import db
from app.models.header_config import HeaderConfig
from app.models.credit_bill import CreditBill
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from datetime import datetime
import math

# Create Blueprint for header config routes
header_config_bp = Blueprint('header_config', __name__)

@header_config_bp.route('/header-config', methods=['GET'])
def get_all_header_configs():
    """Get all header configurations"""
    try:
        # Query parameters for filtering
        visible_only = request.args.get('visible_only', 'false').lower() == 'true'
        
        if visible_only:
            configs = HeaderConfig.get_visible_columns()
        else:
            configs = HeaderConfig.query.order_by(HeaderConfig.display_order).all()
        
        # Convert to dict format
        configs_data = [config.to_dict() for config in configs]
        
        return jsonify({
            'success': True,
            'data': configs_data,
            'count': len(configs_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch header configurations',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/<int:config_id>', methods=['GET'])
def get_header_config_by_id(config_id):
    """Get a specific header configuration by ID"""
    try:
        config = HeaderConfig.query.get_or_404(config_id)
        return jsonify({
            'success': True,
            'data': config.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Header configuration not found',
            'message': str(e)
        }), 404

@header_config_bp.route('/header-config/by-column/<string:col_name>', methods=['GET'])
def get_header_config_by_column(col_name):
    """Get header configuration by column name"""
    try:
        config = HeaderConfig.get_column_config(col_name)
        if not config:
            return jsonify({
                'success': False,
                'error': 'Configuration not found for column',
                'message': f'No configuration found for column: {col_name}'
            }), 404
            
        return jsonify({
            'success': True,
            'data': config.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch configuration',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config', methods=['POST'])
def create_header_config():
    """Create a new header configuration"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        if not data.get('colName'):
            return jsonify({
                'success': False,
                'error': 'Column name is required'
            }), 400
            
        if not data.get('label'):
            return jsonify({
                'success': False,
                'error': 'Label is required'
            }), 400
        
        # Create new configuration
        new_config = HeaderConfig(
            col_name=data.get('colName'),
            label=data.get('label'),
            status=data.get('status', True),
            multi_select_filter=data.get('multiSelectFilter', []),
            data_type=data.get('dataType', 'text'),
            width=data.get('width', 120),
            sortable=data.get('sortable', True),
            searchable=data.get('searchable', True),
            filter_type=data.get('filterType', 'text'),
            display_order=data.get('displayOrder', 0),
            format_options=data.get('formatOptions', {}),
            created_by=data.get('createdBy', 'api_user')
        )
        
        db.session.add(new_config)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_config.to_dict(),
            'message': 'Header configuration created successfully'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Configuration already exists',
            'message': f'Configuration for column {data.get("colName")} already exists'
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to create configuration',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/<int:config_id>', methods=['PUT'])
def update_header_config(config_id):
    """Update an existing header configuration"""
    try:
        config = HeaderConfig.query.get_or_404(config_id)
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update configuration fields
        if 'label' in data:
            config.label = data['label']
        if 'status' in data:
            config.status = data['status']
        if 'multiSelectFilter' in data:
            config.multi_select_filter = data['multiSelectFilter']
        if 'dataType' in data:
            config.data_type = data['dataType']
        if 'width' in data:
            config.width = data['width']
        if 'sortable' in data:
            config.sortable = data['sortable']
        if 'searchable' in data:
            config.searchable = data['searchable']
        if 'filterType' in data:
            config.filter_type = data['filterType']
        if 'displayOrder' in data:
            config.display_order = data['displayOrder']
        if 'formatOptions' in data:
            config.format_options = data['formatOptions']
        
        config.updated_by = data.get('updatedBy', 'api_user')
        config.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': config.to_dict(),
            'message': 'Header configuration updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to update configuration',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/<int:config_id>', methods=['DELETE'])
def delete_header_config(config_id):
    """Delete a header configuration"""
    try:
        config = HeaderConfig.query.get_or_404(config_id)
        db.session.delete(config)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Header configuration deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to delete configuration',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/toggle-visibility/<string:col_name>', methods=['PATCH'])
def toggle_column_visibility(col_name):
    """Toggle visibility status for a column"""
    try:
        data = request.get_json() or {}
        visible = data.get('visible')  # If provided, set to specific value, otherwise toggle
        
        config = HeaderConfig.toggle_visibility(col_name, visible)
        
        if not config:
            return jsonify({
                'success': False,
                'error': 'Configuration not found',
                'message': f'No configuration found for column: {col_name}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': config.to_dict(),
            'message': f'Visibility toggled for column: {col_name}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to toggle visibility',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/update-filters/<string:col_name>', methods=['PATCH'])
def update_column_filters(col_name):
    """Update multi-select filter options for a column"""
    try:
        data = request.get_json()
        
        if not data or 'filterOptions' not in data:
            return jsonify({
                'success': False,
                'error': 'Filter options are required'
            }), 400
        
        filter_options = data['filterOptions']
        
        config = HeaderConfig.update_filter_options(col_name, filter_options)
        
        if not config:
            return jsonify({
                'success': False,
                'error': 'Configuration not found',
                'message': f'No configuration found for column: {col_name}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': config.to_dict(),
            'message': f'Filter options updated for column: {col_name}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to update filter options',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/bulk-update', methods=['PUT'])
def bulk_update_configurations():
    """Bulk update multiple header configurations"""
    try:
        data = request.get_json()
        
        if not data or 'configs' not in data:
            return jsonify({
                'success': False,
                'error': 'Configs array is required'
            }), 400
        
        updated_configs = []
        
        for config_data in data['configs']:
            if 'id' not in config_data:
                continue
                
            config = HeaderConfig.query.get(config_data['id'])
            if not config:
                continue
            
            # Update fields if provided
            for field, value in config_data.items():
                if field == 'id':
                    continue
                elif field == 'label':
                    config.label = value
                elif field == 'status':
                    config.status = value
                elif field == 'multiSelectFilter':
                    config.multi_select_filter = value
                elif field == 'displayOrder':
                    config.display_order = value
                elif field == 'width':
                    config.width = value
                # Add more fields as needed
            
            config.updated_at = datetime.utcnow()
            updated_configs.append(config.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': updated_configs,
            'message': f'Updated {len(updated_configs)} configurations'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to bulk update configurations',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/bills-with-config', methods=['GET'])
def get_bills_with_config():
    """Get bills data with header configuration for the configurable table"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 25, type=int), 100)  # Limit max per_page
        search = request.args.get('search', '').strip()
        status_filter = request.args.get('status', '').strip()
        
        # Get header configurations
        header_configs = HeaderConfig.query.order_by(HeaderConfig.display_order).all()
        visible_columns = [config.col_name for config in header_configs if config.status]
        
        # Build query for bills
        query = CreditBill.query
        
        # Apply search filter
        if search:
            search_conditions = []
            for config in header_configs:
                if config.searchable and config.status:
                    # Create search condition based on column name
                    column = getattr(CreditBill, config.col_name, None)
                    if column is not None:
                        search_conditions.append(column.ilike(f'%{search}%'))
            
            if search_conditions:
                query = query.filter(or_(*search_conditions))
        
        # Apply status filter
        if status_filter:
            query = query.filter(CreditBill.status == status_filter)
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        bills = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Calculate pagination info
        total_pages = math.ceil(total_count / per_page) if total_count > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        # Convert bills to dict format
        bills_data = []
        for bill in bills:
            bill_dict = bill.to_dict()
            bills_data.append(bill_dict)
        
        # Convert header configs to dict format
        header_configs_data = [config.to_dict() for config in header_configs]
        
        return jsonify({
            'success': True,
            'data': {
                'bills': bills_data,
                'headerConfig': header_configs_data,
                'visibleColumns': visible_columns,
                'pagination': {
                    'page': page,
                    'perPage': per_page,
                    'total': total_count,
                    'totalPages': total_pages,
                    'hasNext': has_next,
                    'hasPrev': has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch bills with configuration',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/reset-defaults', methods=['POST'])
def reset_to_defaults():
    """Reset all header configurations to default values"""
    try:
        # Set all columns to visible (default state)
        HeaderConfig.query.update({'status': True})
        db.session.commit()
        
        configs = HeaderConfig.query.order_by(HeaderConfig.display_order).all()
        configs_data = [config.to_dict() for config in configs]
        
        return jsonify({
            'success': True,
            'data': configs_data,
            'message': 'Header configurations reset to defaults successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to reset configurations',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/column/<string:col_name>', methods=['GET'])
def get_column_config_by_name(col_name):
    """Get configuration for a specific column by name"""
    try:
        config = HeaderConfig.query.filter_by(col_name=col_name).first()
        
        if not config:
            return jsonify({
                'success': False,
                'error': 'Configuration not found',
                'message': f'No configuration found for column: {col_name}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': config.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch column configuration',
            'message': str(e)
        }), 500

@header_config_bp.route('/header-config/display-order', methods=['PATCH'])
def update_display_order():
    """Update display order of columns"""
    try:
        data = request.get_json()
        
        if not data or 'columnOrders' not in data:
            return jsonify({
                'success': False,
                'error': 'Column orders array is required'
            }), 400
        
        column_orders = data['columnOrders']
        
        for order_data in column_orders:
            if 'colName' not in order_data or 'displayOrder' not in order_data:
                continue
                
            config = HeaderConfig.query.filter_by(col_name=order_data['colName']).first()
            if config:
                config.display_order = order_data['displayOrder']
                config.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Display order updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to update display order',
            'message': str(e)
        }), 500