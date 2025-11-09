"""
Data Controller
Handles customer data CRUD operations and queries
"""

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import CustomerData, User, db, Cycle
from sqlalchemy import or_, and_

data_bp = Blueprint('data', __name__)


@data_bp.route('/customer-data', methods=['GET'])
@jwt_required()
def get_customer_data():
    """
    Get customer data with pagination and filtering
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Records per page (default: 100)
    - search: Search term for filtering
    - status: Filter by status
    - department: Filter by department
    - city: Filter by city
    """
    try:
        current_user = get_jwt_identity()
        # Diagnostic logging: record who called and which query params were sent
        try:
            current_app.logger.info(f"get_customer_data called by: {current_user} args={dict(request.args)}")
        except Exception:
            # If logger or current_user isn't available for some reason, fallback to print
            print(f"get_customer_data called by: {current_user} args={dict(request.args)}")
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        search = request.args.get('search', '', type=str)
        status = request.args.get('status', '', type=str)
        department = request.args.get('department', '', type=str)
        city = request.args.get('city', '', type=str)
        cycle = request.args.get('cycle', '', type=str)
        
        # Build query
        query = CustomerData.query
        
        # Apply filters
        if search:
            query = query.filter(
                or_(
                    CustomerData.customer_name.ilike(f'%{search}%'),
                    CustomerData.email.ilike(f'%{search}%'),
                    CustomerData.employee_id.ilike(f'%{search}%')
                )
            )
        
        if status:
            query = query.filter(CustomerData.status == status)
        
        if department:
            query = query.filter(CustomerData.department == department)
        
        if city:
            query = query.filter(CustomerData.city == city)
        if cycle:
            query = query.filter(CustomerData.cycle_name == cycle)
        
        # Order by id descending (most recent first)
        query = query.order_by(CustomerData.id.desc())
        
    # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert to dictionary
        data = [record.to_dict() for record in pagination.items]
        
        result = {
            'success': True,
            'message': 'Customer data retrieved successfully',
            'data': data,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }

        # Log result summary for diagnostics
        try:
            current_app.logger.info(f"get_customer_data returning {len(data)} records for user={current_user} cycle={cycle}")
        except Exception:
            print(f"get_customer_data returning {len(data)} records for user={current_user} cycle={cycle}")

        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving customer data: {str(e)}'
        }), 500


@data_bp.route('/customer-data/<int:record_id>', methods=['GET'])
@jwt_required()
def get_customer_data_by_id(record_id):
    """Get a single customer data record by ID"""
    try:
        record = CustomerData.query.get(record_id)
        
        if not record:
            return jsonify({
                'success': False,
                'message': 'Record not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Record retrieved successfully',
            'data': record.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving record: {str(e)}'
        }), 500


