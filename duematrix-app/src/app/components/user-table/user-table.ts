import { Component, OnInit } from '@angular/core';
import { TableModule } from 'primeng/table';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { MultiSelectModule } from 'primeng/multiselect';
import { ColumnHeader, DataRow } from '../../models/data.model';
import { MockDataGenerator } from '../../services/mock-data.service';

@Component({
  selector: 'app-user-table',
  imports: [CommonModule, TableModule, FormsModule, InputTextModule, MultiSelectModule],
  templateUrl: './user-table.html',
  styleUrl: './user-table.scss',
})
export class UserTable implements OnInit {
  dataset: DataRow[] = [];
  columnHeaders: ColumnHeader[] = [];
  displayedColumns: ColumnHeader[] = [];
  multiSelectOptions: { [key: string]: string[] } = {};
  selectedFilters: { [key: string]: string[] } = {};
  filterValues: { [key: string]: string } = {};
  filteredDataset: DataRow[] = [];

  ngOnInit() {
    // Generate 100 records with 50 columns
    this.dataset = MockDataGenerator.generateDataset(100);
    this.columnHeaders = MockDataGenerator.generateHeaderMapping();
    
    // Filter only displayed columns and sort by display_order
    this.displayedColumns = this.columnHeaders
      .filter(col => col.display)
      .sort((a, b) => a.display_order - b.display_order);

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

    this.filteredDataset = [...this.dataset];

    console.log('Generated Dataset:', this.dataset);
    console.log('Column Headers:', this.columnHeaders);
    console.log('MultiSelect Options:', this.multiSelectOptions);
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
    console.log('Edit started for row:', row);
  }

  onRowEditSave(row: DataRow) {
    console.log('Row saved:', row);
  }

  onRowEditCancel(row: DataRow, index: number) {
    console.log('Edit cancelled for row:', row);
  }
}
