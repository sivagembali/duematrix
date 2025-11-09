import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { take } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterOutlet, RouterLink, NavigationEnd } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
// Table and Tag modules removed from dashboard imports since UI section was removed
import { AuthService } from '../../services/auth.service';
import { HeaderService, ColumnHeader } from '../../services/header.service';
import { CycleService } from '../../services/cycle.service';
import { Subscription, filter } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, FormsModule, CardModule, ButtonModule, RouterOutlet, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit, OnDestroy {
  currentUser: any = null;
  headers: ColumnHeader[] = [];
  loading: boolean = false;
  cycles: any[] = [];
  selectedCycle: string = '';
  private routerSubscription?: Subscription;
  private userSubscription?: Subscription;
  private isInitialized: boolean = false;
  private isLoadingCycles: boolean = false;
  constructor(
    private authService: AuthService,
    private headerService: HeaderService,
    private router: Router,
    private cycleService: CycleService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    console.log('[Dashboard] ngOnInit called, isInitialized:', this.isInitialized);
    this.currentUser = this.authService.getCurrentUserValue();
    console.log('[Dashboard] Current user:', this.currentUser);
    
    // Load initial data
    this.loadDashboardData();
    this.isInitialized = true;
    
    // Subscribe to user changes - this will fire when login happens
    this.userSubscription = this.authService.currentUser$.subscribe(user => {
      console.log('[Dashboard] User changed:', user, 'previous:', this.currentUser);
      
      // Only reload if user actually changed (not initial subscription emission)
      if (this.isInitialized && user && user !== this.currentUser) {
        console.log('[Dashboard] Different user detected, reloading data');
        this.currentUser = user;
        this.loadDashboardData();
      } else {
        this.currentUser = user;
      }
    });

    // Listen for navigation events to reload data when returning to dashboard
    this.routerSubscription = this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      console.log('[Dashboard] Navigation event:', event.url);
      // Reload dashboard data when navigating to dashboard route
      if (event.url === '/dashboard' || event.url.startsWith('/dashboard')) {
        console.log('[Dashboard] Navigated to dashboard, reloading data');
        this.loadDashboardData();
      }
    });
  }

  private loadDashboardData(): void {
    console.log('[Dashboard] loadDashboardData called');
    
    // Prevent multiple simultaneous loads
    if (this.isLoadingCycles) {
      console.log('[Dashboard] Already loading cycles, skipping duplicate call');
      return;
    }
    
    // Always load headers when dashboard loads
    this.loadHeaders();

    // Load cycles and auto-select/publish the first one
    console.log('[Dashboard] Loading cycles...');
    this.isLoadingCycles = true;
    
    this.cycleService.loadCycles().subscribe({
      next: (res) => {
        console.log('[Dashboard] Cycles loaded, raw response:', res);
        const data = (res && (res as any).data) ? (res as any).data : (Array.isArray(res) ? res : []);
        this.cycles = data || [];
        console.log('[Dashboard] Processed cycles:', this.cycles);
        
        if (this.cycles.length > 0) {
          const defaultCycle = this.cycles[0].cycle_name;
          console.log('[Dashboard] Auto-selecting first cycle:', defaultCycle);
          
          // Set the selected cycle and publish to service
          this.selectedCycle = defaultCycle;
          
          // Use microtask to ensure DOM is updated before publishing
          queueMicrotask(() => {
            console.log('[Dashboard] Publishing cycle to service:', this.selectedCycle);
            this.cycleService.setSelectedCycle(this.selectedCycle);
            this.cdr.detectChanges();
          });
        } else {
          console.warn('[Dashboard] No cycles available');
        }
        
        this.isLoadingCycles = false;
      },
      error: (err) => {
        console.error('[Dashboard] Error loading cycles:', err);
        this.isLoadingCycles = false;
      }
    });
  }

  ngOnDestroy(): void {
    console.log('[Dashboard] ngOnDestroy called');
    if (this.routerSubscription) {
      this.routerSubscription.unsubscribe();
    }
    if (this.userSubscription) {
      this.userSubscription.unsubscribe();
    }
    this.isInitialized = false;
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

  onCycleChange(cycle: string) {
    this.selectedCycle = cycle;
    this.cycleService.setSelectedCycle(cycle);
  }

  isAdmin(): boolean {
    // Check if user has admin role
    return this.currentUser?.role_name?.toLowerCase() === 'admin';
  }

  logout(): void {
    console.log('[Dashboard] Logout initiated');
    this.authService.logout().subscribe({
      next: (response) => {
        console.log('[Dashboard] Logout successful', response);
        // Reset cycle service to clear any selected cycle
        this.cycleService.reset();
        console.log('[Dashboard] Navigating to login');
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('[Dashboard] Logout error', error);
        // Still navigate to login and reset cycle service even on error
        this.cycleService.reset();
        this.router.navigate(['/login']);
      }
    });
  }
}
