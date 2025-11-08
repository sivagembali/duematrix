"""
Seed script to populate column_headers table with comprehensive mock data
This script inserts headers for all available roles from the mock-data.service.ts
"""

from app import create_app
from models import db, ColumnHeader, RoleMaster
from datetime import datetime

def get_all_roles():
    """Get all available roles from the database"""
    roles = RoleMaster.query.filter_by(is_active=True).all()
    return roles

def seed_comprehensive_headers():
    """Insert comprehensive header data for all roles"""
    app = create_app()
    
    with app.app_context():
        # Get all active roles
        roles = get_all_roles()
        print(f"\nFound {len(roles)} active roles:")
        for role in roles:
            print(f"  - {role.role_name} (ID: {role.id})")
        
        # Clear existing headers
        print("\nClearing existing headers...")
        ColumnHeader.query.delete()
        db.session.commit()
        
        # Define comprehensive headers from mock-data.service.ts
        base_headers = [
            {'col_header': 'id', 'col_label': 'ID', 'is_editable': False, 'is_multi_select': False, 'col_width': 5, 'display': True, 'default_display': True, 'is_frozen': True, 'display_order': 1},
            {'col_header': 'customer_name', 'col_label': 'Customer Name', 'is_editable': False, 'is_multi_select': True, 'col_width': 15, 'display': True, 'default_display': True, 'is_frozen': True, 'display_order': 2},
            {'col_header': 'credit_card_no', 'col_label': 'Credit Card No', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': True, 'is_frozen': True, 'display_order': 3},
            {'col_header': 'current_address', 'col_label': 'Current Address', 'is_editable': True, 'is_multi_select': False, 'col_width': 20, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 4},
            {'col_header': 'email', 'col_label': 'Email', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 5},
            {'col_header': 'phone_number', 'col_label': 'Phone Number', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 6},
            {'col_header': 'date_of_birth', 'col_label': 'Date of Birth', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 7},
            {'col_header': 'city', 'col_label': 'City', 'is_editable': True, 'is_multi_select': True, 'col_width': 10, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 8},
            {'col_header': 'state', 'col_label': 'State', 'is_editable': True, 'is_multi_select': True, 'col_width': 10, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 9},
            {'col_header': 'postal_code', 'col_label': 'Postal Code', 'is_editable': True, 'is_multi_select': False, 'col_width': 8, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 10},
            {'col_header': 'country', 'col_label': 'Country', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 11},
            {'col_header': 'account_balance', 'col_label': 'Account Balance', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 12},
            {'col_header': 'account_type', 'col_label': 'Account Type', 'is_editable': True, 'is_multi_select': True, 'col_width': 12, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 13},
            {'col_header': 'registration_date', 'col_label': 'Registration Date', 'is_editable': False, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 14},
            {'col_header': 'last_login', 'col_label': 'Last Login', 'is_editable': False, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 15},
            {'col_header': 'status', 'col_label': 'Status', 'is_editable': True, 'is_multi_select': True, 'col_width': 10, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 16},
            {'col_header': 'department', 'col_label': 'Department', 'is_editable': True, 'is_multi_select': True, 'col_width': 12, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 17},
            {'col_header': 'employee_id', 'col_label': 'Employee ID', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 18},
            {'col_header': 'salary', 'col_label': 'Salary', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': True, 'is_frozen': False, 'display_order': 19},
            {'col_header': 'hire_date', 'col_label': 'Hire Date', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 20},
            {'col_header': 'manager_name', 'col_label': 'Manager Name', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 21},
            {'col_header': 'project_name', 'col_label': 'Project Name', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 22},
            {'col_header': 'project_code', 'col_label': 'Project Code', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 23},
            {'col_header': 'skill_set', 'col_label': 'Skill Set', 'is_editable': True, 'is_multi_select': True, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 24},
            {'col_header': 'experience_years', 'col_label': 'Experience (Years)', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 25},
            {'col_header': 'education', 'col_label': 'Education', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 26},
            {'col_header': 'certification', 'col_label': 'Certification', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 27},
            {'col_header': 'emergency_contact', 'col_label': 'Emergency Contact', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 28},
            {'col_header': 'blood_group', 'col_label': 'Blood Group', 'is_editable': True, 'is_multi_select': True, 'col_width': 8, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 29},
            {'col_header': 'nationality', 'col_label': 'Nationality', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 30},
            {'col_header': 'marital_status', 'col_label': 'Marital Status', 'is_editable': True, 'is_multi_select': True, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 31},
            {'col_header': 'spouse_name', 'col_label': 'Spouse Name', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 32},
            {'col_header': 'children_count', 'col_label': 'Children Count', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 33},
            {'col_header': 'vehicle_type', 'col_label': 'Vehicle Type', 'is_editable': True, 'is_multi_select': True, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 34},
            {'col_header': 'vehicle_number', 'col_label': 'Vehicle Number', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 35},
            {'col_header': 'insurance_policy_no', 'col_label': 'Insurance Policy No', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 36},
            {'col_header': 'pan_number', 'col_label': 'PAN Number', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 37},
            {'col_header': 'aadhar_number', 'col_label': 'Aadhar Number', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 38},
            {'col_header': 'bank_name', 'col_label': 'Bank Name', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 39},
            {'col_header': 'bank_account_no', 'col_label': 'Bank Account No', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 40},
            {'col_header': 'ifsc_code', 'col_label': 'IFSC Code', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 41},
            {'col_header': 'branch_name', 'col_label': 'Branch Name', 'is_editable': True, 'is_multi_select': False, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 42},
            {'col_header': 'annual_income', 'col_label': 'Annual Income', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 43},
            {'col_header': 'tax_regime', 'col_label': 'Tax Regime', 'is_editable': True, 'is_multi_select': True, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 44},
            {'col_header': 'performance_rating', 'col_label': 'Performance Rating', 'is_editable': True, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 45},
            {'col_header': 'last_appraisal_date', 'col_label': 'Last Appraisal Date', 'is_editable': False, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 46},
            {'col_header': 'next_appraisal_date', 'col_label': 'Next Appraisal Date', 'is_editable': False, 'is_multi_select': False, 'col_width': 12, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 47},
            {'col_header': 'work_location', 'col_label': 'Work Location', 'is_editable': True, 'is_multi_select': True, 'col_width': 15, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 48},
            {'col_header': 'remote_work_eligible', 'col_label': 'Remote Work Eligible', 'is_editable': True, 'is_multi_select': False, 'col_width': 10, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 49},
            {'col_header': 'notes', 'col_label': 'Notes', 'is_editable': True, 'is_multi_select': False, 'col_width': 20, 'display': True, 'default_display': False, 'is_frozen': False, 'display_order': 50}
        ]
        
        # Strategy: Insert all headers with role_id=None (available to all roles)
        # The API will filter based on user's role if needed
        
        headers_created = 0
        
        print("\n" + "="*80)
        print("INSERTING HEADERS")
        print("="*80)
        
        # Insert all headers as common/generic (available to all roles)
        print(f"\nInserting all {len(base_headers)} headers (available to all roles)...")
        for header_data in base_headers:
            header_data['role_id'] = None  # Available to all roles
            header_data['created_by'] = 'system'
            header_data['updated_by'] = 'system'
            
            header = ColumnHeader.from_dict(header_data)
            db.session.add(header)
            headers_created += 1
        
        db.session.commit()
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✓ Successfully inserted {headers_created} column headers")
        print(f"\nAll headers are available to all roles (role_id = NULL)")
        print(f"The API can filter headers based on business logic if needed")
        
        # Verify counts
        print("\n" + "="*80)
        print("VERIFICATION")
        print("="*80)
        total_headers = ColumnHeader.query.count()
        default_headers = ColumnHeader.query.filter_by(default_display=True).count()
        print(f"  - Total headers: {total_headers}")
        print(f"  - Default display headers: {default_headers}")
        print(f"  - Available to all roles: {total_headers}")

if __name__ == '__main__':
    seed_comprehensive_headers()
