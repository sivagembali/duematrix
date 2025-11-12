import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { DatePicker } from 'primeng/datepicker';
import { Select } from 'primeng/select';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { ToastModule } from 'primeng/toast';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { MessageService, ConfirmationService } from 'primeng/api';
import { DataService } from '../../services/data.service';

interface Cycle {
  id?: number;
  cycle_name: string;
  start_date: Date | string | null;
  end_date: Date | string | null;
  status: string;
  created_at?: string;
  updated_at?: string;
}

@Component({
  selector: 'app-cycle-management',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    DialogModule,
    InputTextModule,
    DatePicker,
    Select,
    CardModule,
    TagModule,
    ToastModule,
    ConfirmDialogModule
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './cycle-management.html',
  styleUrls: ['./cycle-management.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CycleManagementComponent implements OnInit {
  cycles: Cycle[] = [];
  displayDialog: boolean = false;
  cycle: Cycle = this.getEmptyCycle();
  isEditMode: boolean = false;
  loading: boolean = false;

  statusOptions = [
    { label: 'Active', value: 'active' },
    { label: 'Upcoming', value: 'upcoming' },
    { label: 'Closed', value: 'closed' }
  ];

  constructor(
    private dataService: DataService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    setTimeout(() => {
      this.loadCycles();
    });
  }

  loadCycles(): void {
    this.loading = true;
    this.cdr.markForCheck();

    this.dataService.getCycles().subscribe({
      next: (response) => {
        if (response.success) {
          this.cycles = response.data;
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Cycles loaded successfully'
          });
        }
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error: any) => {
        console.error('Error loading cycles:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load cycles'
        });
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  showAddDialog(): void {
    this.cycle = this.getEmptyCycle();
    this.isEditMode = false;
    this.displayDialog = true;
    this.cdr.markForCheck();
  }

  editCycle(cycle: Cycle): void {
    this.cycle = {
      ...cycle,
      start_date: cycle.start_date ? new Date(cycle.start_date) : null,
      end_date: cycle.end_date ? new Date(cycle.end_date) : null
    };
    this.isEditMode = true;
    this.displayDialog = true;
    this.cdr.markForCheck();
  }

  deleteCycle(cycle: Cycle): void {
    this.confirmationService.confirm({
      message: `Are you sure you want to delete cycle "${cycle.cycle_name}"?`,
      header: 'Confirm Delete',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        if (!cycle.id) return;

        this.dataService.deleteCycle(cycle.id).subscribe({
          next: (response: any) => {
            if (response.success) {
              this.messageService.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Cycle deleted successfully'
              });
              this.loadCycles();
            }
          },
          error: (error: any) => {
            console.error('Error deleting cycle:', error);
            const errorMsg = error.error?.message || 'Failed to delete cycle';
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: errorMsg
            });
            this.cdr.markForCheck();
          }
        });
      }
    });
  }

  saveCycle(): void {
    if (!this.cycle.cycle_name?.trim()) {
      this.messageService.add({
        severity: 'warn',
        summary: 'Warning',
        detail: 'Cycle name is required'
      });
      return;
    }

    const cycleData = {
      ...this.cycle,
      start_date: this.cycle.start_date ? new Date(this.cycle.start_date).toISOString().split('T')[0] : null,
      end_date: this.cycle.end_date ? new Date(this.cycle.end_date).toISOString().split('T')[0] : null
    };

    const request = this.isEditMode && this.cycle.id
      ? this.dataService.updateCycle(this.cycle.id, cycleData)
      : this.dataService.createCycle(cycleData);

    request.subscribe({
      next: (response: any) => {
        if (response.success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: `Cycle ${this.isEditMode ? 'updated' : 'created'} successfully`
          });
          this.displayDialog = false;
          this.loadCycles();
        }
      },
      error: (error: any) => {
        console.error('Error saving cycle:', error);
        const errorMsg = error.error?.message || 'Failed to save cycle';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: errorMsg
        });
        this.cdr.markForCheck();
      }
    });
  }

  hideDialog(): void {
    this.displayDialog = false;
    this.cycle = this.getEmptyCycle();
    this.cdr.markForCheck();
  }

  private getEmptyCycle(): Cycle {
    return {
      cycle_name: '',
      start_date: null,
      end_date: null,
      status: 'active'
    };
  }

  getStatusSeverity(status: string): any {
    const severityMap: { [key: string]: string } = {
      'active': 'success',
      'upcoming': 'info',
      'closed': 'secondary'
    };
    return severityMap[status] || 'info';
  }
}
