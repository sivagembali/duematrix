"""
Seed Customer Data
Populates the customer_data table with comprehensive sample records
"""

from app import create_app
from models import db, CustomerData
import random
from datetime import datetime

FIRST_NAMES = ['Raj', 'Priya', 'Amit', 'Sita', 'Vijay', 'Anita', 'Ravi', 'Lakshmi', 'Kumar', 'Deepa', 
               'Arjun', 'Meera', 'Rahul', 'Pooja', 'Suresh', 'Kavita', 'Manoj', 'Swati', 'Anil', 'Neha']
LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Krishnan', 'Gupta', 'Nair', 'Desai', 'Rao',
              'Verma', 'Joshi', 'Mehta', 'Shah', 'Bhat', 'Iyer', 'Pillai', 'Menon', 'Agarwal', 'Chopra']
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
STATES = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'West Bengal', 'Telangana', 'Delhi', 'Rajasthan']
DEPARTMENTS = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'IT', 'Support']
STATUSES = ['Active', 'Inactive', 'Pending', 'Completed', 'In Progress']
BANKS = ['HDFC Bank', 'ICICI Bank', 'State Bank of India', 'Axis Bank', 'Kotak Mahindra Bank', 'Punjab National Bank']
CYCLES = ['Q1-2024', 'Q2-2024', 'Q3-2024', 'Q4-2024', 'Q1-2025', 'H1-2024', 'H2-2024', 'FY2024', 'FY2025']


def random_item(items):
    return random.choice(items)


def generate_credit_card():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])


def generate_address():
    street = random.randint(1, 999)
    building = random.choice(['A', 'B', 'C', 'D'])
    area = random.choice(['Sector', 'Phase', 'Block'])
    num = random.randint(1, 50)
    city = random_item(CITIES)
    return f'{street}/{building}/{area}-{num}/{city}'


def generate_phone():
    return f'+91{random.randint(1000000000, 9999999999)}'


def generate_date(start_year, end_year):
    year = random.randint(start_year, end_year)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f'{year}-{month}-{day}'


def generate_datetime():
    date = generate_date(2024, 2025)
    hour = str(random.randint(0, 23)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    return f'{date} {hour}:{minute}'


def generate_postal_code():
    return str(random.randint(100000, 999999))


def generate_amount(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)


def generate_pan():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pan = ''.join([random.choice(letters) for _ in range(5)])
    pan += str(random.randint(0, 9999)).zfill(4)
    pan += random.choice(letters)
    return pan


def generate_aadhar():
    return str(random.randint(100000000000, 999999999999))


def generate_account_number():
    return str(random.randint(1000000000000000, 9999999999999999))


def generate_random_text():
    texts = [
        'Important customer record.',
        'High priority account.',
        'Verified and active.',
        'Requires follow-up.',
        'Premium member.',
        'Recently updated information.',
        'Contact for special offers.'
    ]
    return random_item(texts)


def seed_customer_data(count=100):
    """Seed customer data records"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing customer data...")
        CustomerData.query.delete()
        db.session.commit()
        
        print(f"Creating {count} customer data records...")
        
        for i in range(1, count + 1):
            record = CustomerData(
                user_id=None,  # Can be linked to specific users later
                customer_name=f'{random_item(FIRST_NAMES)} {random_item(LAST_NAMES)}',
                email=f'customer{i}@example.com',
                phone_number=generate_phone(),
                date_of_birth=generate_date(1950, 2005),
                blood_group=random_item(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
                nationality='Indian',
                marital_status=random_item(['Single', 'Married', 'Divorced']),
                spouse_name=f'{random_item(FIRST_NAMES)} {random_item(LAST_NAMES)}' if random.random() > 0.5 else 'N/A',
                children_count=random.randint(0, 4),
                emergency_contact=generate_phone(),
                current_address=generate_address(),
                city=random_item(CITIES),
                state=random_item(STATES),
                postal_code=generate_postal_code(),
                country='India',
                credit_card_no=generate_credit_card(),
                account_balance=generate_amount(1000, 100000),
                account_type=random_item(['Savings', 'Current', 'Fixed Deposit', 'Recurring Deposit']),
                bank=random_item(BANKS),
                bank_name=random_item(BANKS),
                bank_account_no=generate_account_number(),
                ifsc_code=f'{random_item(["HDFC", "ICIC", "SBIN", "UTIB", "KKBK"])}0{str(random.randint(0, 100000)).zfill(6)}',
                branch_name=f'{random_item(CITIES)} Branch',
                pan_number=generate_pan(),
                aadhar_number=generate_aadhar(),
                annual_income=generate_amount(360000, 2400000),
                tax_regime=random_item(['Old Regime', 'New Regime']),
                insurance_policy_no=f'INS{str(random.randint(0, 1000000)).zfill(8)}',
                employee_id=f'EMP{str(i).zfill(5)}',
                department=random_item(DEPARTMENTS),
                status=random_item(STATUSES),
                salary=generate_amount(30000, 200000),
                hire_date=generate_date(2015, 2024),
                manager_name=f'{random_item(FIRST_NAMES)} {random_item(LAST_NAMES)}',
                work_location=random_item(CITIES),
                remote_work_eligible=random_item(['Yes', 'No']),
                project_name=f'Project {random_item(["Alpha", "Beta", "Gamma", "Delta", "Epsilon"])}',
                project_code=f'PRJ{str(random.randint(0, 1000)).zfill(4)}',
                cycle_name=random_item(CYCLES),
                skill_set=random_item(['Java, Python', 'React, Angular', 'DevOps, AWS', 'Data Science, ML']),
                experience_years=random.randint(1, 20),
                education=random_item(['B.Tech', 'M.Tech', 'MBA', 'MCA', 'B.Sc', 'M.Sc']),
                certification=random_item(['AWS Certified', 'Azure Certified', 'PMP', 'Scrum Master', 'None']),
                performance_rating=round(random.uniform(1, 5), 1),
                last_appraisal_date=generate_date(2023, 2024),
                next_appraisal_date=generate_date(2025, 2026),
                vehicle_type=random_item(['Two Wheeler', 'Four Wheeler', 'None']),
                vehicle_number=f'MH{str(random.randint(0, 100)).zfill(2)}XX{random.randint(0, 10000)}',
                registration_date=generate_date(2020, 2024),
                last_login=generate_datetime(),
                notes=f'Sample notes for record {i}. {generate_random_text()}',
                created_by='system',
                updated_by='system'
            )
            
            db.session.add(record)
            
            if i % 10 == 0:
                print(f'Created {i} records...')
        
        db.session.commit()
        print(f'✅ Successfully created {count} customer data records!')
        
        # Display sample records
        sample = CustomerData.query.limit(3).all()
        print('\nSample records:')
        for record in sample:
            print(f'  - ID: {record.id}, Name: {record.customer_name}, Email: {record.email}, Bank: {record.bank}, Cycle: {record.cycle_name}')


if __name__ == '__main__':
    seed_customer_data(100)
