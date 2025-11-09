import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  CustomerData, 
  CustomerDataResponse, 
  SingleCustomerDataResponse,
  FilterOptionsResponse 
} from '../models/data.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = 'http://localhost:5000/api/data';

  constructor(private http: HttpClient) {}

  /**
   * Get customer data with pagination and optional filters
   */
  getCustomerData(params?: {
    page?: number;
    per_page?: number;
    search?: string;
    status?: string;
    department?: string;
    city?: string;
  }): Observable<CustomerDataResponse> {
    let httpParams = new HttpParams();
    
    if (params) {
      if (params.page) httpParams = httpParams.set('page', params.page.toString());
      if (params.per_page) httpParams = httpParams.set('per_page', params.per_page.toString());
      if (params.search) httpParams = httpParams.set('search', params.search);
      if (params.status) httpParams = httpParams.set('status', params.status);
      if (params.department) httpParams = httpParams.set('department', params.department);
      if (params.city) httpParams = httpParams.set('city', params.city);
    }
    
    return this.http.get<CustomerDataResponse>(`${this.apiUrl}/customer-data`, { params: httpParams });
  }

  /**
   * Get a single customer data record by ID
   */
  getCustomerDataById(id: number): Observable<SingleCustomerDataResponse> {
    return this.http.get<SingleCustomerDataResponse>(`${this.apiUrl}/customer-data/${id}`);
  }

  /**
   * Create a new customer data record
   */
  createCustomerData(data: Partial<CustomerData>): Observable<SingleCustomerDataResponse> {
    return this.http.post<SingleCustomerDataResponse>(`${this.apiUrl}/customer-data`, data);
  }

  /**
   * Update an existing customer data record
   */
  updateCustomerData(id: number, data: Partial<CustomerData>): Observable<SingleCustomerDataResponse> {
    return this.http.put<SingleCustomerDataResponse>(`${this.apiUrl}/customer-data/${id}`, data);
  }

  /**
   * Delete a customer data record
   */
  deleteCustomerData(id: number): Observable<{ success: boolean; message: string }> {
    return this.http.delete<{ success: boolean; message: string }>(`${this.apiUrl}/customer-data/${id}`);
  }

  /**
   * Bulk create customer data records
   */
  bulkCreateCustomerData(dataList: Partial<CustomerData>[]): Observable<CustomerDataResponse> {
    return this.http.post<CustomerDataResponse>(`${this.apiUrl}/customer-data/bulk`, dataList);
  }

  /**
   * Get filter options for dropdown filters
   */
  getFilterOptions(): Observable<FilterOptionsResponse> {
    return this.http.get<FilterOptionsResponse>(`${this.apiUrl}/customer-data/filters`);
  }
}
