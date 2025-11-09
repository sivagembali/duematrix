import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { TableModule } from 'primeng/table';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { MultiSelectModule } from 'primeng/multiselect';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { ColumnHeader, DataRow, CustomerData } from '../../models/data.model';
import { MockDataGenerator } from '../../services/mock-data.service';
import { DataService } from '../../services/data.service';
import { CycleService } from '../../services/cycle.service';
import { AuthService } from '../../services/auth.service';
import { firstValueFrom, Subscription } from 'rxjs';

@Component({
  selector: 'app-user-table',
  imports: [CommonModule, TableModule, FormsModule, InputTextModule, MultiSelectModule, ButtonModule, ToastModule],
  providers: [MessageService],
  templateUrl: './user-table.html',
  styleUrl: './user-table.scss',
})
export class UserTable implements OnInit, OnDestroy {
  dataset: DataRow[] = [];
  columnHeaders: ColumnHeader[] = [];
  displayedColumns: ColumnHeader[] = [];
  frozenColumns: ColumnHeader[] = []; // Columns with is_frozen = true
  scrollableColumns: ColumnHeader[] = []; // Non-frozen columns
  availableColumns: ColumnHeader[] = []; // All columns available for selection
  selectedColumns: ColumnHeader[] = []; // Currently selected columns
  multiSelectOptions: { [key: string]: string[] } = {};
  selectedFilters: { [key: string]: string[] } = {};
  filterValues: { [key: string]: string } = {};
  filteredDataset: DataRow[] = [];
  loading: boolean = false;
  saving: boolean = false;
  totalRecords: number = 0;
  
  // Track edited records
  editedRecords: Map<string, DataRow> = new Map(); // key: id, value: edited row data
  originalRecords: Map<string, DataRow> = new Map(); // key: id, value: original row data
  private cycleSubscription?: Subscription;

  constructor(
    private mockDataGenerator: MockDataGenerator,
    private dataService: DataService,
    private cdr: ChangeDetectorRef,
    private messageService: MessageService,
    private cycleService: CycleService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    console.log('[UserTable] ngOnInit called');
    
    // Load column headers from AuthService (which are loaded by Dashboard from API)
    // Subscribe to headers to get updates
    this.authService.headers$.subscribe(headers => {
      console.log('[UserTable] Headers received from AuthService:', headers.length);
      if (headers && headers.length > 0) {
        this.columnHeaders = headers;
        this.initializeColumnsAndFilters();
      } else {
        // Fallback to mock headers if not available yet
        console.warn('[UserTable] No headers from AuthService, using mock headers');
        this.columnHeaders = this.mockDataGenerator.generateHeaderMapping();
        this.initializeColumnsAndFilters();
      }
    });

    // Subscribe to cycle selection changes and load data accordingly
    this.cycleSubscription = this.cycleService.selectedCycle$.subscribe(cycle => {
      console.log('[UserTable] Cycle changed:', cycle);
      if (cycle) {
        console.log('[UserTable] Loading data for cycle:', cycle);
        this.loadCustomerData(cycle);
      } else {
        console.log('[UserTable] No cycle selected, clearing dataset');
        // No cycle selected yet: clear dataset to avoid an unnecessary API call
        this.dataset = [];
        this.filteredDataset = [];
        this.totalRecords = 0;
      }
    });
  }

  private initializeColumnsAndFilters() {
    console.log('[UserTable] Initializing columns and filters');
    
    // Store all columns that can be displayed
    this.availableColumns = this.columnHeaders
      .filter(col => col.display)
      .sort((a, b) => {
        // Sort frozen columns first, then by display_order
        if (a.is_frozen !== b.is_frozen) {
          return a.is_frozen ? -1 : 1;
        }
        return a.display_order - b.display_order;
      });
    
    console.log('[UserTable] Available columns:', this.availableColumns.length);
    
    // Initialize selected columns with default_display columns
    this.selectedColumns = this.availableColumns.filter(col => col.default_display);
    
    console.log('[UserTable] Selected columns:', this.selectedColumns.length);
    
    // Update displayed columns based on selected columns - frozen first
    this.updateDisplayedColumns();

    // Initialize filter objects
    this.displayedColumns.forEach(col => {
      if (col.is_multi_select) {
        this.selectedFilters[col.col_header] = [];
      } else {
        this.filterValues[col.col_header] = '';
      }
    });
    
    console.log('[UserTable] Displayed columns:', this.displayedColumns.length);
  }

