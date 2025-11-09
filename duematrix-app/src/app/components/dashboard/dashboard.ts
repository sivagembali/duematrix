import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet, RouterLink } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
// Table and Tag modules removed from dashboard imports since UI section was removed
import { AuthService } from '../../services/auth.service';
import { HeaderService, ColumnHeader } from '../../services/header.service';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, CardModule, ButtonModule, RouterOutlet, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  currentUser: any = null;
  headers: ColumnHeader[] = [];
  loading: boolean = false;

  constructor(
    private authService: AuthService,
    private headerService: HeaderService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUserValue();
    
    // Subscribe to user changes
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    // Always load headers when dashboard loads
    this.loadHeaders();
  }

  loadHeaders(): void {
    this.loading = true;
    this.headerService.getDashboardHeaders().subscribe({
      next: (response) => {
        if (response.success) {
          this.headers = response.data;
          // Update AuthService headers so they're available across the app
          this.authService.setHeaders(response.data);
          console.log('Dashboard: Loaded headers from API', this.headers.length);
        }
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading headers:', error);
        this.loading = false;
      }
    });
  }

  isAdmin(): boolean {
    // Check if user has admin role
    return this.currentUser?.role_name?.toLowerCase() === 'admin';
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: (response) => {
        console.log('Logout successful', response);
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Logout error', error);
        // Still navigate to login even on error (data is already cleared)
        this.router.navigate(['/login']);
      }
    });
  }
}
