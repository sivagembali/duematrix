# Debug Instructions for User Switching Issue

## Changes Made

I've added comprehensive logging throughout the application to help diagnose the user-switching issue. Here's what was changed:

### 1. Dashboard Component (`dashboard.ts`)
- Added `isInitialized` flag to track component lifecycle
- Added `userSubscription` to properly track user changes
- Added detailed console logging for:
  - Component initialization
  - User changes
  - Data loading
  - Navigation events
  - Logout process

### 2. CycleService (`cycle.service.ts`)
- Added logging to track:
  - When cycles are loaded
  - When selected cycle changes
  - When reset is called

### 3. AuthService (`auth.service.ts`)
- Added logging to track:
  - Login attempts
  - Auth data storage
  - Auth data clearing (logout)
  - User subject updates

### 4. UserTable Component (`user-table.ts`)
- Added logging to track cycle subscription changes

## How to Test

### Step 1: Start Backend
```powershell
cd C:\Users\ssiva\Dev\duematrix\backend
python app.py
```

### Step 2: Start Frontend (in a new terminal)
```powershell
cd C:\Users\ssiva\Dev\duematrix\duematrix-app
npm start
```

### Step 3: Open Browser Console
1. Open your browser (Chrome/Edge recommended)
2. Press F12 to open Developer Tools
3. Go to the Console tab
4. Clear any existing logs

### Step 4: Test User Switching
Follow these steps exactly and watch the console output:

#### Test Sequence 1: Admin to Telecaller
1. **Login as Admin**
   - Username: `admin` (or your admin username)
   - Password: your admin password
   - Watch console logs - look for:
     - `[AuthService] Login attempt`
     - `[AuthService] Login successful`
     - `[AuthService] Storing auth data`
     - `[Dashboard] ngOnInit called`
     - `[Dashboard] loadDashboardData called`
     - `[CycleService] loadCycles called`
     - `[Dashboard] Cycles loaded`
     - `[Dashboard] Auto-selecting first cycle`
     - `[CycleService] setSelectedCycle called`
     - `[UserTable] Cycle changed`
     - `[UserTable] Loading data for cycle`

2. **Verify Dashboard Loads**
   - Check that cycle dropdown shows cycles
   - Check that table shows data
   - Note which cycle is selected

3. **Logout**
   - Click Logout button
   - Watch console logs - look for:
     - `[Dashboard] Logout initiated`
     - `[Dashboard] Logout successful`
     - `[CycleService] reset called`
     - `[AuthService] Clearing all auth data`
     - `[Dashboard] Navigating to login`

4. **Login as Telecaller** (WITHOUT hard refresh)
   - Username: your telecaller username
   - Password: your telecaller password
   - Watch console logs carefully - look for:
     - `[AuthService] Login attempt`
     - `[AuthService] Storing auth data`
     - `[Dashboard] User changed` (should show new user)
     - `[Dashboard] Different user detected, reloading data`
     - `[Dashboard] loadDashboardData called`
     - `[CycleService] loadCycles called`
     - `[Dashboard] Cycles loaded`

5. **Verify Dashboard Loads**
   - **CHECK**: Does cycle dropdown show cycles?
   - **CHECK**: Does table show data?
   - **CHECK**: Is a cycle auto-selected?

#### Test Sequence 2: Telecaller to Admin
Repeat the same process in reverse:
1. Login as Telecaller
2. Verify dashboard loads
3. Logout
4. Login as Admin (without refresh)
5. Verify dashboard loads

### Step 5: Analyze Console Logs

If the dropdown is still blank, look for these issues in the console:

#### Issue 1: Cycles not loading
Look for:
- `[CycleService] loadCycles called` - is this present?
- `[Dashboard] Cycles loaded` - is this present?
- Any error messages about cycles?

If cycles are not loading, check:
- Network tab - is `/api/data/cycles/public` being called?
- Is it returning data?

#### Issue 2: Cycle not being set
Look for:
- `[Dashboard] Auto-selecting first cycle` - is this present?
- `[CycleService] setSelectedCycle called` - is this present with a cycle name?
- `[UserTable] Cycle changed` - is this present?

If cycle is being set but not showing:
- Check if `this.selectedCycle` is being set in dashboard
- Check the dropdown binding in the template

#### Issue 3: Navigation not triggering reload
Look for:
- `[Dashboard] Navigation event` - is this present after login?
- `[Dashboard] Navigated to dashboard, reloading data` - is this present?

#### Issue 4: User change not detected
Look for:
- `[Dashboard] User changed` - is this present?
- `[Dashboard] Different user detected` - is this present?
- `[AuthService] Auth data stored` - is this present?

## Expected Console Output (Successful Flow)

### On Login:
```
[AuthService] Login attempt for user: admin
[AuthService] Login successful, storing auth data
[AuthService] Storing auth data for user: {id: 1, username: 'admin', ...}
[AuthService] Auth data stored, currentUserSubject updated
[Dashboard] User changed: {id: 1, username: 'admin', ...}
[Dashboard] Different user detected, reloading data
[Dashboard] loadDashboardData called
[CycleService] loadCycles called
[Dashboard] Cycles loaded, raw response: {...}
[Dashboard] Processed cycles: [{cycle_name: '2025-Q1', ...}, ...]
[Dashboard] Auto-selecting first cycle: 2025-Q1
[Dashboard] Publishing cycle to service: 2025-Q1
[CycleService] setSelectedCycle called with: 2025-Q1
[UserTable] Cycle changed: 2025-Q1
[UserTable] Loading data for cycle: 2025-Q1
```

### On Logout:
```
[Dashboard] Logout initiated
[AuthService] Clearing all auth data
[AuthService] Auth data cleared, currentUserSubject set to null
[Dashboard] Logout successful
[CycleService] reset called - clearing selected cycle
[Dashboard] Navigating to login
[UserTable] Cycle changed: null
[UserTable] No cycle selected, clearing dataset
```

## Common Issues and Solutions

### Issue: "No cycles available" in console
**Solution**: Check backend - ensure cycles are seeded:
```powershell
cd C:\Users\ssiva\Dev\duematrix\backend
python seed_cycles.py
```

### Issue: Network error when loading cycles
**Solution**: 
1. Verify backend is running on port 5000
2. Check CORS configuration
3. Check auth interceptor isn't blocking the public endpoint

### Issue: Component ngOnInit not called
**Solution**: This is expected - Angular reuses components. The user subscription should handle this.

### Issue: User change detected but data not loading
**Solution**: Check if `isInitialized` flag is true and user comparison is working.

## What to Report Back

Please provide:
1. Complete console log output from login through to dashboard display
2. Screenshots of:
   - Empty dropdown (if still happening)
   - Network tab showing cycle API call
   - Console errors (if any)
3. Which user roles you tested (admin, telecaller, etc.)
4. Whether the issue happens on first login or only when switching

This will help identify exactly where the flow is breaking.
