import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardModule } from 'primeng/card';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { DataService } from '../../services/data.service';
import { CycleService } from '../../services/cycle.service';

interface CycleStats {
  cycle_name: string;
  customer_count: number;
  active_count: number;
  inactive_count: number;
}

interface StatusStats {
  status: string;
  count: number;
  percentage: number;
}

interface DepartmentStats {
  department: string;
  count: number;
  avg_salary: number;
}

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, CardModule, TableModule, TagModule, ButtonModule],
  templateUrl: './reports.html',
  styleUrl: './reports.scss'
})
export class ReportsComponent implements OnInit {
  loading: boolean = false;
  cycleStats: CycleStats[] = [];
  statusStats: StatusStats[] = [];
  departmentStats: DepartmentStats[] = [];
  totalCustomers: number = 0;
  
  constructor(
    private dataService: DataService,
    private cycleService: CycleService
  ) {}

  ngOnInit(): void {
    this.loadReports();
  }

  loadReports(): void {
    this.loading = true;
    console.log('[Reports] Loading customer data for analysis');
    
    // Fetch all customer data (or a large sample)
    this.dataService.getCustomerData({ per_page: 1000 }).subscribe({
      next: (response) => {
        console.log('[Reports] Data loaded:', response.data.length, 'records');
        const customers = response.data;
        this.totalCustomers = response.pagination?.total || customers.length;
        
        // Calculate cycle statistics
        this.calculateCycleStats(customers);
        
        // Calculate status statistics
        this.calculateStatusStats(customers);
        
        // Calculate department statistics
        this.calculateDepartmentStats(customers);
        
        this.loading = false;
      },
      error: (error) => {
        console.error('[Reports] Error loading data:', error);
        this.loading = false;
      }
    });
  }

  private calculateCycleStats(customers: any[]): void {
    const cycleMap = new Map<string, { total: number; active: number; inactive: number }>();
    
    customers.forEach(customer => {
      const cycle = customer.cycle_name || 'Unknown';
      const status = customer.status?.toLowerCase() || '';
      
      if (!cycleMap.has(cycle)) {
        cycleMap.set(cycle, { total: 0, active: 0, inactive: 0 });
      }
      
      const stats = cycleMap.get(cycle)!;
      stats.total++;
      
      if (status === 'active') {
        stats.active++;
      } else if (status === 'inactive') {
        stats.inactive++;
      }
    });
    
    this.cycleStats = Array.from(cycleMap.entries()).map(([cycle_name, stats]) => ({
      cycle_name,
      customer_count: stats.total,
      active_count: stats.active,
      inactive_count: stats.inactive
    })).sort((a, b) => b.customer_count - a.customer_count);
    
    console.log('[Reports] Cycle stats:', this.cycleStats);
  }

  private calculateStatusStats(customers: any[]): void {
    const statusMap = new Map<string, number>();
    
    customers.forEach(customer => {
      const status = customer.status || 'Unknown';
      statusMap.set(status, (statusMap.get(status) || 0) + 1);
    });
    
    const total = customers.length;
    this.statusStats = Array.from(statusMap.entries()).map(([status, count]) => ({
      status,
      count,
      percentage: total > 0 ? Math.round((count / total) * 100) : 0
    })).sort((a, b) => b.count - a.count);
    
    console.log('[Reports] Status stats:', this.statusStats);
  }

  private calculateDepartmentStats(customers: any[]): void {
    const deptMap = new Map<string, { count: number; totalSalary: number }>();
    
    customers.forEach(customer => {
      const dept = customer.department || 'Unknown';
      const salary = parseFloat(customer.salary) || 0;
      
      if (!deptMap.has(dept)) {
        deptMap.set(dept, { count: 0, totalSalary: 0 });
      }
      
      const stats = deptMap.get(dept)!;
      stats.count++;
      stats.totalSalary += salary;
    });
    
    this.departmentStats = Array.from(deptMap.entries()).map(([department, stats]) => ({
      department,
      count: stats.count,
      avg_salary: stats.count > 0 ? Math.round(stats.totalSalary / stats.count) : 0
    })).sort((a, b) => b.count - a.count);
    
    console.log('[Reports] Department stats:', this.departmentStats);
  }

  getStatusSeverity(status: string): any {
    const statusLower = status?.toLowerCase() || '';
    if (statusLower === 'active') return 'success';
    if (statusLower === 'inactive') return 'secondary';
    if (statusLower === 'pending') return 'warning';
    return 'info';
  }

  refreshReports(): void {
    this.loadReports();
  }
}
