import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  User, 
  CreateUserRequest, 
  Role, 
  RoleMapping, 
  AssignRoleRequest,
  ApiResponse 
} from '../models/user.model';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserManagementService {
  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getHeaders(): HttpHeaders {
    const token = this.authService.getAccessToken();
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  /**
   * Get all users
   */
  getUsers(): Observable<ApiResponse<User[]>> {
    return this.http.get<ApiResponse<User[]>>(
      `${this.apiUrl}/auth/users`,
      { headers: this.getHeaders() }
    );
  }

  /**
   * Create a new user
   */
  createUser(userData: CreateUserRequest): Observable<ApiResponse<{ user: User; access_token: string; refresh_token: string }>> {
    return this.http.post<ApiResponse<{ user: User; access_token: string; refresh_token: string }>>(
      `${this.apiUrl}/auth/register`,
      userData,
      { headers: this.getHeaders() }
    );
  }

  /**
   * Get all roles
   */
  getRoles(): Observable<ApiResponse<Role[]>> {
    return this.http.get<ApiResponse<Role[]>>(
      `${this.apiUrl}/roles`,
      { headers: this.getHeaders() }
    );
  }

  /**
   * Get role mappings for a user
   */
  getUserRoleMappings(userId: number): Observable<ApiResponse<RoleMapping[]>> {
    return this.http.get<ApiResponse<RoleMapping[]>>(
      `${this.apiUrl}/role-mappings/user/${userId}`,
      { headers: this.getHeaders() }
    );
  }

  /**
   * Assign a role to a user
   */
  assignRole(data: AssignRoleRequest): Observable<ApiResponse<RoleMapping>> {
    return this.http.post<ApiResponse<RoleMapping>>(
      `${this.apiUrl}/role-mappings`,
      data,
      { headers: this.getHeaders() }
    );
  }

  /**
   * Revoke a role from a user
   */
  revokeRole(mappingId: number): Observable<ApiResponse<string>> {
    return this.http.delete<ApiResponse<string>>(
      `${this.apiUrl}/role-mappings/${mappingId}`,
      { headers: this.getHeaders() }
    );
  }

  /**
   * Update user status (activate/deactivate)
   */
  updateUserStatus(userId: number, isActive: boolean): Observable<ApiResponse<User>> {
    return this.http.patch<ApiResponse<User>>(
      `${this.apiUrl}/auth/users/${userId}/status`,
      { is_active: isActive },
      { headers: this.getHeaders() }
    );
  }

  /**
   * Change user password
   */
  changeUserPassword(userId: number, data: { new_password: string }): Observable<ApiResponse<string>> {
    return this.http.patch<ApiResponse<string>>(
      `${this.apiUrl}/auth/users/${userId}/password`,
      data,
      { headers: this.getHeaders() }
    );
  }
}
