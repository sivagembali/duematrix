import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, tap, catchError, of } from 'rxjs';
import { LoginRequest, LoginResponse, User } from '../models/auth.model';
import { ColumnHeader } from './header.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api/auth';
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private headersSubject = new BehaviorSubject<ColumnHeader[]>([]);
  public headers$ = this.headersSubject.asObservable();

  constructor(
    private http: HttpClient
  ) {
    // Load user from localStorage on service initialization
    this.loadUserFromStorage();
  }

  /**
   * Login user with username or email and password
   */
  login(credentials: LoginRequest): Observable<LoginResponse> {
    console.log('[AuthService] Login attempt for user:', credentials.username);
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, credentials).pipe(
      tap((response) => {
        if (response.success) {
          console.log('[AuthService] Login successful, storing auth data');
          // Store tokens and user data
          this.storeAuthData(response.data);
        }
      })
    );
  }

  /**
   * Get current authenticated user profile
   */
  getCurrentUser(): Observable<any> {
    const token = this.getAccessToken();
    if (!token) {
      throw new Error('No access token found');
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.get(`${this.apiUrl}/me`, { headers }).pipe(
      tap((response: any) => {
        if (response.success) {
          this.currentUserSubject.next(response.data);
          localStorage.setItem('currentUser', JSON.stringify(response.data));
        }
      })
    );
  }

  /**
   * Logout user
   */
  logout(): Observable<any> {
    const token = this.getAccessToken();
    
    if (token) {
      const headers = new HttpHeaders({
        Authorization: `Bearer ${token}`
      });

      return this.http.post(`${this.apiUrl}/logout`, {}, { headers }).pipe(
        tap(() => {
          this.clearAuthData();
        }),
        // Even if backend fails, clear local data
        catchError((error) => {
          console.error('Backend logout failed, clearing local data anyway', error);
          this.clearAuthData();
          return of({ success: true, message: 'Logged out locally' });
        })
      );
    }

    // If no token, just clear local data
    this.clearAuthData();
    return of({ success: true, message: 'Already logged out' });
  }

  /**
   * Refresh access token
   */
  refreshToken(): Observable<any> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token found');
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${refreshToken}`
    });

    return this.http.post(`${this.apiUrl}/refresh`, {}, { headers }).pipe(
      tap((response: any) => {
        if (response.success) {
          localStorage.setItem('access_token', response.data.access_token);
        }
      })
    );
  }

  /**
   * Store authentication data in localStorage
   */
  private storeAuthData(data: { user: User; access_token: string; refresh_token: string }): void {
    console.log('[AuthService] Storing auth data for user:', data.user);
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('currentUser', JSON.stringify(data.user));
    this.currentUserSubject.next(data.user);
    console.log('[AuthService] Auth data stored, currentUserSubject updated');
  }

  /**
   * Clear all authentication data
   */
  private clearAuthData(): void {
    console.log('[AuthService] Clearing all auth data');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('columnHeaders');
    sessionStorage.clear();
    this.currentUserSubject.next(null);
    this.headersSubject.next([]);
    console.log('[AuthService] Auth data cleared, currentUserSubject set to null');
  }

  /**
   * Load user from localStorage
   */
  private loadUserFromStorage(): void {
    const userJson = localStorage.getItem('currentUser');
    if (userJson) {
      try {
        const user = JSON.parse(userJson);
        this.currentUserSubject.next(user);
      } catch (e) {
        console.error('Error parsing user from localStorage', e);
        this.clearAuthData();
      }
    }
    
    // Load headers from localStorage
    const headersJson = localStorage.getItem('columnHeaders');
    if (headersJson) {
      try {
        const headers = JSON.parse(headersJson);
        this.headersSubject.next(headers);
      } catch (e) {
        console.error('Error parsing headers from localStorage', e);
      }
    }
  }

  /**
   * Get access token from localStorage
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Get refresh token from localStorage
   */
  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  /**
   * Get current user value
   */
  getCurrentUserValue(): User | null {
    return this.currentUserSubject.value;
  }
  
  /**
   * Get current headers value
   */
  getHeadersValue(): ColumnHeader[] {
    return this.headersSubject.value;
  }
  
  /**
   * Set headers (used when loading headers from other components)
   */
  setHeaders(headers: ColumnHeader[]): void {
    this.headersSubject.next(headers);
    localStorage.setItem('columnHeaders', JSON.stringify(headers));
  }
}
