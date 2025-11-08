import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ColumnHeader {
  id: number;
  col_header: string;
  col_label: string;
  is_editable: boolean;
  is_multi_select: boolean;
  col_width: number;
  display: boolean;
  default_display: boolean;
  is_frozen: boolean;
  display_order: number;
  role_id: number | null;
  created_at: string;
  updated_at: string;
  created_by: string;
  updated_by: string;
}

export interface HeaderResponse {
  success: boolean;
  data: ColumnHeader[];
  count: number;
  user?: {
    id: number;
    username: string;
    role_id: number | null;
  };
  role?: {
    id: number;
    name: string;
    description: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class HeaderService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:5000/api';

  /**
   * Get all column headers
   */
  getAllHeaders(): Observable<HeaderResponse> {
    return this.http.get<HeaderResponse>(`${this.apiUrl}/headers`);
  }

  /**
   * Get column headers for authenticated user's dashboard
   * Returns role-specific headers + generic headers
   */
  getDashboardHeaders(): Observable<HeaderResponse> {
    return this.http.get<HeaderResponse>(`${this.apiUrl}/headers/dashboard`);
  }

  /**
   * Get only default display headers
   */
  getDefaultHeaders(): Observable<HeaderResponse> {
    return this.http.get<HeaderResponse>(`${this.apiUrl}/headers/default`);
  }

  /**
   * Get headers for a specific role (admin function)
   */
  getHeadersByRole(roleId: number): Observable<HeaderResponse> {
    return this.http.get<HeaderResponse>(`${this.apiUrl}/headers/role/${roleId}`);
  }

  /**
   * Get a specific header by ID
   */
  getHeaderById(headerId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/headers/${headerId}`);
  }

  /**
   * Create a new column header
   */
  createHeader(headerData: Partial<ColumnHeader>): Observable<any> {
    return this.http.post(`${this.apiUrl}/headers`, headerData);
  }

  /**
   * Update an existing column header
   */
  updateHeader(headerId: number, headerData: Partial<ColumnHeader>): Observable<any> {
    return this.http.put(`${this.apiUrl}/headers/${headerId}`, headerData);
  }

  /**
   * Delete a column header
   */
  deleteHeader(headerId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/headers/${headerId}`);
  }

  /**
   * Bulk create multiple headers
   */
  bulkCreateHeaders(headers: Partial<ColumnHeader>[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/headers/bulk`, headers);
  }
}
