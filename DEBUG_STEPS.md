# Debug Instructions

## Step 1: Refresh Browser
Press `Ctrl + F5` to hard refresh your browser

## Step 2: Open Developer Console
Press `F12` and go to the Console tab

## Step 3: Look for These Logs
You should see:
- "API Response received:" - Shows what data is coming through
- "Final data:" - Shows the processed data counts
- "Backend API error:" - If there are connection issues

## Step 4: What Should Happen Now
With the sample data fallback enabled, you should see:
- **Statistics**: 5 total, 1 paid, 2 pending, 1 overdue
- **Table**: 5 sample bills displayed
- **Functionality**: All filters, search, sorting working

## Step 5: If Still No Data
If you still see "No bills found", check console for errors and let me know what you see.

## Expected Console Output
```
Backend API error: [error details]
Using sample data fallback
API Response received: {bills: Array(5), header_config: Array(9), ...}
Final data: {bills: 5, visibleColumns: 9, totalCount: 5}
```

## Quick Test
You can also test by typing this in the console:
```javascript
// Check if bills array exists
console.log('Bills in component:', angular.getTestability(document.body).findBindings(document.body, 'bills'));
```