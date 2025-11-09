import { ColumnHeader, DataRow } from '../models/data.model';
import { Injectable, inject } from '@angular/core';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class MockDataGenerator {
  private authService = inject(AuthService);
  
  private static readonly FIRST_NAMES = ['Raj', 'Priya', 'Amit', 'Sita', 'Vijay', 'Anita', 'Ravi', 'Lakshmi', 'Kumar', 'Deepa'];
  private static readonly LAST_NAMES = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Krishnan', 'Gupta', 'Nair', 'Desai', 'Rao'];
  private static readonly CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad'];
  private static readonly STATES = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'West Bengal', 'Telangana'];
  private static readonly DEPARTMENTS = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'IT', 'Support'];
  private static readonly STATUSES = ['Active', 'Inactive', 'Pending', 'Completed', 'In Progress'];

  /**
   * Get header mapping from API (via AuthService)
   * Falls back to static headers if API data is not available
   */
  generateHeaderMapping(): ColumnHeader[] {
    // Try to get headers from auth service (loaded from API)
    const apiHeaders = this.authService.getHeadersValue();
    
    if (apiHeaders && apiHeaders.length > 0) {
      console.log('Using headers from API:', apiHeaders.length);
      return apiHeaders;
    }
    
    // Fallback to static headers if API headers not available
    console.warn('API headers not available, using fallback static headers');
    const headers: ColumnHeader[] = [
      { col_header: 'id', col_label: 'ID', is_editable: false, is_multi_select: false, col_width: 5, display: true, default_display: true, is_frozen: true, display_order: 1 },
      { col_header: 'customer_name', col_label: 'Customer Name', is_editable: false, is_multi_select: true, col_width: 15, display: true, default_display: true, is_frozen: true, display_order: 2 },
      { col_header: 'credit_card_no', col_label: 'Credit Card No', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: true, is_frozen: true, display_order: 3 },
      { col_header: 'current_address', col_label: 'Current Address', is_editable: true, is_multi_select: false, col_width: 20, display: true, default_display: false, is_frozen: false, display_order: 4 },
      { col_header: 'email', col_label: 'Email', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: true, is_frozen: false, display_order: 5 },
      { col_header: 'phone_number', col_label: 'Phone Number', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: true, is_frozen: false, display_order: 6 },
      { col_header: 'date_of_birth', col_label: 'Date of Birth', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 7 },
      { col_header: 'city', col_label: 'City', is_editable: true, is_multi_select: true, col_width: 10, display: true, default_display: true, is_frozen: false, display_order: 8 },
      { col_header: 'state', col_label: 'State', is_editable: true, is_multi_select: true, col_width: 10, display: true, default_display: true, is_frozen: false, display_order: 9 },
      { col_header: 'postal_code', col_label: 'Postal Code', is_editable: true, is_multi_select: false, col_width: 8, display: true, default_display: false, is_frozen: false, display_order: 10 },
      { col_header: 'country', col_label: 'Country', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: true, is_frozen: false, display_order: 11 },
      { col_header: 'account_balance', col_label: 'Account Balance', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: true, is_frozen: false, display_order: 12 },
      { col_header: 'account_type', col_label: 'Account Type', is_editable: true, is_multi_select: true, col_width: 12, display: true, default_display: true, is_frozen: false, display_order: 13 },
      { col_header: 'registration_date', col_label: 'Registration Date', is_editable: false, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 14 },
      { col_header: 'last_login', col_label: 'Last Login', is_editable: false, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 15 },
      { col_header: 'status', col_label: 'Status', is_editable: true, is_multi_select: true, col_width: 10, display: true, default_display: true, is_frozen: false, display_order: 16 },
      { col_header: 'department', col_label: 'Department', is_editable: true, is_multi_select: true, col_width: 12, display: true, default_display: true, is_frozen: false, display_order: 17 },
      { col_header: 'employee_id', col_label: 'Employee ID', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 18 },
      { col_header: 'salary', col_label: 'Salary', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: true, is_frozen: false, display_order: 19 },
      { col_header: 'hire_date', col_label: 'Hire Date', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 20 },
      { col_header: 'manager_name', col_label: 'Manager Name', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 21 },
      { col_header: 'project_name', col_label: 'Project Name', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 22 },
      { col_header: 'project_code', col_label: 'Project Code', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 23 },
      { col_header: 'skill_set', col_label: 'Skill Set', is_editable: true, is_multi_select: true, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 24 },
      { col_header: 'experience_years', col_label: 'Experience (Years)', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 25 },
      { col_header: 'education', col_label: 'Education', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 26 },
      { col_header: 'certification', col_label: 'Certification', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 27 },
      { col_header: 'emergency_contact', col_label: 'Emergency Contact', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 28 },
      { col_header: 'blood_group', col_label: 'Blood Group', is_editable: true, is_multi_select: true, col_width: 8, display: true, default_display: false, is_frozen: false, display_order: 29 },
      { col_header: 'nationality', col_label: 'Nationality', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 30 },
      { col_header: 'marital_status', col_label: 'Marital Status', is_editable: true, is_multi_select: true, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 31 },
      { col_header: 'spouse_name', col_label: 'Spouse Name', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 32 },
      { col_header: 'children_count', col_label: 'Children Count', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 33 },
      { col_header: 'vehicle_type', col_label: 'Vehicle Type', is_editable: true, is_multi_select: true, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 34 },
      { col_header: 'vehicle_number', col_label: 'Vehicle Number', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 35 },
      { col_header: 'insurance_policy_no', col_label: 'Insurance Policy No', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 36 },
      { col_header: 'pan_number', col_label: 'PAN Number', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 37 },
      { col_header: 'aadhar_number', col_label: 'Aadhar Number', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 38 },
      { col_header: 'bank', col_label: 'Bank', is_editable: true, is_multi_select: true, col_width: 15, display: true, default_display: true, is_frozen: false, display_order: 39 },
      { col_header: 'bank_name', col_label: 'Bank Name', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 40 },
      { col_header: 'bank_account_no', col_label: 'Bank Account No', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 41 },
      { col_header: 'ifsc_code', col_label: 'IFSC Code', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 42 },
      { col_header: 'branch_name', col_label: 'Branch Name', is_editable: true, is_multi_select: false, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 43 },
      { col_header: 'annual_income', col_label: 'Annual Income', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 44 },
      { col_header: 'tax_regime', col_label: 'Tax Regime', is_editable: true, is_multi_select: true, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 45 },
      { col_header: 'performance_rating', col_label: 'Performance Rating', is_editable: true, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 46 },
      { col_header: 'last_appraisal_date', col_label: 'Last Appraisal Date', is_editable: false, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 47 },
      { col_header: 'next_appraisal_date', col_label: 'Next Appraisal Date', is_editable: false, is_multi_select: false, col_width: 12, display: true, default_display: false, is_frozen: false, display_order: 48 },
      { col_header: 'work_location', col_label: 'Work Location', is_editable: true, is_multi_select: true, col_width: 15, display: true, default_display: false, is_frozen: false, display_order: 49 },
      { col_header: 'remote_work_eligible', col_label: 'Remote Work Eligible', is_editable: true, is_multi_select: false, col_width: 10, display: true, default_display: false, is_frozen: false, display_order: 50 },
      { col_header: 'cycle_name', col_label: 'Cycle Name', is_editable: true, is_multi_select: true, col_width: 12, display: true, default_display: true, is_frozen: false, display_order: 51 },
      { col_header: 'user_id', col_label: 'User ID', is_editable: false, is_multi_select: false, col_width: 8, display: true, default_display: false, is_frozen: false, display_order: 52 },
      { col_header: 'notes', col_label: 'Notes', is_editable: true, is_multi_select: false, col_width: 20, display: true, default_display: false, is_frozen: false, display_order: 53 }
    ];

    return headers;
  }

  generateDataset(count: number = 100): DataRow[] {
    const data: DataRow[] = [];

    for (let i = 1; i <= count; i++) {
      data.push({
        id: i,
        user_id: Math.random() > 0.5 ? Math.floor(Math.random() * 10) + 1 : null,
        customer_name: `${this.getRandomItem(MockDataGenerator.FIRST_NAMES)} ${this.getRandomItem(MockDataGenerator.LAST_NAMES)}`,
        credit_card_no: this.generateCreditCard(),
        current_address: this.generateAddress(),
        email: `user${i}@example.com`,
        phone_number: this.generatePhone(),
        date_of_birth: this.generateDate(1950, 2005),
        city: this.getRandomItem(MockDataGenerator.CITIES),
        state: this.getRandomItem(MockDataGenerator.STATES),
        postal_code: this.generatePostalCode(),
        country: 'India',
        account_balance: this.generateAmount(1000, 100000),
        account_type: this.getRandomItem(['Savings', 'Current', 'Fixed Deposit', 'Recurring Deposit']),
        registration_date: this.generateDate(2020, 2024),
        last_login: this.generateDateTime(),
        status: this.getRandomItem(MockDataGenerator.STATUSES),
        department: this.getRandomItem(MockDataGenerator.DEPARTMENTS),
        employee_id: `EMP${String(i).padStart(5, '0')}`,
        salary: this.generateAmount(30000, 200000),
        hire_date: this.generateDate(2015, 2024),
        manager_name: `${this.getRandomItem(MockDataGenerator.FIRST_NAMES)} ${this.getRandomItem(MockDataGenerator.LAST_NAMES)}`,
        project_name: `Project ${this.getRandomItem(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'])}`,
        project_code: `PRJ${String(Math.floor(Math.random() * 1000)).padStart(4, '0')}`,
        cycle_name: this.getRandomItem(['Q1-2024', 'Q2-2024', 'Q3-2024', 'Q4-2024', 'Q1-2025', 'H1-2024', 'H2-2024', 'FY2024', 'FY2025']),
        skill_set: this.getRandomItem(['Java, Python', 'React, Angular', 'DevOps, AWS', 'Data Science, ML']),
        experience_years: Math.floor(Math.random() * 20) + 1,
        education: this.getRandomItem(['B.Tech', 'M.Tech', 'MBA', 'MCA', 'B.Sc', 'M.Sc']),
        certification: this.getRandomItem(['AWS Certified', 'Azure Certified', 'PMP', 'Scrum Master', 'None']),
        emergency_contact: this.generatePhone(),
        blood_group: this.getRandomItem(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
        nationality: 'Indian',
        marital_status: this.getRandomItem(['Single', 'Married', 'Divorced']),
        spouse_name: Math.random() > 0.5 ? `${this.getRandomItem(MockDataGenerator.FIRST_NAMES)} ${this.getRandomItem(MockDataGenerator.LAST_NAMES)}` : 'N/A',
        children_count: Math.floor(Math.random() * 4),
        vehicle_type: this.getRandomItem(['Two Wheeler', 'Four Wheeler', 'None']),
        vehicle_number: `MH${String(Math.floor(Math.random() * 100)).padStart(2, '0')}XX${Math.floor(Math.random() * 10000)}`,
        insurance_policy_no: `INS${String(Math.floor(Math.random() * 1000000)).padStart(8, '0')}`,
        pan_number: this.generatePAN(),
        aadhar_number: this.generateAadhar(),
        bank: this.getRandomItem(['HDFC Bank', 'ICICI Bank', 'State Bank of India', 'Axis Bank', 'Kotak Mahindra Bank', 'Punjab National Bank']),
        bank_name: this.getRandomItem(['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Mahindra']),
        bank_account_no: this.generateAccountNumber(),
        ifsc_code: `${this.getRandomItem(['HDFC', 'ICIC', 'SBIN', 'UTIB', 'KKBK'])}0${String(Math.floor(Math.random() * 100000)).padStart(6, '0')}`,
        branch_name: `${this.getRandomItem(MockDataGenerator.CITIES)} Branch`,
        annual_income: this.generateAmount(360000, 2400000),
        tax_regime: this.getRandomItem(['Old Regime', 'New Regime']),
        performance_rating: (Math.random() * 5).toFixed(1),
        last_appraisal_date: this.generateDate(2023, 2024),
        next_appraisal_date: this.generateDate(2025, 2026),
        work_location: this.getRandomItem(MockDataGenerator.CITIES),
        remote_work_eligible: this.getRandomItem(['Yes', 'No']),
        notes: `Sample notes for record ${i}. ${this.generateRandomText()}`
      });
    }

    return data;
  }

  private getRandomItem<T>(array: T[]): T {
    return array[Math.floor(Math.random() * array.length)];
  }

  private generateCreditCard(): string {
    let card = '';
    for (let i = 0; i < 16; i++) {
      card += Math.floor(Math.random() * 10);
    }
    return card;
  }

  private generateAddress(): string {
    const street = Math.floor(Math.random() * 999) + 1;
    const building = this.getRandomItem(['A', 'B', 'C', 'D']);
    const area = this.getRandomItem(['Sector', 'Phase', 'Block']);
    const num = Math.floor(Math.random() * 50) + 1;
    return `${street}/${building}/${area}-${num}/${this.getRandomItem(MockDataGenerator.CITIES)}`;
  }

  private generatePhone(): string {
    return `+91${Math.floor(Math.random() * 9000000000) + 1000000000}`;
  }

  private generateDate(startYear: number, endYear: number): string {
    const year = Math.floor(Math.random() * (endYear - startYear + 1)) + startYear;
    const month = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0');
    const day = String(Math.floor(Math.random() * 28) + 1).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  private generateDateTime(): string {
    const date = this.generateDate(2024, 2025);
    const hour = String(Math.floor(Math.random() * 24)).padStart(2, '0');
    const minute = String(Math.floor(Math.random() * 60)).padStart(2, '0');
    return `${date} ${hour}:${minute}`;
  }

  private generatePostalCode(): string {
    return String(Math.floor(Math.random() * 900000) + 100000);
  }

  private generateAmount(min: number, max: number): string {
    return Math.floor(Math.random() * (max - min + 1) + min).toFixed(2);
  }

  private generatePAN(): string {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let pan = '';
    for (let i = 0; i < 5; i++) {
      pan += letters.charAt(Math.floor(Math.random() * letters.length));
    }
    pan += Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    pan += letters.charAt(Math.floor(Math.random() * letters.length));
    return pan;
  }

  private generateAadhar(): string {
    return String(Math.floor(Math.random() * 900000000000) + 100000000000);
  }

  private generateAccountNumber(): string {
    return String(Math.floor(Math.random() * 9000000000000000) + 1000000000000000);
  }

  private generateRandomText(): string {
    const texts = [
      'Important customer record.',
      'High priority account.',
      'Verified and active.',
      'Requires follow-up.',
      'Premium member.',
      'Recently updated information.',
      'Contact for special offers.'
    ];
    return this.getRandomItem(texts);
  }
}
