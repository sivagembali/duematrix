#!/usr/bin/env python3
"""
Sample Data Seeder for Credit Bills
Creates sample credit bill data for testing the header configuration API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.credit_bill import CreditBill
from datetime import datetime, timedelta
import random

def create_sample_bills():
    """Create sample credit bill data"""
    
    # Sample data
    banks = ['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Bank', 'IndusInd Bank']
    statuses = ['pending', 'paid', 'partially_paid', 'overdue']
    emp_names = ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson', 'David Brown']
    
    sample_bills = []
    
    for i in range(1, 51):  # Create 50 sample bills
        bill = CreditBill(
            s_no=i,
            card_no=f"1234****567{i:02d}",
            cum_name=random.choice(banks),
            card_limit=round(random.uniform(50000, 500000), 2),
            tos=random.choice(['A', 'B', 'C']),
            pos=random.choice(['X', 'Y', 'Z']),
            tad=round(random.uniform(1000, 50000), 2),
            norm=round(random.uniform(5000, 25000), 2),
            rb=round(random.uniform(100, 5000), 2),
            stab=f"STAB{i:03d}",
            emi=round(random.uniform(2000, 15000), 2),
            principle=round(random.uniform(10000, 100000), 2),
            mobile=f"9{random.randint(100000000, 999999999)}",
            per_percent=round(random.uniform(1.5, 4.0), 2),
            block=random.choice(['YES', 'NO']),
            cycle=f"Cycle{random.randint(1, 12)}",
            emp_name=random.choice(emp_names),
            paid_unpaid=random.choice(['PAID', 'UNPAID']),
            status=random.choice(statuses),
            contact_status=random.choice(['Contacted', 'Not Contacted', 'Follow Up']),
            mis=f"MIS{i:03d}",
            remarks=f"Sample remark for bill {i}",
            ptp_amount=round(random.uniform(1000, 10000), 2),
            paid_amount=round(random.uniform(0, 15000), 2),
            principal=round(random.uniform(10000, 100000), 2),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            updated_at=datetime.utcnow()
        )
        sample_bills.append(bill)
    
    return sample_bills

def main():
    """Seed the database with sample data"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Seeding database with sample credit bills...")
        
        # Check if bills already exist
        existing_count = CreditBill.query.count()
        if existing_count > 0:
            print(f"   Found {existing_count} existing bills")
            response = input("   Do you want to add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("   Skipping data seeding")
                return
        
        # Create sample bills
        sample_bills = create_sample_bills()
        
        try:
            # Add to database
            for bill in sample_bills:
                db.session.add(bill)
            
            db.session.commit()
            print(f"✅ Successfully created {len(sample_bills)} sample credit bills")
            
            # Verify data
            total_bills = CreditBill.query.count()
            print(f"📊 Total bills in database: {total_bills}")
            
            # Show sample data
            print("\n📋 Sample of created bills:")
            sample_display = CreditBill.query.limit(5).all()
            for bill in sample_display:
                print(f"   Bill {bill.s_no}: {bill.cum_name} - {bill.status} - ₹{bill.principal:,.2f}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating sample data: {str(e)}")

if __name__ == "__main__":
    main()