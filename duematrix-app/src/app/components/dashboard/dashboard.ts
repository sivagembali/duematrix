import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { AuthService } from '../../services/auth.service';
import { UserTable } from '../user-table/user-table';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, CardModule, ButtonModule, UserTable],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  currentUser: any = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUserValue();
    
    // Subscribe to user changes
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
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
