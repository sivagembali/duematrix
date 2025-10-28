import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// PrimeNG Imports
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { TagModule } from 'primeng/tag';
import { CardModule } from 'primeng/card';
import { ToolbarModule } from 'primeng/toolbar';

import { Api, CreditBill } from '../services/api';

@Component({
  selector: 'app-bills-table',
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    DropdownModule,
    TagModule,
    CardModule,
    ToolbarModule
  ],
  templateUrl: './bills-table.html',
  styleUrl: './bills-table.css'
})
export class BillsTable implements OnInit {
  private apiService = inject(Api);

  // Signals for reactive state
  bills = signal<CreditBill[]>([]);
  loading = signal<boolean>(false);
  
  // Filter properties
  searchValue = '';
  statusOptions = [
    { label: 'All Status', value: '' },
    { label: 'Paid', value: 'PAID' },
    { label: 'Pending', value: 'PENDING' },
    { label: 'Overdue', value: 'OVERDUE' }
  ];
  selectedStatus = '';

  ngOnInit() {
    console.log('🚀 BillsTable component initialized');
    this.loadBills();
  }

  loadBills() {
    this.loading.set(true);
    
    this.apiService.getBills().subscribe({
      next: (response) => {
        console.log('📊 API Response:', response);
        
        this.bills.set(response);
        console.log('✅ Loaded bills:', response.length);
        
        this.loading.set(false);
      },
      error: (error) => {
        console.error('❌ Error loading bills:', error);
        this.loading.set(false);
      }
    });
  }

  onGlobalFilter(event: Event) {
    const target = event.target as HTMLInputElement;
    this.searchValue = target.value;
  }

  onStatusFilter(event: any) {
    this.selectedStatus = event.value;
  }

  getSeverity(status: string): 'success' | 'secondary' | 'info' | 'warn' | 'danger' | 'contrast' {
    switch (status?.toUpperCase()) {
      case 'PAID':
        return 'success';
      case 'PENDING':
        return 'warn';
      case 'OVERDUE':
        return 'danger';
      default:
        return 'info';
    }
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR'
    }).format(value);
  }
}
