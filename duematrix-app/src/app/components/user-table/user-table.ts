import { Component, OnInit } from '@angular/core';
import { TableModule } from 'primeng/table';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { MultiSelectModule } from 'primeng/multiselect';
import { ButtonModule } from 'primeng/button';
import { ColumnHeader, DataRow } from '../../models/data.model';
import { MockDataGenerator } from '../../services/mock-data.service';

@Component({
  selector: 'app-user-table',
  imports: [CommonModule, TableModule, FormsModule, InputTextModule, MultiSelectModule, ButtonModule],
  templateUrl: './user-table.html',
  styleUrl: './user-table.scss',
})
export class UserTable implements OnInit {
  dataset: DataRow[] = [];
  columnHeaders: ColumnHeader[] = [];
  displayedColumns: ColumnHeader[] = [];
  availableColumns: ColumnHeader[] = []; // All columns available for selection
  selectedColumns: ColumnHeader[] = []; // Currently selected columns
  multiSelectOptions: { [key: string]: string[] } = {};
  selectedFilters: { [key: string]: string[] } = {};
  filterValues: { [key: string]: string } = {};
  filteredDataset: DataRow[] = [];
  
  // Track edited records
  editedRecords: Map<string, DataRow> = new Map(); // key: id, value: edited row data
  originalRecords: Map<string, DataRow> = new Map(); // key: id, value: original row data
  clonedRows: { [key: string]: DataRow } = {}; // For edit mode cloning

  ngOnInit() {
    // Generate 100 records with 50 columns
    this.dataset = MockDataGenerator.generateDataset(100);
    this.columnHeaders = MockDataGenerator.generateHeaderMapping();
    
    // Store all columns that can be displayed
    this.availableColumns = this.columnHeaders
      .filter(col => col.display)
      .sort((a, b) => a.display_order - b.display_order);
    
    // Initialize selected columns with default_display columns
    this.selectedColumns = this.availableColumns.filter(col => col.default_display);
    
    // Update displayed columns based on selected columns
    this.displayedColumns = [...this.selectedColumns];

    // Generate filter options for multi-select columns
    this.generateMultiSelectOptions();
    
    // Initialize filter objects
    this.displayedColumns.forEach(col => {
      if (col.is_multi_select) {
        this.selectedFilters[col.col_header] = [];
      } else {
        this.filterValues[col.col_header] = '';
      }
    });

    // Store original records for comparison
    this.dataset.forEach(row => {
      this.originalRecords.set(row['id'].toString(), { ...row });
    });

    this.filteredDataset = [...this.dataset];

    console.log('Generated Dataset:', this.dataset);
    console.log('Column Headers:', this.columnHeaders);
    console.log('Displayed Columns (default_display=true):', this.displayedColumns);
    console.log('Column Headers:', this.columnHeaders);
    console.log('MultiSelect Options:', this.multiSelectOptions);
  }

  // Called when column selection changes
  onColumnSelectionChange() {
    this.displayedColumns = [...this.selectedColumns].sort((a, b) => a.display_order - b.display_order);
    
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

  onRowEditInit(row: DataRow) {
    const rowId = row['id'].toString();
    // Clone the row data before editing
    this.clonedRows[rowId] = { ...row };
    console.log('Edit started for row:', row);
  }

  onRowEditSave(row: DataRow) {
    const rowId = row['id'].toString();
    const originalRow = this.originalRecords.get(rowId);
    
    if (originalRow) {
      // Check if any field has changed
      let hasChanges = false;
      for (const key in row) {
        if (row[key] !== originalRow[key]) {
          hasChanges = true;
          break;
        }
      }
      
      if (hasChanges) {
        // Store the edited record
        this.editedRecords.set(rowId, { ...row });
        console.log('Row saved with changes:', row);
        console.log('Total edited records:', this.editedRecords.size);
        console.log('All edited records:', Array.from(this.editedRecords.values()));
      } else {
        // No changes, remove from edited records if it was there
        this.editedRecords.delete(rowId);
        console.log('Row saved without changes:', row);
      }
    }
    
    // Clean up cloned row
    delete this.clonedRows[rowId];
  }

  onRowEditCancel(row: DataRow, index: number) {
    const rowId = row['id'].toString();
    
    // Restore the original values from clone
    if (this.clonedRows[rowId]) {
      Object.assign(row, this.clonedRows[rowId]);
      delete this.clonedRows[rowId];
    }
    
    console.log('Edit cancelled for row:', row);
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
