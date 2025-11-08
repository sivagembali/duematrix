import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CardModule } from 'primeng/card';
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
    InputTextModule,
    PasswordModule,
    ButtonModule,
    CheckboxModule,
    MessageModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = signal(false);
  errorMessage = signal<string | null>(null);
  showPassword = signal(false);

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Redirect if already logged in
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }

    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      rememberMe: [false]
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.markFormGroupTouched(this.loginForm);
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);

    const { username, password } = this.loginForm.value;

    // Trim whitespace from username and password
    const trimmedUsername = username?.trim();
    const trimmedPassword = password?.trim();

    this.authService.login({ username: trimmedUsername, password: trimmedPassword }).subscribe({
      next: (response) => {
        this.loading.set(false);
        if (response.success) {
          console.log('Login successful', response.data.user);
          // Navigate to dashboard
          this.router.navigate(['/dashboard']);
        }
      },
      error: (error) => {
        this.loading.set(false);
        console.error('Login error', error);
        
        if (error.error?.error) {
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
