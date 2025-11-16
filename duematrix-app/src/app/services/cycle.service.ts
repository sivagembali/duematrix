import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, shareReplay, tap } from 'rxjs/operators';
import { DataService } from './data.service';

@Injectable({
  providedIn: 'root'
})
export class CycleService {
  private selectedCycleSubject = new BehaviorSubject<string | null>(null);
  selectedCycle$ = this.selectedCycleSubject.asObservable();

  constructor(private dataService: DataService) {}

  setSelectedCycle(cycle: string | null) {
    const current = this.selectedCycleSubject.getValue();
    // Only publish when the cycle actually changes to avoid duplicate downstream actions
    if (current === cycle) {
      console.log('[CycleService] setSelectedCycle called with same value, ignoring:', cycle);
      return;
    }
    console.log('[CycleService] setSelectedCycle called with:', cycle, '(previous:', current, ')');
    this.selectedCycleSubject.next(cycle);
  }

  getSelectedCycle(): string | null {
    const current = this.selectedCycleSubject.getValue();
    console.log('[CycleService] getSelectedCycle returning:', current);
    return current;
  }

  // Cached observable for cycles so multiple components don't trigger duplicate HTTP requests
  private cycles$?: Observable<{ success: boolean; data: any[] }>;

  loadCycles(): Observable<{ success: boolean; data: any[] }> {
    if (this.cycles$) {
      console.log('[CycleService] returning cached cycles observable');
      return this.cycles$;
    }

    console.log('[CycleService] loadCycles called - fetching from API');
    this.cycles$ = this.dataService.getCycles().pipe(
      // Keep the latest successful value for future subscribers
      shareReplay(1),
      catchError(err => {
        // On error, clear cache so retries are possible and rethrow
        console.error('[CycleService] error loading cycles', err);
        this.cycles$ = undefined;
        throw err;
      })
    );

    return this.cycles$;
  }

  /**
   * Reset cycle selection (call on logout)
   */
  reset(): void {
    console.log('[CycleService] reset called - clearing selected cycle');
    this.selectedCycleSubject.next(null);
  }
}
