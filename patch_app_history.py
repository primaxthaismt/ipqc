import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Add 'history' to roleTabAccess
code = code.replace(
    "auditor: ['audit', 'map', 'capa'],",
    "auditor: ['audit', 'map', 'capa', 'history'],"
)
code = code.replace(
    "supervisor: ['audit', 'map', 'capa', 'analytics', 'ai'],",
    "supervisor: ['audit', 'map', 'capa', 'history', 'analytics', 'ai'],"
)
code = code.replace(
    "admin: ['audit', 'map', 'capa', 'analytics', 'users', 'qrgen', 'ai']",
    "admin: ['audit', 'map', 'capa', 'history', 'analytics', 'users', 'qrgen', 'ai']"
)

# Add loadAuditHistory on tab click if tab is history
setup_nav_pattern = r"""        if \(targetView\) targetView\.classList\.add\('active'\);
      \}\);
    \}\);"""
setup_nav_replacement = """        if (targetView) targetView.classList.add('active');
        
        if (targetTab === 'history') {
          loadAuditHistory();
        }
      });
    });"""
code = re.sub(setup_nav_pattern, setup_nav_replacement, code)


# Add loadAuditHistory function
new_function = """
// ==========================================================================
// AUDIT HISTORY & REPORT GENERATION
// ==========================================================================
async function loadAuditHistory() {
  const tbody = document.getElementById('history-table-body');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">Fetching audits...</td></tr>';
  
  let audits = [];
  try {
    const res = await apiFetch('/api/audits');
    if (res.ok) audits = await res.json();
  } catch (e) {
    console.warn("Could not fetch audits", e);
  }
  
  const fDate = document.getElementById('history-filter-date').value;
  const fLine = document.getElementById('history-filter-line').value;
  const fModel = document.getElementById('history-filter-model').value.trim().toLowerCase();
  const fWO = document.getElementById('history-filter-wo').value.trim().toLowerCase();
  
  if (fDate) {
    audits = audits.filter(a => (a.audit_time || a.created_at || '').startsWith(fDate));
  }
  if (fLine) {
    audits = audits.filter(a => a.line_name === fLine);
  }
  if (fModel) {
    audits = audits.filter(a => (a.model_no || '').toLowerCase().includes(fModel));
  }
  if (fWO) {
    audits = audits.filter(a => (a.work_order || '').toLowerCase().includes(fWO));
  }
  
  // Sort by date descending
  audits.sort((a, b) => new Date(b.audit_time || b.created_at || 0) - new Date(a.audit_time || a.created_at || 0));
  
  if (audits.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">No completed audits found matching the criteria.</td></tr>';
    return;
  }
  
  tbody.innerHTML = audits.map(a => {
    const isOK = a.overall_status === 'OK';
    const statusColor = isOK ? '#34d399' : '#ef4444';
    
    return `
      <tr style="border-bottom: 1px solid var(--border-color); background: rgba(15,23,42,0.3);">
        <td style="padding: 0.75rem;">${a.audit_time ? a.audit_time.replace('T', ' ').substring(0, 16) : 'N/A'}</td>
        <td style="padding: 0.75rem; font-family: monospace; color: var(--accent-cyan);">${a.id}</td>
        <td style="padding: 0.75rem; font-weight: bold;">${a.line_name || 'N/A'}<br><span style="font-size: 0.7rem; color: var(--text-muted); font-weight: normal;">${a.time_block || ''}</span></td>
        <td style="padding: 0.75rem;">${a.model_no || '-'}<br><span style="font-size: 0.75rem; color: #94a3b8;">${a.work_order || '-'}</span></td>
        <td style="padding: 0.75rem;">${a.station_code || 'Multiple'}<br><span style="font-weight: bold; color: ${statusColor}; font-size: 0.8rem;">${a.overall_status || 'OK'}</span></td>
        <td style="padding: 0.75rem;">${a.auditor || '-'}</td>
        <td style="padding: 0.75rem; text-align: right;">
          <button class="btn-primary" onclick="openEmailModal('audit', '${a.id}')" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;">
            📄 Line Report
          </button>
        </td>
      </tr>
    `;
  }).join('');
}
"""

code += new_function

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