  loadCustomerData(cycle?: string) {
    this.loading = true;
    console.log('Starting to load customer data from API...');
    
    this.dataService.getCustomerData({ per_page: 100, cycle }).subscribe({
      next: (response) => {
        console.log('API Response received:', response);
        console.log('Response data array length:', response.data?.length);
        
        // Transform CustomerData to DataRow format
        this.dataset = response.data.map(customer => this.transformCustomerData(customer));
        this.totalRecords = response.pagination?.total || response.data.length;
        this.filteredDataset = [...this.dataset];
        
        console.log('Transformed dataset:', this.dataset);
        console.log('Dataset length:', this.dataset.length);
        console.log('First record:', this.dataset[0]);
        
        // Store original records for comparison
        this.dataset.forEach(row => {
          this.originalRecords.set(row['id'].toString(), { ...row });
        });

        // Generate filter options for multi-select columns
        this.generateMultiSelectOptions();
        
        this.loading = false;
        
        console.log('✅ Customer data loaded successfully!');
        console.log('Total Records:', this.totalRecords);
        console.log('Filtered Dataset length:', this.filteredDataset.length);
        
        // Manually trigger change detection to update the view
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('❌ Error loading customer data:', error);
        console.error('Error status:', error.status);
        console.error('Error message:', error.message);
        console.error('Error details:', error.error);
        
        this.loading = false;
        
        // Fallback to mock data on error
        console.warn('⚠️ Falling back to mock data generator');
        this.dataset = this.mockDataGenerator.generateDataset(100);
        this.filteredDataset = [...this.dataset];
        
        console.log('Mock dataset length:', this.dataset.length);
        
        // Store original records for comparison
        this.dataset.forEach(row => {
          this.originalRecords.set(row['id'].toString(), { ...row });
        });

        // Generate filter options for multi-select columns
        this.generateMultiSelectOptions();
        
        console.log('Using Mock Data - Total:', this.dataset.length);
        
        // Manually trigger change detection for zoneless mode
        this.cdr.detectChanges();
      }
    });
  }

  ngOnDestroy(): void {
    if (this.cycleSubscription) {
      this.cycleSubscription.unsubscribe();
    }
  }

  // Transform CustomerData from API to DataRow format
  private transformCustomerData(customer: CustomerData): DataRow {
    return {
      id: customer.id,
      user_id: customer.user_id,
      customer_name: customer.customer_name,
      email: customer.email,
      phone_number: customer.phone_number,
      date_of_birth: customer.date_of_birth,
      blood_group: customer.blood_group,
      nationality: customer.nationality,
      marital_status: customer.marital_status,
      spouse_name: customer.spouse_name,
      children_count: customer.children_count,
      emergency_contact: customer.emergency_contact,
      current_address: customer.current_address,
      city: customer.city,
      state: customer.state,
      postal_code: customer.postal_code,
      country: customer.country,
      credit_card_no: customer.credit_card_no,
      account_balance: customer.account_balance?.toString(),
      account_type: customer.account_type,
      bank: customer.bank,
      bank_name: customer.bank_name,
      bank_account_no: customer.bank_account_no,
      ifsc_code: customer.ifsc_code,
      branch_name: customer.branch_name,
      pan_number: customer.pan_number,
      aadhar_number: customer.aadhar_number,
      annual_income: customer.annual_income?.toString(),
      tax_regime: customer.tax_regime,
      insurance_policy_no: customer.insurance_policy_no,
      employee_id: customer.employee_id,
      department: customer.department,
      status: customer.status,
      salary: customer.salary?.toString(),
      hire_date: customer.hire_date,
      manager_name: customer.manager_name,
      work_location: customer.work_location,
      remote_work_eligible: customer.remote_work_eligible,
      project_name: customer.project_name,
      project_code: customer.project_code,
      cycle_name: customer.cycle_name,
      skill_set: customer.skill_set,
      experience_years: customer.experience_years,
      education: customer.education,
      certification: customer.certification,
      performance_rating: customer.performance_rating?.toString(),
      last_appraisal_date: customer.last_appraisal_date,
      next_appraisal_date: customer.next_appraisal_date,
      vehicle_type: customer.vehicle_type,
      vehicle_number: customer.vehicle_number,
      registration_date: customer.registration_date,
      last_login: customer.last_login,
      notes: customer.notes
    };
  }

