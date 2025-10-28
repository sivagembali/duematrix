import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface CreditBill {
  id: number;
  s_no: number;
  card_no: string;
  cum_name: string;
  card_limit: number;
  tos?: string;
  pos?: string;
  tad?: number;
  norm?: number;
  rb?: number;
  stab?: string;
  emi?: number;
  principle?: number;
  mobile?: string;
  per_percent?: number;
  block?: string;
  cycle?: string;
  emp_name?: string;
  paid_unpaid?: string;
  status?: string;
  contact_status?: string;
  mis?: string;
  remarks?: string;
  ptp_date?: string;
  ptp_amount?: number;
  paid_date?: string;
  paid_amount?: number;
  new_numbers?: string;
  new_address?: string;
  mode_of_payment?: string;
  receipt?: string;
  projection?: string;
  manager?: string;
  areas?: string;
  add1?: string;
  add2?: string;
  work_address?: string;
  pincode?: string;
  permanent_address?: string;
  history?: string;
  pnpa?: string;
  principal?: number;
  on_field?: string;
  created_at?: string;
  updated_at?: string;
}

interface HeaderConfig {
  id: number;
  colName: string;
  label: string;
  status: boolean;
  dataType: string;
  width: number;
  sortable: boolean;
  searchable: boolean;
  filterType: string;
  displayOrder: number;
  multiSelectFilter: any[];
}

interface ApiResponse {
  success: boolean;
  data: {
    bills: CreditBill[];
    headerConfig: HeaderConfig[];
    visibleColumns: string[];
    pagination: {
      page: number;
      perPage: number;
      total: number;
      totalPages: number;
      hasNext: boolean;
      hasPrev: boolean;
    };
  };
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div style="padding: 20px; font-family: Arial, sans-serif;">
      <h1 style="color: #333; text-align: center; margin-bottom: 30px;">Credit Bills Management System</h1>
      
      <!-- Search and Controls -->
      <div style="margin-bottom: 20px; display: flex; align-items: center; gap: 15px;">
        <div>
          <input 
            type="text" 
            [(ngModel)]="searchTerm" 
            (keyup.enter)="onSearch()"
            placeholder="Search bills..." 
            style="padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; width: 300px;">
        </div>
        <button (click)="onSearch()" style="padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
          Search
        </button>
        <button (click)="onReset()" style="padding: 8px 16px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
          Reset
        </button>
      </div>
      
      <div *ngIf="loading" style="text-align: center; color: #666;">
        Loading bills...
      </div>
      
      <div *ngIf="!loading">
        <div style="margin-bottom: 15px; color: #555;">
          <strong>Total Records:</strong> {{ totalRecords }} | 
          <strong>Page:</strong> {{ currentPage }} | 
          <strong>Visible Columns:</strong> {{ visibleColumns.length }}
        </div>
        
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; min-width: 800px;">
            <thead>
              <tr style="background-color: #f5f5f5;">
                <th *ngFor="let config of getVisibleHeaders()" 
                    [style.width.px]="config.width"
                    style="padding: 12px; border: 1px solid #ddd; text-align: left; font-weight: bold;">
                  {{ config.label }}
                  <span *ngIf="config.sortable" style="cursor: pointer; color: #007bff;"> ↕</span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let bill of bills; trackBy: trackByBillId">
                <td *ngFor="let config of getVisibleHeaders()" 
                    style="padding: 12px; border: 1px solid #ddd; vertical-align: top;">
                  <span [innerHTML]="getCellValue(bill, config)"></span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div *ngIf="totalRecords > pageSize" style="text-align: center; margin-top: 20px;">
          <button (click)="goToPage(currentPage - 1)" 
                  [disabled]="currentPage <= 1"
                  style="padding: 8px 12px; margin: 0 5px; border: 1px solid #ddd; background: white; cursor: pointer;">
            Previous
          </button>
          <span style="margin: 0 15px; color: #666;">
            Page {{ currentPage }} of {{ Math.ceil(totalRecords / pageSize) }}
          </span>
          <button (click)="goToPage(currentPage + 1)" 
                  [disabled]="currentPage >= Math.ceil(totalRecords / pageSize)"
                  style="padding: 8px 12px; margin: 0 5px; border: 1px solid #ddd; background: white; cursor: pointer;">
            Next
          </button>
        </div>
        
