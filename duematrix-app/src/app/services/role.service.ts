import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Role {
  id: number;
  role_name: string;
  role_description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  created_by?: number;
  updated_by?: number;
}

export interface RoleResponse {
  success: boolean;
  data: Role[];
}

export interface SingleRoleResponse {
  success: boolean;
  data: Role;
}

export interface CreateRoleRequest {
  role_name: string;
  role_description?: string;
  is_active?: boolean;
}

export interface UpdateRoleRequest {
  role_name?: string;
  role_description?: string;
  is_active?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class RoleService {
  private apiUrl = 'http://localhost:5000/api/roles';

  constructor(private http: HttpClient) {}

  getAllRoles(): Observable<RoleResponse> {
    return this.http.get<RoleResponse>(this.apiUrl);
  }

  getRole(roleId: number): Observable<SingleRoleResponse> {
    return this.http.get<SingleRoleResponse>(`${this.apiUrl}/${roleId}`);
  }

  createRole(role: CreateRoleRequest): Observable<SingleRoleResponse> {
    return this.http.post<SingleRoleResponse>(this.apiUrl, role);
  }

  updateRole(roleId: number, role: UpdateRoleRequest): Observable<SingleRoleResponse> {
    return this.http.put<SingleRoleResponse>(`${this.apiUrl}/${roleId}`, role);
  }

  deleteRole(roleId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${roleId}`);
  }
}