  // Update displayed columns - frozen first, then scrollable
  updateDisplayedColumns() {
    const sorted = [...this.selectedColumns].sort((a, b) => {
      // Frozen columns come first
      if (a.is_frozen !== b.is_frozen) {
        return a.is_frozen ? -1 : 1;
      }
      return a.display_order - b.display_order;
    });
    
    this.displayedColumns = sorted;
    this.frozenColumns = sorted.filter(col => col.is_frozen);
    this.scrollableColumns = sorted.filter(col => !col.is_frozen);
  }

  // Called when column selection changes
  onColumnSelectionChange() {
    this.updateDisplayedColumns();
    
    // Regenerate multiselect options for all displayed columns
    this.generateMultiSelectOptions();
    
    // Update filter objects for new columns
    this.displayedColumns.forEach(col => {
      if (col.is_multi_select && !this.selectedFilters[col.col_header]) {
        this.selectedFilters[col.col_header] = [];
      } else if (!col.is_multi_select && this.filterValues[col.col_header] === undefined) {
        this.filterValues[col.col_header] = '';
      }
    });
    
    // Reapply filters with new column set
    this.applyFilters();
  }

  generateMultiSelectOptions() {
    const multiSelectColumns = this.displayedColumns.filter(col => col.is_multi_select);
    
    multiSelectColumns.forEach(column => {
      const uniqueValues = new Set<string>();
      this.dataset.forEach(row => {
        const value = row[column.col_header];
        if (value) {
          uniqueValues.add(value.toString());
        }
      });
      
      this.multiSelectOptions[column.col_header] = Array.from(uniqueValues).sort();
    });
  }

  onFilterChange(event: any, field: string) {
    this.applyFilters();
  }

  onTextFilterChange(event: any, field: string) {
    this.applyFilters();
  }

  applyFilters() {
    this.filteredDataset = this.dataset.filter(row => {
      // Check all multi-select filters
      for (const field in this.selectedFilters) {
        const selectedValues = this.selectedFilters[field];
        if (selectedValues && selectedValues.length > 0) {
          const rowValue = row[field]?.toString() || '';
          if (!selectedValues.includes(rowValue)) {
            return false;
          }
        }
      }

      // Check all text filters
      for (const field in this.filterValues) {
        const filterValue = this.filterValues[field];
        if (filterValue && filterValue.trim() !== '') {
          const rowValue = row[field]?.toString().toLowerCase() || '';
          if (!rowValue.includes(filterValue.toLowerCase())) {
            return false;
          }
        }
      }

      return true;
    });
  }

  getColumnWidth(column: ColumnHeader): string {
    return column.col_width ? `${column.col_width}rem` : 'auto';
  }

  // Calculate the left position for frozen columns
  getFrozenColumnLeft(column: ColumnHeader): string {
    const frozenIndex = this.displayedColumns
      .filter(col => col.is_frozen)
      .findIndex(col => col.col_header === column.col_header);
    
    if (frozenIndex === 0) {
      return '0px';
    }
    
    // Calculate cumulative width of previous frozen columns
    let cumulativeWidth = 0;
    const frozenCols = this.displayedColumns.filter(col => col.is_frozen);
    
    for (let i = 0; i < frozenIndex; i++) {
      const width = frozenCols[i].col_width || 12.5; // Default to 12.5rem (200px)
      cumulativeWidth += width;
    }
    
    return `${cumulativeWidth}rem`;
  }

  // Track cell value changes
  onCellChange(row: DataRow) {
    const rowId = row.id.toString();
    
    // Store original if not already stored
    if (!this.originalRecords.has(rowId)) {
      // Store a deep copy of the original row
      this.originalRecords.set(rowId, JSON.parse(JSON.stringify(row)));
    }
    
    // Check if row has changes compared to original
    const original = this.originalRecords.get(rowId);
    const hasChanges = original && Object.keys(row).some(key => row[key] !== original[key]);
    
    if (hasChanges) {
      this.editedRecords.set(rowId, { ...row });
    } else {
      this.editedRecords.delete(rowId);
    }
  }

