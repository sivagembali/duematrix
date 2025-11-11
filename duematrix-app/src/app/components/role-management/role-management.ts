import { Component, OnInit, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TagModule } from 'primeng/tag';
import { CardModule } from 'primeng/card';
import { MessageService, ConfirmationService } from 'primeng/api';
import { RoleService, Role, CreateRoleRequest, UpdateRoleRequest } from '../../services/role.service';

@Component({
  selector: 'app-role-management',
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
    TagModule,
    CardModule
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './role-management.html',
  styleUrl: './role-management.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RoleManagementComponent implements OnInit {
  roles: Role[] = [];
  loading: boolean = false;
  showDialog: boolean = false;
  dialogMode: 'create' | 'edit' = 'create';
  
  // Form data
  selectedRole: Role | null = null;
  roleName: string = '';
  roleDescription: string = '';
  isActive: boolean = true;

  constructor(
    private roleService: RoleService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    // Use setTimeout to avoid ExpressionChangedAfterItHasBeenCheckedError
    setTimeout(() => {
      this.loadRoles();
    });
  }

  loadRoles(): void {
    this.loading = true;
    this.cdr.markForCheck();
    this.roleService.getAllRoles().subscribe({
      next: (response) => {
        if (response.success) {
          this.roles = response.data;
          console.log('Roles loaded:', this.roles);
        }
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error) => {
        console.error('Error loading roles:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load roles'
        });
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  openCreateDialog(): void {
    this.dialogMode = 'create';
    this.resetForm();
    this.showDialog = true;
    this.cdr.markForCheck();
  }

  openEditDialog(role: Role): void {
    this.dialogMode = 'edit';
    this.selectedRole = role;
    this.roleName = role.role_name;
    this.roleDescription = role.role_description || '';
    this.isActive = role.is_active;
    this.showDialog = true;
    this.cdr.markForCheck();
  }

  resetForm(): void {
    this.selectedRole = null;
    this.roleName = '';
    this.roleDescription = '';
    this.isActive = true;
  }

  saveRole(): void {
    if (!this.roleName.trim()) {
      this.messageService.add({
        severity: 'warn',
        summary: 'Validation Error',
        detail: 'Role name is required'
      });
      return;
    }

    if (this.dialogMode === 'create') {
      this.createRole();
    } else {
      this.updateRole();
    }
  }

  createRole(): void {
    const roleData: CreateRoleRequest = {
      role_name: this.roleName.trim(),
      role_description: this.roleDescription.trim() || undefined,
      is_active: this.isActive
    };

    this.loading = true;
    this.cdr.markForCheck();
    this.roleService.createRole(roleData).subscribe({
      next: (response) => {
        if (response.success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Role created successfully'
          });
          this.loadRoles();
          this.showDialog = false;
        }
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error) => {
        console.error('Error creating role:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error.error?.error || 'Failed to create role'
        });
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  updateRole(): void {
    if (!this.selectedRole) return;

    const roleData: UpdateRoleRequest = {
      role_name: this.roleName.trim(),
      role_description: this.roleDescription.trim() || undefined,
      is_active: this.isActive
    };

    this.loading = true;
    this.cdr.markForCheck();
    this.roleService.updateRole(this.selectedRole.id, roleData).subscribe({
      next: (response) => {
        if (response.success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Role updated successfully'
          });
          this.loadRoles();
          this.showDialog = false;
        }
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error) => {
        console.error('Error updating role:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error.error?.error || 'Failed to update role'
        });
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  confirmDelete(role: Role): void {
    this.confirmationService.confirm({
      message: `Are you sure you want to delete the role "${role.role_name}"?`,
      header: 'Delete Confirmation',
      icon: 'pi pi-exclamation-triangle',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        this.deleteRole(role.id);
      }
    });
  }

  deleteRole(roleId: number): void {
    this.loading = true;
    this.cdr.markForCheck();
    this.roleService.deleteRole(roleId).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Role deleted successfully'
        });
        this.loadRoles();
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error) => {
        console.error('Error deleting role:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error.error?.error || 'Failed to delete role'
        });
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  getStatusSeverity(isActive: boolean): any {
    return isActive ? 'success' : 'danger';
  }

  cancelDialog(): void {
    this.showDialog = false;
    this.resetForm();
    this.cdr.markForCheck();
  }
}
