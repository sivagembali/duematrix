"""
Customer Data Model
Represents comprehensive customer/employee data for the dashboard
"""

from . import db
from datetime import datetime


class CustomerData(db.Model):
    """Model for storing customer/employee data records"""
    
    __tablename__ = 'customer_data'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Personal Information
    customer_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=True)
    blood_group = db.Column(db.String(10), nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    spouse_name = db.Column(db.String(255), nullable=True)
    children_count = db.Column(db.Integer, default=0)
    emergency_contact = db.Column(db.String(20), nullable=True)
    
    # Address Information
    current_address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    
    # Financial Information
    credit_card_no = db.Column(db.String(20), nullable=True)
    account_balance = db.Column(db.Float, default=0.0)
    account_type = db.Column(db.String(50), nullable=True)
    bank = db.Column(db.String(255), nullable=True)
    bank_name = db.Column(db.String(255), nullable=True)
    bank_account_no = db.Column(db.String(50), nullable=True)
    ifsc_code = db.Column(db.String(20), nullable=True)
    branch_name = db.Column(db.String(255), nullable=True)
    pan_number = db.Column(db.String(20), nullable=True)
    aadhar_number = db.Column(db.String(20), nullable=True)
    annual_income = db.Column(db.Float, nullable=True)
    tax_regime = db.Column(db.String(50), nullable=True)
    insurance_policy_no = db.Column(db.String(50), nullable=True)
    
    # Employment Information
    employee_id = db.Column(db.String(20), nullable=True, unique=True)
    department = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.Float, nullable=True)
    hire_date = db.Column(db.String(20), nullable=True)
    manager_name = db.Column(db.String(255), nullable=True)
    work_location = db.Column(db.String(255), nullable=True)
    remote_work_eligible = db.Column(db.String(10), nullable=True)
    
    # Project Information
    project_name = db.Column(db.String(255), nullable=True)
    project_code = db.Column(db.String(50), nullable=True)
    cycle_name = db.Column(db.String(100), nullable=True)
    
    # Skills and Education
    skill_set = db.Column(db.String(500), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    education = db.Column(db.String(255), nullable=True)
    certification = db.Column(db.String(255), nullable=True)
    
    # Performance
    performance_rating = db.Column(db.Float, nullable=True)
    last_appraisal_date = db.Column(db.String(20), nullable=True)
    next_appraisal_date = db.Column(db.String(20), nullable=True)
    
    # Vehicle Information
    vehicle_type = db.Column(db.String(50), nullable=True)
    vehicle_number = db.Column(db.String(50), nullable=True)
    
    # System Fields
    registration_date = db.Column(db.String(20), nullable=True)
    last_login = db.Column(db.String(30), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100), nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='customer_data_records', lazy=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'customer_name': self.customer_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth,
            'blood_group': self.blood_group,
            'nationality': self.nationality,
            'marital_status': self.marital_status,
            'spouse_name': self.spouse_name,
            'children_count': self.children_count,
            'emergency_contact': self.emergency_contact,
            'current_address': self.current_address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'credit_card_no': self.credit_card_no,
            'account_balance': self.account_balance,
            'account_type': self.account_type,
            'bank': self.bank,
            'bank_name': self.bank_name,
            'bank_account_no': self.bank_account_no,
            'ifsc_code': self.ifsc_code,
            'branch_name': self.branch_name,
            'pan_number': self.pan_number,
            'aadhar_number': self.aadhar_number,
            'annual_income': self.annual_income,
            'tax_regime': self.tax_regime,
            'insurance_policy_no': self.insurance_policy_no,
            'employee_id': self.employee_id,
            'department': self.department,
            'status': self.status,
            'salary': self.salary,
            'hire_date': self.hire_date,
            'manager_name': self.manager_name,
            'work_location': self.work_location,
            'remote_work_eligible': self.remote_work_eligible,
            'project_name': self.project_name,
            'project_code': self.project_code,
            'cycle_name': self.cycle_name,
            'skill_set': self.skill_set,
            'experience_years': self.experience_years,
            'education': self.education,
            'certification': self.certification,
            'performance_rating': self.performance_rating,
            'last_appraisal_date': self.last_appraisal_date,
            'next_appraisal_date': self.next_appraisal_date,
            'vehicle_type': self.vehicle_type,
            'vehicle_number': self.vehicle_number,
            'registration_date': self.registration_date,
            'last_login': self.last_login,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
    
    def __repr__(self):
        return f'<CustomerData {self.id}: {self.customer_name}>'
