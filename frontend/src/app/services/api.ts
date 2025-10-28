import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

export interface CreditBill {
  id: number;
  bill_no: string;
  amount: number;
  due_date: string;
  payment_status: 'PAID' | 'PENDING' | 'OVERDUE';
  mobile: string;
  bank_name: string;
}

@Injectable({
  providedIn: 'root'
})
export class Api {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:5000/api';

  getBills(): Observable<CreditBill[]> {
    console.log('🔄 Fetching bills from API...');
    
    return this.http.get<CreditBill[]>(`${this.baseUrl}/bills`).pipe(
      tap(response => console.log('✅ API Response:', response)),
      catchError((error: HttpErrorResponse) => {
        console.warn('⚠️ API call failed, using sample data:', error.message);
        return of(this.getSampleData());
      })
    );
  }

  private getSampleData(): CreditBill[] {
    return [
      {
        id: 1,
        bill_no: 'CC001',
        amount: 15000,
        due_date: '2024-01-15',
        payment_status: 'PENDING',
        mobile: '9876543210',
        bank_name: 'HDFC'
      },
      {
        id: 2,
        bill_no: 'CC002',
        amount: 25000,
        due_date: '2024-01-10',
        payment_status: 'OVERDUE',
        mobile: '8765432109',
        bank_name: 'ICICI'
      },
      {
        id: 3,
        bill_no: 'CC003',
        amount: 8000,
        due_date: '2024-01-20',
        payment_status: 'PAID',
        mobile: '7654321098',
        bank_name: 'SBI'
      },
      {
        id: 4,
        bill_no: 'CC004',
        amount: 12000,
        due_date: '2024-01-25',
        payment_status: 'PENDING',
        mobile: '6543210987',
        bank_name: 'AXIS'
      },
      {
        id: 5,
        bill_no: 'CC005',
        amount: 30000,
        due_date: '2024-01-05',
        payment_status: 'OVERDUE',
        mobile: '5432109876',
        bank_name: 'HDFC'
      }
    ];
  }
}
