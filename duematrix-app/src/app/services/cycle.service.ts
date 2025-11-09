import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { DataService } from './data.service';

@Injectable({
  providedIn: 'root'
})
export class CycleService {
  private selectedCycleSubject = new BehaviorSubject<string | null>(null);
  selectedCycle$ = this.selectedCycleSubject.asObservable();

  constructor(private dataService: DataService) {}

  setSelectedCycle(cycle: string | null) {
    console.log('[CycleService] setSelectedCycle called with:', cycle);
    this.selectedCycleSubject.next(cycle);
  }

  getSelectedCycle(): string | null {
    const current = this.selectedCycleSubject.getValue();
    console.log('[CycleService] getSelectedCycle returning:', current);
    return current;
  }

  loadCycles(): Observable<{ success: boolean; data: any[] }> {
    console.log('[CycleService] loadCycles called');
    return this.dataService.getCycles();
  }

  /**
   * Reset cycle selection (call on logout)
   */
  reset(): void {
    console.log('[CycleService] reset called - clearing selected cycle');
    this.selectedCycleSubject.next(null);
  }
}
