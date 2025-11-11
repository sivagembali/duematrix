import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-config-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './config-layout.html',
  styleUrl: './config-layout.scss'
})
export class ConfigLayoutComponent implements OnInit {
  
  menuItems = [
    { label: 'User Management', icon: 'pi pi-users', route: '/config/users' },
    { label: 'Role Management', icon: 'pi pi-key', route: '/config/roles' },
    { label: 'Header Mapping', icon: 'pi pi-table', route: '/config/headers' }
  ];

  constructor() {}

  ngOnInit(): void {
    console.log('[ConfigLayout] Initialized');
  }
}