        <p style="color: #666; font-style: italic; margin-top: 20px;">
          * Data is {{ bills.length > 0 && bills[0].s_no ? 'loaded from backend API' : 'showing sample data (API not available)' }}
        </p>
      </div>
    </div>
  `,
  styles: []
})
export class AppComponent {
  title = 'Credit Bills Management System';
  bills: CreditBill[] = [];
  headerConfig: HeaderConfig[] = [];
  visibleColumns: string[] = [];
  loading = true;
  currentPage = 1;
  pageSize = 25;
  totalRecords = 0;
  searchTerm = '';
  
  constructor(private http: HttpClient) {
    console.log('🚀 AppComponent constructor called!');
    this.loadBillsWithConfig();
  }
  
  loadBillsWithConfig() {
    console.log('🔄 Loading bills with configuration...');
    
    const params = new URLSearchParams({
      page: this.currentPage.toString(),
      per_page: this.pageSize.toString()
    });
    
    if (this.searchTerm) {
      params.append('search', this.searchTerm);
    }
    
    // Try to fetch from backend, fallback to sample data
    this.http.get<ApiResponse>(`http://localhost:5000/api/header-config/bills-with-config?${params}`)
      .subscribe({
        next: (response) => {
          console.log('✅ Data loaded from API:', response);
          if (response.success) {
            this.bills = response.data.bills;
            this.headerConfig = response.data.headerConfig;
            this.visibleColumns = response.data.visibleColumns;
            this.totalRecords = response.data.pagination.total;
          }
          this.loading = false;
        },
        error: (error) => {
          console.warn('⚠️ API not available, using sample data:', error);
          this.loadSampleData();
          this.loading = false;
        }
      });
  }
  
  loadSampleData() {
    this.bills = this.getSampleData();
    this.headerConfig = this.getSampleHeaders();
    this.visibleColumns = ['s_no', 'card_no', 'cum_name', 'card_limit', 'mobile', 'status'];
    this.totalRecords = this.bills.length;
  }
  
  getSampleData(): CreditBill[] {
    return [
      {
        id: 1,
        s_no: 1,
        card_no: '1234****5678',
        cum_name: 'HDFC Bank Customer',
        card_limit: 50000,
        mobile: '9876543210',
        status: 'PENDING',
        paid_unpaid: 'UNPAID'
      },
      {
        id: 2,
        s_no: 2,
        card_no: '2345****6789',
        cum_name: 'ICICI Bank Customer',
        card_limit: 75000,
        mobile: '8765432109',
        status: 'OVERDUE',
        paid_unpaid: 'UNPAID'
      },
      {
        id: 3,
        s_no: 3,
        card_no: '3456****7890',
        cum_name: 'SBI Bank Customer',
        card_limit: 30000,
        mobile: '7654321098',
        status: 'PAID',
        paid_unpaid: 'PAID'
      },
      {
        id: 4,
        s_no: 4,
        card_no: '4567****8901',
        cum_name: 'AXIS Bank Customer',
        card_limit: 60000,
        mobile: '6543210987',
        status: 'PENDING',
        paid_unpaid: 'UNPAID'
      },
      {
        id: 5,
        s_no: 5,
        card_no: '5678****9012',
        cum_name: 'Kotak Bank Customer',
        card_limit: 80000,
        mobile: '5432109876',
        status: 'OVERDUE',
        paid_unpaid: 'UNPAID'
      }
    ];
  }
  
  getSampleHeaders(): HeaderConfig[] {
    return [
      { id: 1, colName: 's_no', label: 'S.No', status: true, dataType: 'number', width: 80, sortable: true, searchable: false, filterType: 'text', displayOrder: 1, multiSelectFilter: [] },
      { id: 2, colName: 'card_no', label: 'Card No', status: true, dataType: 'text', width: 140, sortable: true, searchable: true, filterType: 'text', displayOrder: 2, multiSelectFilter: [] },
      { id: 3, colName: 'cum_name', label: 'Customer Name', status: true, dataType: 'text', width: 200, sortable: true, searchable: true, filterType: 'text', displayOrder: 3, multiSelectFilter: [] },
      { id: 4, colName: 'card_limit', label: 'Card Limit', status: true, dataType: 'number', width: 120, sortable: true, searchable: false, filterType: 'number', displayOrder: 4, multiSelectFilter: [] },
      { id: 5, colName: 'mobile', label: 'Mobile', status: true, dataType: 'text', width: 120, sortable: false, searchable: true, filterType: 'text', displayOrder: 5, multiSelectFilter: [] },
      { id: 6, colName: 'status', label: 'Status', status: true, dataType: 'text', width: 100, sortable: true, searchable: false, filterType: 'select', displayOrder: 6, multiSelectFilter: ['PAID', 'PENDING', 'OVERDUE'] }
    ];
  }
  
  getStatusColor(status: string): string {
    switch (status) {
      case 'PAID': return '#22c55e';    // Green
      case 'PENDING': return '#f59e0b'; // Orange  
      case 'OVERDUE': return '#ef4444'; // Red
      default: return '#666';
    }
  }
  
  getVisibleHeaders(): HeaderConfig[] {
    return this.headerConfig.filter(config => config.status)
                           .sort((a, b) => a.displayOrder - b.displayOrder);
  }
  
  getCellValue(bill: any, config: HeaderConfig): string {
    const value = bill[config.colName];
    
    if (value === null || value === undefined) {
      return '';
    }
    
    // Format based on data type
    switch (config.dataType) {
      case 'number':
        if (config.colName.includes('amount') || config.colName.includes('limit')) {
          return `₹${Number(value).toLocaleString('en-IN')}`;
        }
        return value.toString();
      
      case 'text':
        if (config.colName === 'status') {
          return `<span style="color: ${this.getStatusColor(value)}; font-weight: bold;">${value}</span>`;
        }
        return value.toString();
      
      default:
        return value.toString();
    }
  }
  
  trackByBillId(index: number, bill: CreditBill): number {
    return bill.id;
  }
  
  onSearch() {
    console.log('🔍 Searching for:', this.searchTerm);
    this.currentPage = 1;
    this.loadBillsWithConfig();
  }
  
  onReset() {
    this.searchTerm = '';
    this.currentPage = 1;
    this.loadBillsWithConfig();
  }
  
  goToPage(page: number) {
    if (page >= 1 && page <= Math.ceil(this.totalRecords / this.pageSize)) {
      this.currentPage = page;
      this.loadBillsWithConfig();
    }
  }
  
  // Expose Math for template
  Math = Math;
}