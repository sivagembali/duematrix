import { Component, OnInit } from '@angular/core';
import { TableModule } from 'primeng/table';
import { CommonModule } from '@angular/common';
import { ColumnHeader, DataRow } from '../../models/data.model';
import { MockDataGenerator } from '../../services/mock-data.service';

@Component({
  selector: 'app-user-table',
  imports: [CommonModule, TableModule],
  templateUrl: './user-table.html',
  styleUrl: './user-table.scss',
})
export class UserTable implements OnInit {
  dataset: DataRow[] = [];
  columnHeaders: ColumnHeader[] = [];
  displayedColumns: ColumnHeader[] = [];

  ngOnInit() {
    // Generate 100 records with 50 columns
    this.dataset = MockDataGenerator.generateDataset(100);
    this.columnHeaders = MockDataGenerator.generateHeaderMapping();
    
    // Filter only displayed columns and sort by display_order
    this.displayedColumns = this.columnHeaders
      .filter(col => col.display)
      .sort((a, b) => a.display_order - b.display_order);

    console.log('Generated Dataset:', this.dataset);
    console.log('Column Headers:', this.columnHeaders);
  }

  getColumnWidth(column: ColumnHeader): string {
    return column.col_width ? `${column.col_width}rem` : 'auto';
  }
}
