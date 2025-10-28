from app import create_app, db
from app.models.header_config import HeaderConfig
from datetime import datetime

def init_header_configurations():
    """Initialize default header configurations for all credit bill columns"""
    app = create_app()
    
    with app.app_context():
        # Check if configurations already exist
        if HeaderConfig.query.first():
            print("⚠️  Header configurations already exist. Skipping...")
            return
        
        # Default column configurations for all 42 columns
        default_configs = [
            {
                'col_name': 's_no',
                'label': 'S/NO',
                'status': True,
                'data_type': 'number',
                'width': 50,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 1,
                'multi_select_filter': []
            },
            {
                'col_name': 'card_no',
                'label': 'CARD NO',
                'status': True,
                'data_type': 'text',
                'width': 140,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 2,
                'multi_select_filter': []
            },
            {
                'col_name': 'cum_name',
                'label': 'CUM NAME',
                'status': True,
                'data_type': 'text',
                'width': 120,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 3,
                'multi_select_filter': []
            },
            {
                'col_name': 'card_limit',
                'label': 'CARD LIMIT',
                'status': True,
                'data_type': 'currency',
                'width': 100,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 4,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'tos',
                'label': 'TOS',
                'status': True,
                'data_type': 'text',
                'width': 70,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 5,
                'multi_select_filter': ['TOS001', 'TOS002', 'TOS003', 'TOS004', 'TOS005']
            },
            {
                'col_name': 'pos',
                'label': 'POS',
                'status': True,
                'data_type': 'text',
                'width': 70,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 6,
                'multi_select_filter': ['POS001', 'POS002', 'POS003', 'POS004', 'POS005']
            },
            {
                'col_name': 'tad',
                'label': 'TAD',
                'status': True,
                'data_type': 'currency',
                'width': 80,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 7,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'norm',
                'label': 'NORM',
                'status': True,
                'data_type': 'currency',
                'width': 80,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 8,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'rb',
                'label': 'RB',
                'status': True,
                'data_type': 'currency',
                'width': 70,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 9,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'stab',
                'label': 'STAB',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 10,
                'multi_select_filter': ['STABLE', 'UNSTABLE', 'CRITICAL']
            },
            {
                'col_name': 'emi',
                'label': 'EMI',
                'status': True,
                'data_type': 'currency',
                'width': 70,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 11,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'principle',
                'label': 'PRINCIPLE',
                'status': True,
                'data_type': 'currency',
                'width': 90,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 12,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'mobile',
                'label': 'MOBILE',
                'status': True,
                'data_type': 'text',
                'width': 100,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 13,
                'multi_select_filter': []
            },
            {
                'col_name': 'per_percent',
                'label': 'PER %',
                'status': True,
                'data_type': 'percentage',
                'width': 60,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 14,
                'format_options': {'decimal_places': 1},
                'multi_select_filter': []
            },
            {
                'col_name': 'block',
                'label': 'BLOCK',
                'status': True,
                'data_type': 'text',
                'width': 70,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 15,
                'multi_select_filter': ['YES', 'NO']
            },
            {
                'col_name': 'cycle',
                'label': 'CYCLE',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 16,
                'multi_select_filter': ['1st', '5th', '10th', '15th', '20th', '25th', 'MONTHLY']
            },
            {
                'col_name': 'emp_name',
                'label': 'EMP NAME',
                'status': True,
                'data_type': 'text',
                'width': 120,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 17,
                'multi_select_filter': []
            },
            {
                'col_name': 'paid_unpaid',
                'label': 'PAID/UNPAID',
                'status': True,
                'data_type': 'text',
                'width': 100,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 18,
                'multi_select_filter': ['PAID', 'UNPAID']
            },
            {
                'col_name': 'status',
                'label': 'STATUS',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 19,
                'multi_select_filter': ['ACTIVE', 'INACTIVE', 'BLOCKED', 'OVERDUE', 'CURRENT']
            },
            {
                'col_name': 'contact_status',
                'label': 'CONTACT STATUS',
                'status': True,
                'data_type': 'text',
                'width': 120,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 20,
                'multi_select_filter': ['CONTACTED', 'NOT REACHABLE', 'PROMISED TO PAY', 'CONNECTED', 'RINGING', 'PENDING']
            },
            {
                'col_name': 'mis',
                'label': 'MIS',
                'status': True,
                'data_type': 'text',
                'width': 70,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 21,
                'multi_select_filter': []
            },
            {
                'col_name': 'remarks',
                'label': 'REMARKS',
                'status': True,
                'data_type': 'text',
                'width': 150,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 22,
                'multi_select_filter': []
            },
            {
                'col_name': 'ptp_date',
                'label': 'PTP DATE',
                'status': True,
                'data_type': 'date',
                'width': 90,
                'sortable': True,
                'searchable': False,
                'filter_type': 'date_range',
                'display_order': 23,
                'format_options': {'date_format': 'YYYY-MM-DD'},
                'multi_select_filter': []
            },
            {
                'col_name': 'ptp_amount',
                'label': 'PTP AMOUNT',
                'status': True,
                'data_type': 'currency',
                'width': 100,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 24,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'paid_date',
                'label': 'PAID DATE',
                'status': True,
                'data_type': 'date',
                'width': 90,
                'sortable': True,
                'searchable': False,
                'filter_type': 'date_range',
                'display_order': 25,
                'format_options': {'date_format': 'YYYY-MM-DD'},
                'multi_select_filter': []
            },
            {
                'col_name': 'paid_amount',
                'label': 'PAID AMOUNT',
                'status': True,
                'data_type': 'currency',
                'width': 100,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 26,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'new_numbers',
                'label': 'NEW NUMBERS',
                'status': True,
                'data_type': 'text',
                'width': 120,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 27,
                'multi_select_filter': []
            },
            {
                'col_name': 'new_address',
                'label': 'NEW ADDRESS',
                'status': True,
                'data_type': 'text',
                'width': 150,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 28,
                'multi_select_filter': []
            },
            {
                'col_name': 'mode_of_payment',
                'label': 'MODE OF PAYMENT',
                'status': True,
                'data_type': 'text',
                'width': 100,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 29,
                'multi_select_filter': ['NEFT', 'UPI', 'CHEQUE', 'CASH', 'NET BANKING', 'ONLINE']
            },
            {
                'col_name': 'receipt',
                'label': 'RECEIPT',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 30,
                'multi_select_filter': []
            },
            {
                'col_name': 'projection',
                'label': 'PROJECTION',
                'status': True,
                'data_type': 'text',
                'width': 90,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 31,
                'multi_select_filter': ['POSITIVE', 'NEGATIVE', 'GOOD', 'CRITICAL', 'EXCELLENT']
            },
            {
                'col_name': 'manager',
                'label': 'MANAGER',
                'status': True,
                'data_type': 'text',
                'width': 100,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 32,
                'multi_select_filter': []
            },
            {
                'col_name': 'areas',
                'label': 'AREAS',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 33,
                'multi_select_filter': ['Bangalore North', 'Mumbai Central', 'Delhi NCR', 'Chennai South', 'Hyderabad West', 'CENTRAL']
            },
            {
                'col_name': 'add1',
                'label': 'ADD1',
                'status': True,
                'data_type': 'text',
                'width': 120,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 34,
                'multi_select_filter': []
            },
            {
                'col_name': 'add2',
                'label': 'ADD2',
                'status': True,
                'data_type': 'text',
                'width': 120,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 35,
                'multi_select_filter': []
            },
            {
                'col_name': 'work_address',
                'label': 'WORK ADDRESS',
                'status': True,
                'data_type': 'text',
                'width': 140,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 36,
                'multi_select_filter': []
            },
            {
                'col_name': 'pincode',
                'label': 'PINCODE',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': True,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 37,
                'multi_select_filter': []
            },
            {
                'col_name': 'permanent_address',
                'label': 'PERMANENT ADDRESS',
                'status': True,
                'data_type': 'text',
                'width': 140,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 38,
                'multi_select_filter': []
            },
            {
                'col_name': 'history',
                'label': 'HISTORY',
                'status': True,
                'data_type': 'text',
                'width': 80,
                'sortable': False,
                'searchable': True,
                'filter_type': 'text',
                'display_order': 39,
                'multi_select_filter': []
            },
            {
                'col_name': 'pnpa',
                'label': 'PNPA',
                'status': True,
                'data_type': 'text',
                'width': 70,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 40,
                'multi_select_filter': ['PTP', 'PAID', 'NPA', 'CURRENT']
            },
            {
                'col_name': 'principal',
                'label': 'PRINCIPAL',
                'status': True,
                'data_type': 'currency',
                'width': 90,
                'sortable': True,
                'searchable': False,
                'filter_type': 'number_range',
                'display_order': 41,
                'format_options': {'currency': 'INR', 'decimal_places': 2},
                'multi_select_filter': []
            },
            {
                'col_name': 'on_field',
                'label': 'O/N',
                'status': True,
                'data_type': 'text',
                'width': 60,
                'sortable': True,
                'searchable': True,
                'filter_type': 'select',
                'display_order': 42,
                'multi_select_filter': ['Y', 'N', 'YES', 'NO']
            }
        ]
        
        # Insert configurations
        configs_created = 0
        for config_data in default_configs:
            config = HeaderConfig(
                col_name=config_data['col_name'],
                label=config_data['label'],
                status=config_data['status'],
                data_type=config_data['data_type'],
                width=config_data['width'],
                sortable=config_data['sortable'],
                searchable=config_data['searchable'],
                filter_type=config_data['filter_type'],
                display_order=config_data['display_order'],
                multi_select_filter=config_data['multi_select_filter'],
                format_options=config_data.get('format_options', {}),
                created_by='system'
            )
            db.session.add(config)
            configs_created += 1
        
        try:
            db.session.commit()
            print(f"✅ Successfully created {configs_created} header configurations!")
            print("\n📊 Header Configuration Summary:")
            print(f"   • Total columns configured: {configs_created}")
            print(f"   • Visible columns: {len([c for c in default_configs if c['status']])}")
            print(f"   • Sortable columns: {len([c for c in default_configs if c['sortable']])}")
            print(f"   • Searchable columns: {len([c for c in default_configs if c['searchable']])}")
            print(f"   • Columns with filters: {len([c for c in default_configs if c['multi_select_filter']])}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating header configurations: {str(e)}")

if __name__ == '__main__':
    init_header_configurations()