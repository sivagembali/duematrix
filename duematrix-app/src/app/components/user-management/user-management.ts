import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { Select } from 'primeng/select';
import { CheckboxModule } from 'primeng/checkbox';
import { MessageModule } from 'primeng/message';
import { ToastModule } from 'primeng/toast';
import { Tooltip } from 'primeng/tooltip';
import { ConfirmDialog } from 'primeng/confirmdialog';
import { MessageService, ConfirmationService } from 'primeng/api';
import { UserManagementService } from '../../services/user-management.service';
import { User, Role, RoleMapping } from '../../models/user.model';
import { IstDatePipe } from '../../pipes/ist-date.pipe';

@Component({
  selector: 'app-user-management',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    CardModule,
    TableModule,
    ButtonModule,
    DialogModule,
    InputTextModule,
    PasswordModule,
    Select,
    CheckboxModule,
    MessageModule,
    ToastModule,
    Tooltip,
    ConfirmDialog,
    IstDatePipe
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './user-management.html',
  styleUrl: './user-management.scss'
})
export class UserManagementComponent implements OnInit {
  users = signal<User[]>([]);
  roles = signal<Role[]>([]);
  loading = signal(false);
  
  showCreateUserDialog = signal(false);
  showAssignRoleDialog = signal(false);
  
  createUserForm!: FormGroup;
  assignRoleForm!: FormGroup;
  selectedUser: User | null = null;

  constructor(
    private fb: FormBuilder,
    private userService: UserManagementService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService
  ) {}

  ngOnInit(): void {
    this.initializeForms();
    this.loadUsers();
    this.loadRoles();
  }

  initializeForms(): void {
    this.createUserForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      first_name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      is_active: [true],
      is_verified: [false]
    });

    this.assignRoleForm = this.fb.group({
      role_id: [null, [Validators.required]]
    });
  }

  loadUsers(): void {
    this.loading.set(true);
    this.userService.getUsers().subscribe({
      next: (response) => {
        if (response.success) {
          // Sort users by ID in ascending order
          const sortedUsers = response.data.sort((a, b) => a.id - b.id);
          this.users.set(sortedUsers);
        }
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error loading users', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to load users'
        });
        this.loading.set(false);
      }
    });
  }

  loadRoles(): void {
    this.userService.getRoles().subscribe({
      next: (response) => {
        if (response.success) {
          this.roles.set(response.data);
        }
      },
      error: (error) => {
        console.error('Error loading roles', error);
      }
    });
  }

  openCreateUserDialog(): void {
    this.createUserForm.reset({
      is_active: true,
      is_verified: false
    });
    this.showCreateUserDialog.set(true);
  }

  closeCreateUserDialog(): void {
    this.showCreateUserDialog.set(false);
  }

  createUser(): void {
    if (this.createUserForm.invalid) {
      this.markFormGroupTouched(this.createUserForm);
      return;
    }

    this.loading.set(true);
    this.userService.createUser(this.createUserForm.value).subscribe({
      next: (response) => {
        if (response.success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'User created successfully'
          });
          this.loadUsers();
          this.closeCreateUserDialog();
        }
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error creating user', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error.error?.error || 'Failed to create user'
        });
        this.loading.set(false);
      }
    });
  }

  openAssignRoleDialog(user: User): void {
    this.selectedUser = user;
    this.assignRoleForm.reset();
    this.showAssignRoleDialog.set(true);
  }

  closeAssignRoleDialog(): void {
    this.showAssignRoleDialog.set(false);
    this.selectedUser = null;
  }

  assignRole(): void {
    if (this.assignRoleForm.invalid || !this.selectedUser) {
      return;
    }

    const data = {
      user_id: this.selectedUser.id,
      role_id: this.assignRoleForm.value.role_id
    };

    this.loading.set(true);
    this.userService.assignRole(data).subscribe({
      next: (response) => {
        if (response.success) {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Role assigned successfully'
          });
          this.loadUsers();
          this.closeAssignRoleDialog();
        }
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Error assigning role', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error.error?.error || 'Failed to assign role'
        });
        this.loading.set(false);
      }
    });
  }

  toggleUserStatus(user: User): void {
    const newStatus = !user.is_active;
    const action = newStatus ? 'activate' : 'deactivate';
    
    this.confirmationService.confirm({
      message: `Are you sure you want to ${action} user "${user.username}"?`,
      header: `${action.charAt(0).toUpperCase() + action.slice(1)} User`,
      icon: newStatus ? 'pi pi-check-circle' : 'pi pi-exclamation-triangle',
      acceptLabel: 'Yes',
      rejectLabel: 'No',
      acceptButtonStyleClass: newStatus ? 'p-button-success' : 'p-button-danger',
      rejectButtonStyleClass: 'p-button-text',
      accept: () => {
        this.loading.set(true);
        this.userService.updateUserStatus(user.id, newStatus).subscribe({
          next: (response) => {
            if (response.success) {
              this.messageService.add({
                severity: 'success',
                summary: 'Success',
                detail: `User ${action}d successfully`
              });
              this.loadUsers();
            }
            this.loading.set(false);
          },
          error: (error) => {
            console.error('Error updating user status', error);
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: error.error?.error || 'Failed to update user status'
            });
            this.loading.set(false);
          }
        });
      }
    });
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();
    });
  }

  getRoleName(roleId: number | null): string {
    if (!roleId) return 'No Role';
    const role = this.roles().find(r => r.id === roleId);
    return role?.role_name || 'Unknown';
  }
}
