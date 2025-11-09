# User Switching Issue - Investigation & Fix Summary

## Problem Description
When switching between different user accounts (e.g., admin → telecaller or vice versa) without doing a hard browser refresh, the dashboard displayed:
- Empty cycle dropdown
- Blank data table

Hard refresh would fix it, indicating a client-side state management issue.

## Root Cause Analysis

### Multiple Issues Identified:

1. **Component Reuse**: Angular Router reuses the DashboardComponent instance when navigating login → dashboard → logout → login → dashboard. This means `ngOnInit` is only called once, not on every navigation.

2. **BehaviorSubject Immediate Emission**: The `currentUser$` BehaviorSubject emits its current value immediately upon subscription, making it difficult to distinguish between:
   - Initial load (user already in localStorage)
   - New login (user changed)

3. **Timing Issues**: The sequence of events during login:
   - User logs in → AuthService updates currentUserSubject
   - Dashboard subscribes to currentUser$ → receives current value
   - But data might not reload if subscription logic isn't careful

4. **State Persistence**: Previous user's cycle selection persisted in CycleService until reset was called.

## Solutions Implemented

### 1. Enhanced Dashboard Component Lifecycle Management

**File**: `duematrix-app/src/app/components/dashboard/dashboard.ts`

**Changes**:
- Added `isInitialized` flag to track first-time setup vs. subsequent loads
- Added `userSubscription` for proper subscription management
- Modified `ngOnInit` logic:
  ```typescript
  // Load initial data immediately
  this.loadDashboardData();
  this.isInitialized = true;
  
  // Subscribe to user changes
  this.userSubscription = this.authService.currentUser$.subscribe(user => {
    // Only reload if user actually changed (not initial subscription)
    if (this.isInitialized && user && user !== this.currentUser) {
      this.loadDashboardData();
    }
    this.currentUser = user;
  });
  ```
- This ensures:
  - Data loads on first visit
  - Data reloads when a different user logs in
  - Avoids double-loading on initial subscription

### 2. Comprehensive Diagnostic Logging

**Files Modified**:
- `dashboard.ts`
- `cycle.service.ts`
- `auth.service.ts`
- `user-table.ts`

**Logging Added**:
- `[Dashboard]` prefix: Component lifecycle, user changes, data loading, navigation
- `[CycleService]` prefix: Cycle loading, selection changes, reset
- `[AuthService]` prefix: Login, logout, auth data storage/clearing
- `[UserTable]` prefix: Cycle subscription changes, data loading

**Purpose**: Enable step-by-step debugging of the entire user authentication and data loading flow.

### 3. Navigation Event Handling

**Already Implemented** (kept in place):
- Router navigation subscription to reload data when navigating to `/dashboard`
- Handles cases where user navigates away and back to dashboard

### 4. Proper Subscription Cleanup

**Enhanced**:
```typescript
ngOnDestroy(): void {
  if (this.routerSubscription) {
    this.routerSubscription.unsubscribe();
  }
  if (this.userSubscription) {
    this.userSubscription.unsubscribe();
  }
  this.isInitialized = false;
}
```

## Testing Instructions

See `DEBUG_INSTRUCTIONS.md` for detailed testing steps.

### Quick Test:
1. Login as admin → verify dropdown and table load
2. Logout
3. Login as telecaller (no hard refresh) → verify dropdown and table load
4. Check console for log sequence
5. Repeat in reverse (telecaller → admin)

### Expected Behavior:
- Cycles dropdown populates immediately for all roles
- Table loads data based on selected cycle
- No blank screens when switching users
- Console shows complete log sequence without errors

## Key Code Sections

### Dashboard ngOnInit (dashboard.ts:36-62)
```typescript
ngOnInit(): void {
  console.log('[Dashboard] ngOnInit called, isInitialized:', this.isInitialized);
  this.currentUser = this.authService.getCurrentUserValue();
  
  // Load initial data
  this.loadDashboardData();
  this.isInitialized = true;
  
  // Subscribe to user changes
  this.userSubscription = this.authService.currentUser$.subscribe(user => {
    // Only reload if user actually changed
    if (this.isInitialized && user && user !== this.currentUser) {
      console.log('[Dashboard] Different user detected, reloading data');
      this.currentUser = user;
      this.loadDashboardData();
    } else {
      this.currentUser = user;
    }
  });
  
  // Navigation event subscription (existing)
  // ...
}
```

### CycleService reset() (cycle.service.ts:26-30)
```typescript
reset(): void {
  console.log('[CycleService] reset called - clearing selected cycle');
  this.selectedCycleSubject.next(null);
}
```

### AuthService storeAuthData (auth.service.ts:117-125)
```typescript
private storeAuthData(data: { user: User; access_token: string; refresh_token: string }): void {
  console.log('[AuthService] Storing auth data for user:', data.user);
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  localStorage.setItem('currentUser', JSON.stringify(data.user));
  this.currentUserSubject.next(data.user);
  console.log('[AuthService] Auth data stored, currentUserSubject updated');
}
```

## What Logs to Look For

### Successful Flow:
```
[AuthService] Login attempt for user: telecaller
[AuthService] Storing auth data for user: {...}
[Dashboard] User changed: {...}
[Dashboard] Different user detected, reloading data
[Dashboard] loadDashboardData called
[CycleService] loadCycles called
[Dashboard] Cycles loaded
[Dashboard] Auto-selecting first cycle: 2025-Q1
[CycleService] setSelectedCycle called with: 2025-Q1
[UserTable] Cycle changed: 2025-Q1
[UserTable] Loading data for cycle: 2025-Q1
```

### If Still Broken, Look For:
- Missing "[Dashboard] Different user detected" → User change not triggering reload
- Missing "[CycleService] loadCycles called" → Cycles not being fetched
- Missing "[Dashboard] Cycles loaded" → API call failing or not returning data
- Missing "[UserTable] Cycle changed" → Cycle service publication not working

## Next Steps

1. **Run the application** with these changes
2. **Follow test sequence** in DEBUG_INSTRUCTIONS.md
3. **Collect console logs** from a full user-switching scenario
4. **Report findings**:
   - Does it work now?
   - If not, which log messages are missing?
   - Any error messages?

## Files Modified

1. `duematrix-app/src/app/components/dashboard/dashboard.ts`
   - Enhanced lifecycle management
   - Added comprehensive logging
   - Improved user change detection

2. `duematrix-app/src/app/services/cycle.service.ts`
   - Added logging to all methods

3. `duematrix-app/src/app/services/auth.service.ts`
   - Added logging to login, storeAuthData, clearAuthData

4. `duematrix-app/src/app/components/user-table/user-table.ts`
   - Added logging to cycle subscription

5. `DEBUG_INSTRUCTIONS.md` (NEW)
   - Comprehensive testing guide

6. `USER_SWITCHING_FIX_SUMMARY.md` (THIS FILE)
   - Documentation of changes and analysis