  // Save all edited records to backend
  async saveAllEdits() {
    if (this.editedRecords.size === 0) {
      return;
    }

    this.saving = true;
    let successCount = 0;
    let failCount = 0;

    const editedRecordsArray = Array.from(this.editedRecords.values());

    for (const record of editedRecordsArray) {
      try {
        const response = await firstValueFrom(
          this.dataService.updateCustomerData(record.id, record)
        );

        if (response && response.success) {
          successCount++;
          // Update original record to match saved state
          this.originalRecords.set(record.id.toString(), { ...record });
          // Remove from edited records
          this.editedRecords.delete(record.id.toString());
        } else {
          failCount++;
        }
      } catch (error) {
        failCount++;
        console.error(`Failed to save record ${record.id}:`, error);
      }
    }

    this.saving = false;

    // Show success message
    if (successCount > 0) {
      this.messageService.add({
        severity: 'success',
        summary: 'Save Complete',
        detail: `Successfully saved ${successCount} record${successCount > 1 ? 's' : ''}`,
        life: 3000
      });
    }

    // Show error message if any failed
    if (failCount > 0) {
      this.messageService.add({
        severity: 'error',
        summary: 'Save Failed',
        detail: `Failed to save ${failCount} record${failCount > 1 ? 's' : ''}`,
        life: 5000
      });
    }
  }

  // Get all edited records ready for database save
  getEditedRecordsForSave(): DataRow[] {
    return Array.from(this.editedRecords.values());
  }

  // Get edited records with their changes (delta)
  getEditedRecordsWithChanges(): Array<{ id: string, original: DataRow, edited: DataRow, changes: any }> {
    const editedWithChanges: Array<{ id: string, original: DataRow, edited: DataRow, changes: any }> = [];
    
    this.editedRecords.forEach((editedRow, id) => {
      const originalRow = this.originalRecords.get(id);
      if (originalRow) {
        const changes: any = {};
        for (const key in editedRow) {
          if (editedRow[key] !== originalRow[key]) {
            changes[key] = {
              old: originalRow[key],
              new: editedRow[key]
            };
          }
        }
        
        editedWithChanges.push({
          id,
          original: originalRow,
          edited: editedRow,
          changes
        });
      }
    });
    
    return editedWithChanges;
  }

  // Clear all tracked edits
  clearEditedRecords() {
    this.editedRecords.clear();
    console.log('All edited records cleared');
  }

  // Check if there are unsaved changes
  hasUnsavedChanges(): boolean {
    return this.editedRecords.size > 0;
  }

  // Show edited records in console (can be replaced with dialog)
  showEditedRecords() {
    const editedWithChanges = this.getEditedRecordsWithChanges();
    console.log('=== EDITED RECORDS READY FOR DATABASE ===');
    console.log('Total edited records:', this.editedRecords.size);
    console.log('\nFull edited records:', this.getEditedRecordsForSave());
    console.log('\nChanges details:', editedWithChanges);
    
    // You can replace this with a dialog/modal display
    alert(`Total edited records: ${this.editedRecords.size}\n\nCheck console for details.`);
  }

  // Export edited records as JSON (ready for API call)
  exportEditedRecords() {
    const editedRecords = this.getEditedRecordsForSave();
    const editedWithChanges = this.getEditedRecordsWithChanges();
    
    const dataToExport = {
      editedRecords,
      changesDetails: editedWithChanges,
      timestamp: new Date().toISOString(),
      totalChanges: this.editedRecords.size
    };
    
    console.log('=== EXPORTED DATA FOR DATABASE ===');
    console.log(JSON.stringify(dataToExport, null, 2));
    
    // Download as JSON file
    const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `edited-records-${new Date().getTime()}.json`;
    a.click();
    window.URL.revokeObjectURL(url);
    
    alert(`Exported ${this.editedRecords.size} edited records to JSON file.`);
  }

  // Export filtered data as CSV
  exportFilteredDataAsCSV() {
    if (this.filteredDataset.length === 0) {
      alert('No data to export. Please adjust your filters.');
      return;
    }

    // Get displayed column headers
    const headers = this.displayedColumns.map(col => col.col_label);
    const headerKeys = this.displayedColumns.map(col => col.col_header);

    // Create CSV content
    let csvContent = headers.join(',') + '\n';

    // Add data rows
    this.filteredDataset.forEach(row => {
      const rowData = headerKeys.map(key => {
        const value = row[key];
        // Handle values that contain commas, quotes, or newlines
        if (value === null || value === undefined) {
          return '';
        }
        const stringValue = String(value);
        if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
          // Escape quotes and wrap in quotes
          return `"${stringValue.replace(/"/g, '""')}"`;
        }
        return stringValue;
      });
      csvContent += rowData.join(',') + '\n';
    });

    // Create and download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `filtered-data-${new Date().getTime()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);

    console.log(`Exported ${this.filteredDataset.length} filtered records to CSV`);
  }
}
