#!/usr/bin/env python3
"""
Quick check for header configurations and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.credit_bill import CreditBill
from app.models.header_config import HeaderConfig

def main():
    """Check database state"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking database state...")
        
        # Check header configurations
        header_count = HeaderConfig.query.count()
        print(f"📋 Header configurations: {header_count}")
        
        if header_count == 0:
            print("⚠️  No header configurations found!")
            print("   Run: python init_header_config.py")
        else:
            visible_configs = HeaderConfig.query.filter(HeaderConfig.status == True).count()
            print(f"👁️  Visible columns: {visible_configs}")
            
            # Show first few configs
            configs = HeaderConfig.query.limit(5).all()
            print("\n📋 Sample configurations:")
            for config in configs:
                status = "✅" if config.status else "❌"
                print(f"   {status} {config.col_name} -> {config.label}")
        
        # Check credit bills
        bill_count = CreditBill.query.count()
        print(f"\n💳 Credit bills: {bill_count}")
        
        if bill_count == 0:
            print("⚠️  No bills found!")
            print("   Run: python seed_sample_data.py")
        else:
            # Show first few bills
            bills = CreditBill.query.limit(3).all()
            print("\n💳 Sample bills:")
            for bill in bills:
                print(f"   Bill {bill.s_no}: {bill.cum_name} - {bill.status}")
        
        print(f"\n🌐 API endpoints available:")
        print(f"   GET /api/bills/with-config")
        print(f"   GET /api/header-config") 
        print(f"   GET /api/bills/stats")

if __name__ == "__main__":
    main()