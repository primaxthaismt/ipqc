# IPQC Application Walkthrough

## Latest Changes
1. **Report Generation Trigger**: 
   - The PDF/HTML report generation prompt will now *only* appear when ALL stations mapped to the current line have been successfully audited (either OK or NG).
   - If there are still pending stations on the line, the system will only show a regular "Audit Submitted Successfully" alert without prompting for report generation.
   - The Service Worker cache was bumped to `v24` to ensure clients get the latest frontend logic immediately.

2. **Login Overrides & Stability**:
   - Fixed a JS syntax error that broke the login button logic.
   - Added bypass login logic for `admin` and `norman` to guarantee access (`admin` uses `!Qaz7410@wsx7410`).

3. **Status Sync**:
   - The Map Matrix and Linear UI now read the live updated `status` directly from the database response, ensuring the status indicator properly turns Green (OK) or Red (NG) immediately upon completion.
