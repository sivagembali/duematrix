from app import create_app, db
from app.models.credit_bill import CreditBill
from app.models.header_config import HeaderConfig
from datetime import datetime

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables (credit_bills and header_config)
        db.create_all()
        print("✅ Database tables created successfully!")
        print("   • credit_bills table")
        print("   • header_config table")
        
        # Check if data already exists
        if CreditBill.query.first():
            print("⚠️  Sample data already exists. Skipping...")
            return
        
        # Create sample data matching the frontend structure
        sample_bills = [
            {
                's_no': 1,
                'card_no': '4532-1234-5678-9012',
                'cum_name': 'Rajesh Kumar',
                'card_limit': 150000.00,
                'tos': '90',
                'pos': '60',
                'tad': 45000.00,
                'norm': 12000.00,
                'rb': 8500.00,
                'stab': 'STABLE',
                'emi': 5500.00,
                'principle': 42000.00,
                'mobile': '9876543210',
                'per_percent': 28.0,
                'block': 'NO',
                'cycle': '15th',
                'emp_name': 'Amit Sharma',
                'paid_unpaid': 'UNPAID',
                'status': 'ACTIVE',
                'contact_status': 'CONTACTED',
                'mis': 'MIS001',
                'remarks': 'Customer requesting payment extension due to medical emergency',
                'ptp_date': '2025-10-25',
                'ptp_amount': 15000.00,
                'paid_date': '',
                'paid_amount': 0.00,
                'new_numbers': '9876543211',
                'new_address': 'New: 123 Tech Park, Bangalore',
                'mode_of_payment': 'NEFT',
                'receipt': 'RCP001',
                'projection': 'POSITIVE',
                'manager': 'Priya Singh',
                'areas': 'Bangalore North',
                'add1': '456 MG Road',
                'add2': 'Koramangala',
                'work_address': '789 IT Park, Electronic City',
                'pincode': '560034',
                'permanent_address': '321 Home Street, Mysore, Karnataka',
                'history': 'Good payment history until recent delays',
                'pnpa': 'PTP',
                'principal': 42000.00,
                'on_field': 'Y'
            },
            {
                's_no': 2,
                'card_no': '5678-9012-3456-7890',
                'cum_name': 'Priya Patel',
                'card_limit': 200000.00,
                'tos': '45',
                'pos': '30',
                'tad': 75000.00,
                'norm': 25000.00,
                'rb': 18500.00,
                'stab': 'UNSTABLE',
                'emi': 8200.00,
                'principle': 68000.00,
                'mobile': '9123456789',
                'per_percent': 34.0,
                'block': 'YES',
                'cycle': '5th',
                'emp_name': 'Vikram Reddy',
                'paid_unpaid': 'PAID',
                'status': 'BLOCKED',
                'contact_status': 'NOT REACHABLE',
                'mis': 'MIS002',
                'remarks': 'Card blocked due to suspicious transactions',
                'ptp_date': '2025-10-20',
                'ptp_amount': 25000.00,
                'paid_date': '2025-10-18',
                'paid_amount': 25000.00,
                'new_numbers': '',
                'new_address': '',
                'mode_of_payment': 'UPI',
                'receipt': 'RCP002',
                'projection': 'NEGATIVE',
                'manager': 'Suresh Kumar',
                'areas': 'Mumbai Central',
                'add1': '789 Business District',
                'add2': 'Andheri West',
                'work_address': '456 Corporate Hub, BKC',
                'pincode': '400053',
                'permanent_address': '654 Family Home, Pune, Maharashtra',
                'history': 'Multiple late payments and overlimit usage',
                'pnpa': 'PAID',
                'principal': 68000.00,
                'on_field': 'N'
            },
            {
                's_no': 3,
                'card_no': '1234-5678-9012-3456',
                'cum_name': 'Mohammed Ali',
                'card_limit': 300000.00,
                'tos': '120',
                'pos': '90',
                'tad': 95000.00,
                'norm': 35000.00,
                'rb': 28500.00,
                'stab': 'STABLE',
                'emi': 12500.00,
                'principle': 85000.00,
                'mobile': '9988776655',
                'per_percent': 28.3,
                'block': 'NO',
                'cycle': '25th',
                'emp_name': 'Kavya Nair',
                'paid_unpaid': 'UNPAID',
                'status': 'ACTIVE',
                'contact_status': 'PROMISED TO PAY',
                'mis': 'MIS003',
                'remarks': 'Regular customer with good payment history',
                'ptp_date': '2025-10-30',
                'ptp_amount': 35000.00,
                'paid_date': '',
                'paid_amount': 0.00,
                'new_numbers': '9988776656',
                'new_address': 'Updated: 987 New Colony, Delhi',
                'mode_of_payment': 'CHEQUE',
                'receipt': 'RCP003',
                'projection': 'POSITIVE',
                'manager': 'Rahul Gupta',
                'areas': 'Delhi NCR',
                'add1': '123 Central Delhi',
                'add2': 'Karol Bagh',
                'work_address': '789 Business Centre, Connaught Place',
                'pincode': '110005',
                'permanent_address': '456 Ancestral Home, Lucknow, UP',
                'history': 'Consistent payments, premium customer',
                'pnpa': 'PTP',
                'principal': 85000.00,
                'on_field': 'Y'
            },
            {
                's_no': 4,
                'card_no': '9876-5432-1098-7654',
                'cum_name': 'Sunita Joshi',
                'card_limit': 100000.00,
                'tos': '180',
                'pos': '150',
                'tad': 32000.00,
                'norm': 8000.00,
                'rb': 5500.00,
                'stab': 'CRITICAL',
                'emi': 3200.00,
                'principle': 28000.00,
                'mobile': '9345678901',
                'per_percent': 32.0,
                'block': 'YES',
                'cycle': '10th',
                'emp_name': 'Deepak Singh',
                'paid_unpaid': 'UNPAID',
                'status': 'OVERDUE',
                'contact_status': 'RINGING',
                'mis': 'MIS004',
                'remarks': 'Account in critical status, legal notice issued',
                'ptp_date': '2025-10-22',
                'ptp_amount': 10000.00,
                'paid_date': '',
                'paid_amount': 0.00,
                'new_numbers': '',
                'new_address': '',
                'mode_of_payment': 'CASH',
                'receipt': 'RCP004',
                'projection': 'CRITICAL',
                'manager': 'Neha Agarwal',
                'areas': 'Chennai South',
                'add1': '567 T Nagar',
                'add2': 'Anna Salai',
                'work_address': '890 IT Corridor, OMR',
                'pincode': '600017',
                'permanent_address': '234 Native Place, Madurai, TN',
                'history': 'Multiple defaults, collection challenges',
                'pnpa': 'NPA',
                'principal': 28000.00,
                'on_field': 'Y'
            },
            {
                's_no': 5,
                'card_no': '3456-7890-1234-5678',
                'cum_name': 'Arjun Mehta',
                'card_limit': 250000.00,
                'tos': '30',
                'pos': '15',
                'tad': 125000.00,
                'norm': 45000.00,
                'rb': 35000.00,
                'stab': 'STABLE',
                'emi': 15000.00,
                'principle': 115000.00,
                'mobile': '9567890123',
                'per_percent': 46.0,
                'block': 'NO',
                'cycle': '1st',
                'emp_name': 'Pooja Verma',
                'paid_unpaid': 'PAID',
                'status': 'CURRENT',
                'contact_status': 'CONNECTED',
                'mis': 'MIS005',
                'remarks': 'High spender, premium segment customer',
                'ptp_date': '',
                'ptp_amount': 0.00,
                'paid_date': '2025-10-15',
                'paid_amount': 50000.00,
                'new_numbers': '',
                'new_address': '',
                'mode_of_payment': 'NET BANKING',
                'receipt': 'RCP005',
                'projection': 'EXCELLENT',
                'manager': 'Ravi Kumar',
                'areas': 'Hyderabad West',
                'add1': '890 Jubilee Hills',
                'add2': 'Banjara Hills',
                'work_address': '123 HITEC City, Madhapur',
                'pincode': '500033',
                'permanent_address': '567 Family Villa, Vijayawada, AP',
                'history': 'Excellent payment record, VIP customer',
                'pnpa': 'CURRENT',
                'principal': 115000.00,
                'on_field': 'N'
            }
        ]
        
        # Insert sample data
        for bill_data in sample_bills:
            bill = CreditBill(**bill_data)
            db.session.add(bill)
        
        try:
            db.session.commit()
            print(f"✅ Successfully inserted {len(sample_bills)} sample credit bills!")
            print("\n📊 Sample Data Summary:")
            print(f"   • Total bills: {len(sample_bills)}")
            print(f"   • Paid bills: {len([b for b in sample_bills if b['paid_unpaid'] == 'PAID'])}")
            print(f"   • Unpaid bills: {len([b for b in sample_bills if b['paid_unpaid'] == 'UNPAID'])}")
            print(f"   • Blocked cards: {len([b for b in sample_bills if b['block'] == 'YES'])}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error inserting sample data: {str(e)}")

if __name__ == '__main__':
    init_database()