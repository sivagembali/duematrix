"""
Seed script to populate column_headers table with dummy data
Run this script to insert sample header configurations
"""

from app import create_app
from models import db, ColumnHeader
from datetime import datetime

def seed_headers():
    """Insert dummy header data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing headers (optional - comment out if you want to keep existing data)
        print("Clearing existing headers...")
        ColumnHeader.query.delete()
        
        # Define dummy headers for a project/task management system
        headers_data = [
            {
                'col_header': 'task_id',
                'col_label': 'Task ID',
                'is_editable': False,
                'is_multi_select': False,
                'col_width': 8.0,
                'display': True,
                'default_display': True,
                'is_frozen': True,
                'display_order': 1,
                'role_id': None,  # Available to all roles
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'task_name',
                'col_label': 'Task Name',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 20.0,
                'display': True,
                'default_display': True,
                'is_frozen': False,
                'display_order': 2,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'assigned_to',
                'col_label': 'Assigned To',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 15.0,
                'display': True,
                'default_display': True,
                'is_frozen': False,
                'display_order': 3,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'status',
                'col_label': 'Status',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 12.0,
                'display': True,
                'default_display': True,
                'is_frozen': False,
                'display_order': 4,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'priority',
                'col_label': 'Priority',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 10.0,
                'display': True,
                'default_display': True,
                'is_frozen': False,
                'display_order': 5,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'due_date',
                'col_label': 'Due Date',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 12.0,
                'display': True,
                'default_display': True,
                'is_frozen': False,
                'display_order': 6,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'progress',
                'col_label': 'Progress %',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 10.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 7,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'category',
                'col_label': 'Category',
                'is_editable': True,
                'is_multi_select': True,
                'col_width': 15.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 8,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'description',
                'col_label': 'Description',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 25.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 9,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'estimated_hours',
                'col_label': 'Est. Hours',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 10.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 10,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'actual_hours',
                'col_label': 'Actual Hours',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 10.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 11,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'created_date',
                'col_label': 'Created Date',
                'is_editable': False,
                'is_multi_select': False,
                'col_width': 12.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 12,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'tags',
                'col_label': 'Tags',
                'is_editable': True,
                'is_multi_select': True,
                'col_width': 15.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 13,
                'role_id': None,
                'created_by': 'system',
                'updated_by': 'system'
            },
            # Admin-only columns
            {
                'col_header': 'cost',
                'col_label': 'Cost',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 10.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 14,
                'role_id': 1,  # Admin role only
                'created_by': 'system',
                'updated_by': 'system'
            },
            {
                'col_header': 'budget',
                'col_label': 'Budget',
                'is_editable': True,
                'is_multi_select': False,
                'col_width': 10.0,
                'display': True,
                'default_display': False,
                'is_frozen': False,
                'display_order': 15,
                'role_id': 1,  # Admin role only
                'created_by': 'system',
                'updated_by': 'system'
            }
        ]
        
        # Insert headers
        print("Inserting headers...")
        for header_data in headers_data:
            header = ColumnHeader.from_dict(header_data)
            db.session.add(header)
        
        db.session.commit()
        print(f"✓ Successfully inserted {len(headers_data)} column headers")
        
        # Display summary
        print("\nHeaders Summary:")
        print(f"- Total headers: {len(headers_data)}")
        print(f"- Default display headers: {sum(1 for h in headers_data if h['default_display'])}")
        print(f"- Admin-only headers: {sum(1 for h in headers_data if h['role_id'] == 1)}")
        print(f"- Generic headers: {sum(1 for h in headers_data if h['role_id'] is None)}")

if __name__ == '__main__':
    seed_headers()
