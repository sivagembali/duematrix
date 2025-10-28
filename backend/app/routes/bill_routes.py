from flask import Blueprint, request, jsonify
from app import db
from app.models.credit_bill import CreditBill
from app.models.header_config import HeaderConfig
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Create Blueprint for bill routes
bills_bp = Blueprint('bills', __name__)

@bills_bp.route('/bills/with-config', methods=['GET'])
def get_bills_with_config():
    """Get all credit bills with their header configuration"""
    print("🔥 DEBUG: /bills/with-config endpoint called!")
    print(f"🔥 DEBUG: Query params: {dict(request.args)}")
    try:
        # Query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        search = request.args.get('search', '')
        status_filter = request.args.get('status', '')
        
        # Get header configurations ordered by display_order
        header_configs = HeaderConfig.query.filter(HeaderConfig.status == True).order_by(HeaderConfig.display_order).all()
        
        # Build query for bills
        query = CreditBill.query
        
        # Apply search filter if provided
        if search:
            query = query.filter(
                db.or_(
                    CreditBill.cum_name.ilike(f'%{search}%'),
                    CreditBill.card_no.ilike(f'%{search}%'),
                    CreditBill.mobile.ilike(f'%{search}%')
                )
            )
        
        # Apply status filter if provided
        if status_filter:
            query = query.filter(CreditBill.paid_unpaid == status_filter)
        
        # Apply pagination
        paginated_bills = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dict format
        bills_data = [bill.to_dict() for bill in paginated_bills.items]
        header_config_data = [config.to_dict() for config in header_configs]
        
        return jsonify({
            'success': True,
            'data': {
                'bills': bills_data,
                'headerConfig': header_config_data,
                'visibleColumns': [config.col_name for config in header_configs if config.status],
                'pagination': {
                    'page': page,
                    'perPage': per_page,
                    'total': paginated_bills.total,
                    'totalPages': paginated_bills.pages,
                    'hasNext': paginated_bills.has_next,
                    'hasPrev': paginated_bills.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch bills with configuration',
            'message': str(e)
        }), 500

@bills_bp.route('/bills', methods=['GET'])
def get_all_bills():
    """Get all credit bills with optional filtering and pagination"""
    print("🚨 DEBUG: /bills endpoint called!")
    print(f"🚨 DEBUG: Query params: {dict(request.args)}")
    try:
        # Query parameters for filtering and pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        search = request.args.get('search', '')
        status_filter = request.args.get('status', '')
        
        # Build query
        query = CreditBill.query
        
        # Apply search filter if provided
        if search:
            query = query.filter(
                db.or_(
                    CreditBill.cum_name.ilike(f'%{search}%'),
                    CreditBill.card_no.ilike(f'%{search}%'),
                    CreditBill.mobile.ilike(f'%{search}%')
                )
            )
        
        # Apply status filter if provided
        if status_filter:
            query = query.filter(CreditBill.paid_unpaid == status_filter)
        
        # Apply pagination
        paginated_bills = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dict format
        bills_data = [bill.to_dict() for bill in paginated_bills.items]
        
        return jsonify({
            'success': True,
            'data': bills_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated_bills.total,
                'pages': paginated_bills.pages,
                'has_next': paginated_bills.has_next,
                'has_prev': paginated_bills.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch bills',
            'message': str(e)
        }), 500

@bills_bp.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill_by_id(bill_id):
    """Get a specific credit bill by ID"""
    try:
        bill = CreditBill.query.get_or_404(bill_id)
        return jsonify({
            'success': True,
            'data': bill.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Bill not found',
            'message': str(e)
        }), 404

@bills_bp.route('/bills', methods=['POST'])
def create_bill():
    """Create a new credit bill"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Create new bill instance
        new_bill = CreditBill(
            s_no=data.get('sNo'),
            card_no=data.get('cardNo'),
            cum_name=data.get('cumName'),
            card_limit=data.get('cardLimit', 0.0),
            tos=data.get('tos'),
            pos=data.get('pos'),
            tad=data.get('tad', 0.0),
            norm=data.get('norm', 0.0),
            rb=data.get('rb', 0.0),
            stab=data.get('stab'),
            emi=data.get('emi', 0.0),
            principle=data.get('principle', 0.0),
            mobile=data.get('mobile'),
            per_percent=data.get('per', 0.0),
            block=data.get('block', 'NO'),
            cycle=data.get('cycle'),
            emp_name=data.get('empName'),
            paid_unpaid=data.get('paidUnpaid', 'UNPAID'),
            status=data.get('status'),
            contact_status=data.get('contactStatus'),
            mis=data.get('mis'),
            remarks=data.get('remarks'),
            ptp_date=data.get('ptpDate'),
            ptp_amount=data.get('ptpAmount', 0.0),
            paid_date=data.get('paidDate'),
            paid_amount=data.get('paidAmount', 0.0),
            new_numbers=data.get('newNumbers'),
            new_address=data.get('newAddress'),
            mode_of_payment=data.get('modeOfPayment'),
            receipt=data.get('receipt'),
            projection=data.get('projection'),
            manager=data.get('manager'),
            areas=data.get('areas'),
            add1=data.get('add1'),
            add2=data.get('add2'),
            work_address=data.get('workAddress'),
            pincode=data.get('pincode'),
            permanent_address=data.get('permanentAddress'),
            history=data.get('history'),
            pnpa=data.get('pnpa'),
            principal=data.get('principal', 0.0),
            on_field=data.get('on')
        )
        
        db.session.add(new_bill)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_bill.to_dict(),
            'message': 'Bill created successfully'
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Data integrity error',
            'message': 'Bill with this S/NO already exists or required field is missing'
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to create bill',
            'message': str(e)
        }), 500

@bills_bp.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    """Update an existing credit bill"""
    try:
        bill = CreditBill.query.get_or_404(bill_id)
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update bill fields
        for key, value in data.items():
            if hasattr(bill, key):
                setattr(bill, key, value)
        
        bill.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': bill.to_dict(),
            'message': 'Bill updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to update bill',
            'message': str(e)
        }), 500

@bills_bp.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    """Delete a credit bill"""
    try:
        bill = CreditBill.query.get_or_404(bill_id)
        db.session.delete(bill)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bill deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to delete bill',
            'message': str(e)
        }), 500

@bills_bp.route('/bills/stats', methods=['GET'])
def get_bills_stats():
    """Get statistics about credit bills"""
    print("📊 DEBUG: /bills/stats endpoint called!")
    try:
        total_bills = CreditBill.query.count()
        paid_bills = CreditBill.query.filter(CreditBill.paid_unpaid == 'PAID').count()
        unpaid_bills = CreditBill.query.filter(CreditBill.paid_unpaid == 'UNPAID').count()
        blocked_bills = CreditBill.query.filter(CreditBill.block == 'YES').count()
        
        total_card_limit = db.session.query(db.func.sum(CreditBill.card_limit)).scalar() or 0
        total_outstanding = db.session.query(db.func.sum(CreditBill.principal)).scalar() or 0
        total_paid_amount = db.session.query(db.func.sum(CreditBill.paid_amount)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'totalBills': total_bills,
                'paidBills': paid_bills,
                'unpaidBills': unpaid_bills,
                'blockedBills': blocked_bills,
                'totalCardLimit': total_card_limit,
                'totalOutstanding': total_outstanding,
                'totalPaidAmount': total_paid_amount,
                'paymentRate': round((paid_bills / total_bills * 100), 2) if total_bills > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch statistics',
            'message': str(e)
        }), 500