@data_bp.route('/customer-data', methods=['POST'])
@jwt_required()
def create_customer_data():
    """Create a new customer data record"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Create new record
        new_record = CustomerData(
            user_id=data.get('user_id'),
            customer_name=data.get('customer_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            date_of_birth=data.get('date_of_birth'),
            blood_group=data.get('blood_group'),
            nationality=data.get('nationality'),
            marital_status=data.get('marital_status'),
            spouse_name=data.get('spouse_name'),
            children_count=data.get('children_count', 0),
            emergency_contact=data.get('emergency_contact'),
            current_address=data.get('current_address'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country'),
            credit_card_no=data.get('credit_card_no'),
            account_balance=data.get('account_balance', 0.0),
            account_type=data.get('account_type'),
            bank=data.get('bank'),
            bank_name=data.get('bank_name'),
            bank_account_no=data.get('bank_account_no'),
            ifsc_code=data.get('ifsc_code'),
            branch_name=data.get('branch_name'),
            pan_number=data.get('pan_number'),
            aadhar_number=data.get('aadhar_number'),
            annual_income=data.get('annual_income'),
            tax_regime=data.get('tax_regime'),
            insurance_policy_no=data.get('insurance_policy_no'),
            employee_id=data.get('employee_id'),
            department=data.get('department'),
            status=data.get('status'),
            salary=data.get('salary'),
            hire_date=data.get('hire_date'),
            manager_name=data.get('manager_name'),
            work_location=data.get('work_location'),
            remote_work_eligible=data.get('remote_work_eligible'),
            project_name=data.get('project_name'),
            project_code=data.get('project_code'),
            cycle_name=data.get('cycle_name'),
            skill_set=data.get('skill_set'),
            experience_years=data.get('experience_years'),
            education=data.get('education'),
            certification=data.get('certification'),
            performance_rating=data.get('performance_rating'),
            last_appraisal_date=data.get('last_appraisal_date'),
            next_appraisal_date=data.get('next_appraisal_date'),
            vehicle_type=data.get('vehicle_type'),
            vehicle_number=data.get('vehicle_number'),
            registration_date=data.get('registration_date'),
            last_login=data.get('last_login'),
            notes=data.get('notes'),
            created_by=current_user.get('username', 'system'),
            updated_by=current_user.get('username', 'system')
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Record created successfully',
            'data': new_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating record: {str(e)}'
        }), 500


@data_bp.route('/customer-data/<int:record_id>', methods=['PUT'])
@jwt_required()
def update_customer_data(record_id):
    """Update an existing customer data record"""
    try:
        current_user_id = get_jwt_identity()
        # Get user object to retrieve username
        user = User.query.get(int(current_user_id))
        
        record = CustomerData.query.get(record_id)
        
        if not record:
            return jsonify({
                'success': False,
                'message': 'Record not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields
        for key, value in data.items():
            if hasattr(record, key) and key not in ['id', 'created_at', 'created_by']:
                setattr(record, key, value)
        
        record.updated_by = user.username if user else 'system'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Record updated successfully',
            'data': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating record: {str(e)}'
        }), 500


@data_bp.route('/customer-data/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_customer_data(record_id):
    """Delete a customer data record"""
    try:
        record = CustomerData.query.get(record_id)
        
        if not record:
            return jsonify({
                'success': False,
                'message': 'Record not found'
            }), 404
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Record deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting record: {str(e)}'
        }), 500


@data_bp.route('/customer-data/bulk', methods=['POST'])
@jwt_required()
def bulk_create_customer_data():
    """Bulk create customer data records"""
    try:
        current_user = get_jwt_identity()
        data_list = request.get_json()
        
        if not isinstance(data_list, list):
            return jsonify({
                'success': False,
                'message': 'Expected a list of records'
            }), 400
        
        created_records = []
        
        for data in data_list:
            new_record = CustomerData(
                user_id=data.get('user_id'),
                customer_name=data.get('customer_name'),
                email=data.get('email'),
                phone_number=data.get('phone_number'),
                created_by=current_user.get('username', 'system'),
                updated_by=current_user.get('username', 'system'),
                **{k: v for k, v in data.items() if k not in ['user_id', 'customer_name', 'email', 'phone_number']}
            )
            db.session.add(new_record)
            created_records.append(new_record)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully created {len(created_records)} records',
            'data': [record.to_dict() for record in created_records]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating records: {str(e)}'
        }), 500


@data_bp.route('/customer-data/filters', methods=['GET'])
@jwt_required()
def get_filter_options():
    """Get distinct values for filter fields"""
    try:
        # Get distinct values for common filter fields
        departments = db.session.query(CustomerData.department).distinct().all()
        statuses = db.session.query(CustomerData.status).distinct().all()
        cities = db.session.query(CustomerData.city).distinct().all()
        states = db.session.query(CustomerData.state).distinct().all()
        banks = db.session.query(CustomerData.bank).distinct().all()
        cycles = db.session.query(CustomerData.cycle_name).distinct().all()
        
        return jsonify({
            'success': True,
            'message': 'Filter options retrieved successfully',
            'data': {
                'departments': [d[0] for d in departments if d[0]],
                'statuses': [s[0] for s in statuses if s[0]],
                'cities': [c[0] for c in cities if c[0]],
                'states': [s[0] for s in states if s[0]],
                'banks': [b[0] for b in banks if b[0]],
                'cycles': [c[0] for c in cycles if c[0]]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving filter options: {str(e)}'
        }), 500


@data_bp.route('/cycles', methods=['GET'])
@jwt_required()
def get_cycles():
    """Return list of cycles from Cycle model"""
    try:
        cycles = Cycle.query.order_by(Cycle.start_date.desc()).all()
        return jsonify({
            'success': True,
            'message': 'Cycles retrieved successfully',
            'data': [c.to_dict() for c in cycles]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving cycles: {str(e)}'
        }), 500


@data_bp.route('/cycles/public', methods=['GET'])
def get_cycles_public():
    """Return list of cycles (public endpoint, no authentication required)"""
    try:
        cycles = Cycle.query.order_by(Cycle.start_date.desc()).all()
        return jsonify({
            'success': True,
            'message': 'Public cycles retrieved successfully',
            'data': [c.to_dict() for c in cycles]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving public cycles: {str(e)}'
        }), 500
