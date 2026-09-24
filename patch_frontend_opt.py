import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"""// ==========================================================================
// AUDIT HISTORY & REPORT GENERATION
// ==========================================================================
async function loadAuditHistory\(\) \{
  const tbody = document\.getElementById\('history-table-body'\);
  if \(!tbody\) return;
  tbody\.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:2rem; color:var\(--text-muted\);">Fetching audits\.\.\.</td></tr>';
  
  let audits = \[\];
  try \{
    const res = await apiFetch\('/api/audits', \{
      headers: \{ 'Authorization': `Bearer \$\{authToken\}` \}
    \}\);
    if \(res\.ok\) audits = await res\.json\(\);
  \} catch \(e\) \{
    console\.warn\("Could not fetch audits", e\);
  \}
  
  const fDate = document\.getElementById\('history-filter-date'\)\.value;
  const fLine = document\.getElementById\('history-filter-line'\)\.value;
  const fModel = document\.getElementById\('history-filter-model'\)\.value\.trim\(\)\.toLowerCase\(\);
  const fWO = document\.getElementById\('history-filter-wo'\)\.value\.trim\(\)\.toLowerCase\(\);
  
  if \(fDate\) \{
    audits = audits\.filter\(a => \(a\.audit_time \|\| a\.created_at \|\| ''\)\.startsWith\(fDate\)\);
  \}
  if \(fLine\) \{
    audits = audits\.filter\(a => a\.line_name === fLine\);
  \}
  if \(fModel\) \{
    audits = audits\.filter\(a => \(a\.model_no \|\| ''\)\.toLowerCase\(\)\.includes\(fModel\)\);
  \}
  if \(fWO\) \{
    audits = audits\.filter\(a => \(a\.work_order \|\| ''\)\.toLowerCase\(\)\.includes\(fWO\)\);
  \}"""

replacement = """// ==========================================================================
// AUDIT HISTORY & REPORT GENERATION
// ==========================================================================
async function loadAuditHistory() {
  const tbody = document.getElementById('history-table-body');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">Fetching audits...</td></tr>';
  
  const fDate = document.getElementById('history-filter-date').value;
  const fLine = document.getElementById('history-filter-line').value;
  const fModel = document.getElementById('history-filter-model').value.trim();
  const fWO = document.getElementById('history-filter-wo').value.trim();
  
  const params = new URLSearchParams();
  if (fDate) params.append('date', fDate);
  if (fLine) params.append('line_name', fLine);
  if (fModel) params.append('model_no', fModel);
  if (fWO) params.append('work_order', fWO);
  
  let audits = [];
  try {
    const res = await apiFetch(`/api/audits?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    if (res.ok) audits = await res.json();
  } catch (e) {
    console.warn("Could not fetch audits", e);
  }"""

code = re.sub(pattern, replacement, code)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
