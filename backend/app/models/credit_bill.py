from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Text

class CreditBill(db.Model):
    """Credit Bill model matching the frontend table structure"""
    __tablename__ = 'credit_bills'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # All 42 columns from the frontend table
    s_no = Column(Integer, nullable=False, unique=True)
    card_no = Column(String(20), nullable=False)
    cum_name = Column(String(100), nullable=False)
    card_limit = Column(Float, nullable=False)
    tos = Column(String(10))
    pos = Column(String(10))
    tad = Column(Float, default=0.0)
    norm = Column(Float, default=0.0)
    rb = Column(Float, default=0.0)
    stab = Column(String(50))
    emi = Column(Float, default=0.0)
    principle = Column(Float, default=0.0)
    mobile = Column(String(15))
    per_percent = Column(Float, default=0.0)
    block = Column(String(10), default='NO')
    cycle = Column(String(20))
    emp_name = Column(String(100))
    paid_unpaid = Column(String(10), default='UNPAID')
    status = Column(String(50))
    contact_status = Column(String(100))
    mis = Column(String(50))
    remarks = Column(Text)
    ptp_date = Column(String(20))
    ptp_amount = Column(Float, default=0.0)
    paid_date = Column(String(20))
    paid_amount = Column(Float, default=0.0)
    new_numbers = Column(String(100))
    new_address = Column(Text)
    mode_of_payment = Column(String(50))
    receipt = Column(String(100))
    projection = Column(String(100))
    manager = Column(String(100))
    areas = Column(String(100))
    add1 = Column(String(200))
    add2 = Column(String(200))
    work_address = Column(Text)
    pincode = Column(String(10))
    permanent_address = Column(Text)
    history = Column(Text)
    pnpa = Column(String(50))
    principal = Column(Float, default=0.0)
    on_field = Column(String(50))  # 'on' is a reserved keyword, so using 'on_field'
    
    # Audit fields
    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CreditBill {self.s_no}: {self.cum_name}>'
    
    def to_dict(self):
        """Convert model instance to dictionary for JSON serialization with raw database column names"""
        return {
            'id': self.id,
            's_no': self.s_no,
            'card_no': self.card_no,
            'cum_name': self.cum_name,
            'card_limit': self.card_limit,
            'tos': self.tos,
            'pos': self.pos,
            'tad': self.tad,
            'norm': self.norm,
            'rb': self.rb,
            'stab': self.stab,
            'emi': self.emi,
            'principle': self.principle,
            'mobile': self.mobile,
            'per_percent': self.per_percent,
            'block': self.block,
            'cycle': self.cycle,
            'emp_name': self.emp_name,
            'paid_unpaid': self.paid_unpaid,
            'status': self.status,
            'contact_status': self.contact_status,
            'mis': self.mis,
            'remarks': self.remarks,
            'ptp_date': self.ptp_date,
            'ptp_amount': self.ptp_amount,
            'paid_date': self.paid_date,
            'paid_amount': self.paid_amount,
            'new_numbers': self.new_numbers,
            'new_address': self.new_address,
            'mode_of_payment': self.mode_of_payment,
            'receipt': self.receipt,
            'projection': self.projection,
            'manager': self.manager,
            'areas': self.areas,
            'add1': self.add1,
            'add2': self.add2,
            'work_address': self.work_address,
            'pincode': self.pincode,
            'permanent_address': self.permanent_address,
            'history': self.history,
            'pnpa': self.pnpa,
            'principal': self.principal,
            'on_field': self.on_field,  # Using actual field name since 'on' is reserved
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }