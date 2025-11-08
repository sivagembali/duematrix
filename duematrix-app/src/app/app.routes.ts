import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { DashboardComponent } from './components/dashboard/dashboard';
import { UserTable } from './components/user-table/user-table';
import { UserManagementComponent } from './components/user-management/user-management';
import { authGuard } from './guards/auth.guard';
import { adminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { 
    path: 'dashboard', 
    component: DashboardComponent, 
    canActivate: [authGuard],
    children: [
      { path: '', component: UserTable },
      { path: 'data', component: UserTable }
    ]
  },
  { 
    path: 'config', 
    component: DashboardComponent, 
    canActivate: [authGuard, adminGuard],
    children: [
      { path: 'users', component: UserManagementComponent }
    ]
  },
  { path: '**', redirectTo: '/login' }
];
