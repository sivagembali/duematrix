import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService } from 'primeng/api';
import { MessageService } from 'primeng/api';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { CheckboxModule } from 'primeng/checkbox';
import { MessageModule } from 'primeng/message';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    CardModule,
    ConfirmDialogModule,
    InputTextModule,
    PasswordModule,
    ButtonModule,
    CheckboxModule,
    MessageModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss',
  providers: [ConfirmationService, MessageService]
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = signal(false);
  errorMessage = signal<string | null>(null);
  showPassword = signal(false);
  // store pending credentials when confirmation is required
  private pendingCredentials: any = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
    , private confirmationService: ConfirmationService,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    // Redirect if already logged in
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }

    // Load saved credentials if remember me was checked
    const savedUsername = localStorage.getItem('rememberedUsername');
    const rememberMe = localStorage.getItem('rememberMe') === 'true';

    this.loginForm = this.fb.group({
      username: [savedUsername || '', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      rememberMe: [rememberMe]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.markFormGroupTouched(this.loginForm);
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);

    const { username, password, rememberMe } = this.loginForm.value;

    // Trim whitespace from username and password
    const trimmedUsername = username?.trim();
    const trimmedPassword = password?.trim();

    this.authService.login({ username: trimmedUsername, password: trimmedPassword }).subscribe({
      next: (response) => {
        this.loading.set(false);
        if (response.success) {
          console.log('Login successful', response.data.user);
          
          // Handle remember me functionality
          if (rememberMe) {
            localStorage.setItem('rememberedUsername', trimmedUsername);
            localStorage.setItem('rememberMe', 'true');
          } else {
            localStorage.removeItem('rememberedUsername');
            localStorage.removeItem('rememberMe');
          }
          
          // Navigate to dashboard
          this.router.navigate(['/dashboard']);
        }
      },
      error: (error) => {
        this.loading.set(false);
        console.error('Login error', error);
        
        // If backend reports existing_sessions, prompt to revoke other sessions
        if (error.status === 409 && error.error?.existing_sessions) {
          // store credentials for retry
          this.pendingCredentials = { username: trimmedUsername, password: trimmedPassword };
          this.confirmationService.confirm({
            message: 'You are already logged in on another device or browser. Would you like to end that session and continue here?',
            header: 'Already Logged In',
            icon: 'pi pi-info-circle',
            acceptLabel: 'Yes, Continue Here',
            rejectLabel: 'Cancel',
            acceptButtonStyleClass: 'p-button-success',
            rejectButtonStyleClass: 'p-button-text',
            accept: () => {
              // retry login with force=true
              this.loading.set(true);
              this.authService.login({ ...this.pendingCredentials, force: true }).subscribe({
                next: (resp) => {
                  this.loading.set(false);
                  if (resp.success) {
                    if (rememberMe) {
                      localStorage.setItem('rememberedUsername', trimmedUsername);
                      localStorage.setItem('rememberMe', 'true');
                    }
                    this.router.navigate(['/dashboard']);
                  }
                },
                error: (err2) => {
                  this.loading.set(false);
                  this.messageService.add({severity: 'error', summary: 'Login Failed', detail: err2.error?.error || 'Failed to login after revoking sessions'});
                }
              });
            }
          });
        } else if (error.error?.error) {
          this.errorMessage.set(error.error.error);
        } else if (error.status === 0) {
          this.errorMessage.set('Cannot connect to server. Please ensure the backend is running.');
        } else {
          this.errorMessage.set('Login failed. Please try again.');
        }
      }
    });
  }

  togglePasswordVisibility(): void {
    this.showPassword.set(!this.showPassword());
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();

      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  get username() {
    return this.loginForm.get('username');
  }

  get password() {
    return this.loginForm.get('password');
  }
}
