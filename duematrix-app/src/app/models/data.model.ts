export interface ColumnHeader {
  id?: number;
  col_header: string;
  col_label: string;
  is_editable: boolean;
  is_multi_select?: boolean;
  col_width?: number;
  display: boolean;
  default_display: boolean; // Show column by default in the table
  is_frozen: boolean; // Keep column frozen (fixed) on the left
  display_order: number;
  role_id?: number | null;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  updated_by?: string;
}

export interface DataRow {
  id: number;
  [key: string]: any;
}

export interface CustomerData {
  // Primary Key
  id: number;
  
  // Foreign Keys
  user_id?: number | null;
  
  // Personal Information
  customer_name: string;
  email: string;
  phone_number: string;
  date_of_birth?: string;
  blood_group?: string;
  nationality?: string;
  marital_status?: string;
  spouse_name?: string;
  children_count?: number;
  emergency_contact?: string;
  
  // Address Information
  current_address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  
  // Financial Information
  credit_card_no?: string;
  account_balance?: number;
  account_type?: string;
  bank?: string;
  bank_name?: string;
  bank_account_no?: string;
  ifsc_code?: string;
  branch_name?: string;
  pan_number?: string;
  aadhar_number?: string;
  annual_income?: number;
  tax_regime?: string;
  insurance_policy_no?: string;
  
  // Employment Information
  employee_id?: string;
  department?: string;
  status?: string;
  salary?: number;
  hire_date?: string;
  manager_name?: string;
  work_location?: string;
  remote_work_eligible?: string;
  
  // Project Information
  project_name?: string;
  project_code?: string;
  cycle_name?: string;
  
  // Skills and Education
  skill_set?: string;
  experience_years?: number;
  education?: string;
  certification?: string;
  
  // Performance
  performance_rating?: number;
  last_appraisal_date?: string;
  next_appraisal_date?: string;
  
  // Vehicle Information
  vehicle_type?: string;
  vehicle_number?: string;
  
  // System Fields
  registration_date?: string;
  last_login?: string;
  notes?: string;
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  updated_by?: string;
}

export interface CustomerDataResponse {
  success: boolean;
  message: string;
  data: CustomerData[];
  pagination?: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

export interface SingleCustomerDataResponse {
  success: boolean;
  message: string;
  data: CustomerData;
}

export interface FilterOptions {
  departments: string[];
  statuses: string[];
  cities: string[];
  states: string[];
  banks: string[];
  cycles: string[];
}

export interface FilterOptionsResponse {
  success: boolean;
  message: string;
  data: FilterOptions;
}

