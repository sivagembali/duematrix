import { Component, OnInit, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService } from 'primeng/api';
import { HeaderService, ColumnHeader } from '../../services/header.service';

@Component({
  selector: 'app-header-mapping',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    DialogModule,
    InputTextModule,
    ToastModule,
    ConfirmDialogModule,
    CardModule,
    TagModule
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './header-mapping.html',
  styleUrl: './header-mapping.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HeaderMappingComponent implements OnInit {
  headers: ColumnHeader[] = [];
  filteredHeaders: ColumnHeader[] = [];
  loading = false;

  showDialog = false;
  dialogMode: 'create' | 'edit' = 'create';

  // Filter values
  filterHeaderKey = '';
  filterLabel = '';

  // form fields
  selectedHeader: ColumnHeader | null = null;
  col_header = '';
  col_label = '';
  is_editable = false;
  is_multi_select = false;
  col_width = 150;
  display = true;
  default_display = true;
  is_frozen = false;
  display_order = 0;
  role_id: number | null = null;

  constructor(
    private headerService: HeaderService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    setTimeout(() => this.loadHeaders());
  }

  loadHeaders(): void {
    this.loading = true;
    this.cdr.markForCheck();
    this.headerService.getAllHeaders().subscribe({
      next: (res) => {
        if (res && res.success) {
          this.headers = res.data || [];
          this.filteredHeaders = [...this.headers];
          this.applyFilters();
        }
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Error loading headers', err);
        this.messageService.add({severity: 'error', summary: 'Error', detail: 'Failed to load headers'});
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  openCreate(): void {
    this.dialogMode = 'create';
    this.resetForm();
    this.showDialog = true;
    this.cdr.markForCheck();
  }

  openEdit(header: ColumnHeader): void {
    this.dialogMode = 'edit';
    this.selectedHeader = header;
    this.col_header = header.col_header;
    this.col_label = header.col_label;
    this.is_editable = !!header.is_editable;
    this.is_multi_select = !!header.is_multi_select;
    this.col_width = header.col_width || 150;
    this.display = !!header.display;
    this.default_display = !!header.default_display;
    this.is_frozen = !!header.is_frozen;
    this.display_order = header.display_order || 0;
    this.role_id = header.role_id;
    this.showDialog = true;
    this.cdr.markForCheck();
  }

  resetForm(): void {
    this.selectedHeader = null;
    this.col_header = '';
    this.col_label = '';
    this.is_editable = false;
    this.is_multi_select = false;
    this.col_width = 150;
    this.display = true;
    this.default_display = true;
    this.is_frozen = false;
    this.display_order = 0;
    this.role_id = null;
  }

  save(): void {
    if (!this.col_header.trim()) {
      this.messageService.add({severity: 'warn', summary: 'Validation', detail: 'Header key is required'});
      return;
    }

    const payload: Partial<ColumnHeader> = {
      col_header: this.col_header.trim(),
      col_label: this.col_label.trim() || undefined,
      is_editable: this.is_editable,
      is_multi_select: this.is_multi_select,
      col_width: this.col_width,
      display: this.display,
      default_display: this.default_display,
      is_frozen: this.is_frozen,
      display_order: this.display_order,
      role_id: this.role_id
    };

    this.loading = true;
    this.cdr.markForCheck();

    if (this.dialogMode === 'create') {
      this.headerService.createHeader(payload).subscribe({
        next: (res) => {
          this.messageService.add({severity: 'success', summary: 'Created', detail: 'Header created'});
          this.loadHeaders();
          this.showDialog = false;
          this.loading = false;
          this.cdr.markForCheck();
        },
        error: (err) => {
          console.error('Create header error', err);
          this.messageService.add({severity: 'error', summary: 'Error', detail: 'Failed to create header'});
          this.loading = false;
          this.cdr.markForCheck();
        }
      });
    } else if (this.selectedHeader) {
      this.headerService.updateHeader(this.selectedHeader.id, payload).subscribe({
        next: (res) => {
          this.messageService.add({severity: 'success', summary: 'Updated', detail: 'Header updated'});
          this.loadHeaders();
          this.showDialog = false;
          this.loading = false;
          this.cdr.markForCheck();
        },
        error: (err) => {
          console.error('Update header error', err);
          this.messageService.add({severity: 'error', summary: 'Error', detail: 'Failed to update header'});
          this.loading = false;
          this.cdr.markForCheck();
        }
      });
    }
  }

  confirmDelete(header: ColumnHeader): void {
    this.confirmationService.confirm({
      message: `Delete header "${header.col_header}"?`,
      header: 'Confirm Delete',
      icon: 'pi pi-exclamation-triangle',
      accept: () => this.deleteHeader(header.id)
    });
  }

  deleteHeader(id: number): void {
    this.loading = true;
    this.cdr.markForCheck();
    this.headerService.deleteHeader(id).subscribe({
      next: () => {
        this.messageService.add({severity: 'success', summary: 'Deleted', detail: 'Header deleted'});
        this.loadHeaders();
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Delete header error', err);
        this.messageService.add({severity: 'error', summary: 'Error', detail: 'Failed to delete header'});
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  filterHeaders(event: Event, field: string): void {
    const value = (event.target as HTMLInputElement).value;
    if (field === 'col_header') {
      this.filterHeaderKey = value;
    } else if (field === 'col_label') {
      this.filterLabel = value;
    }
    this.applyFilters();
  }

  applyFilters(): void {
    this.filteredHeaders = this.headers.filter(h => {
      const matchesKey = !this.filterHeaderKey || 
        h.col_header.toLowerCase().includes(this.filterHeaderKey.toLowerCase());
      const matchesLabel = !this.filterLabel || 
        (h.col_label && h.col_label.toLowerCase().includes(this.filterLabel.toLowerCase()));
      return matchesKey && matchesLabel;
    });
    this.cdr.markForCheck();
  }

  cancel(): void {
    this.showDialog = false;
    this.resetForm();
    this.cdr.markForCheck();
  }

  getEditableSeverity(isEditable: boolean): any {
    return isEditable ? 'success' : 'warning';
  }

  getDisplaySeverity(display: boolean): any {
    return display ? 'success' : 'danger';
  }

  downloadHeaders(): void {
    this.headerService.exportHeaders().subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `headers_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        window.URL.revokeObjectURL(url);
        
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Headers exported successfully'
        });
      },
      error: (error: any) => {
        console.error('Error exporting headers', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to export headers'
        });
      }
    });
  }

  uploadHeaders(event: any): void {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Only CSV files are allowed'
      });
      return;
    }

    this.loading = true;
    this.cdr.markForCheck();

    this.headerService.importHeaders(file).subscribe({
      next: (response: any) => {
        if (response.success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: response.message
          });
          this.loadHeaders();
        }
        this.loading = false;
        this.cdr.markForCheck();
        // Reset file input
        event.target.value = '';
      },
      error: (error: any) => {
        console.error('Error importing headers', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error.error?.error || 'Failed to import headers'
        });
        this.loading = false;
        this.cdr.markForCheck();
        event.target.value = '';
      }
    });
  }
}
