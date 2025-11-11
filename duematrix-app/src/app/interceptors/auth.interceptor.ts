import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

// Interceptor: add Authorization header and handle expired-token/401 responses
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);

  // Get the auth token from localStorage
  const token = localStorage.getItem('access_token');
  
  // Clone the request and add the authorization header if token exists
  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  return next(req).pipe(
    catchError((err: any) => {
      // If token expired or unauthorized, clear local state and redirect to login
      const isTokenExpired = err?.status === 401 || err?.error?.msg === 'Token has expired' || (err?.error?.msg && typeof err.error.msg === 'string' && err.error.msg.toLowerCase().includes('token has expired'));
      if (isTokenExpired) {
        console.warn('[AuthInterceptor] Token expired or unauthorized response received. Clearing auth data and redirecting to login.');

        try {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('currentUser');
          localStorage.removeItem('columnHeaders');
          sessionStorage.clear();
        } catch (e) {
          console.warn('[AuthInterceptor] Error clearing storage', e);
        }

        // Safe navigation to login
        try {
          router.navigate(['/login']);
        } catch (e) {
          console.warn('[AuthInterceptor] Router navigation failed', e);
        }
      }

      return throwError(() => err);
    })
  );
};
