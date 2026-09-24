with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = """  if (audits.length === 0) {
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
  }).join('');"""

replacement = """  if (audits.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">No completed audits found matching the criteria.</td></tr>';
    return;
  }
  
  // Group by Line, Time Block, and Date
  const lineReportsMap = {};
  audits.forEach(a => {
    const date = a.audit_time ? a.audit_time.substring(0, 10) : '';
    const key = `${a.line_name}_${date}_${a.time_block}`;
    
    if (!lineReportsMap[key]) {
      lineReportsMap[key] = {
        latest_audit: a, 
        report_id: 'RPT-' + a.id.replace('AUD-', ''),
        line_name: a.line_name,
        date: date,
        time_block: a.time_block,
        latest_time: a.audit_time,
        model_no: a.model_no,
        work_order: a.work_order,
        overall_status: 'OK',
        stations_audited: 0,
        auditors: new Set()
      };
    }
    
    lineReportsMap[key].stations_audited += 1;
    if (a.auditor) lineReportsMap[key].auditors.add(a.auditor.split(' ')[0]); 
    if (a.overall_status !== 'OK') lineReportsMap[key].overall_status = 'NG';
    
    if (new Date(a.audit_time) > new Date(lineReportsMap[key].latest_time)) {
      lineReportsMap[key].latest_time = a.audit_time;
      lineReportsMap[key].latest_audit = a;
      lineReportsMap[key].report_id = 'RPT-' + a.id.replace('AUD-', '');
    }
  });

  const lineReports = Object.values(lineReportsMap);
  lineReports.sort((a, b) => new Date(b.latest_time) - new Date(a.latest_time));

  tbody.innerHTML = lineReports.map(r => {
    const isOK = r.overall_status === 'OK';
    const statusColor = isOK ? '#34d399' : '#ef4444';
    
    return `
      <tr style="border-bottom: 1px solid var(--border-color); background: rgba(15,23,42,0.3);">
        <td style="padding: 0.75rem;">${r.latest_time ? r.latest_time.replace('T', ' ').substring(0, 16) : 'N/A'}</td>
        <td style="padding: 0.75rem; font-family: monospace; color: #facc15; font-weight: bold;">${r.report_id}</td>
        <td style="padding: 0.75rem; font-weight: bold;">${r.line_name || 'N/A'}<br><span style="font-size: 0.7rem; color: var(--text-muted); font-weight: normal;">${r.time_block || ''}</span></td>
        <td style="padding: 0.75rem;">${r.model_no || '-'}<br><span style="font-size: 0.75rem; color: #94a3b8;">${r.work_order || '-'}</span></td>
        <td style="padding: 0.75rem;">${r.stations_audited} Nodes Audited<br><span style="font-weight: bold; color: ${statusColor}; font-size: 0.8rem;">${r.overall_status}</span></td>
        <td style="padding: 0.75rem;">${Array.from(r.auditors).join(', ') || '-'}</td>
        <td style="padding: 0.75rem; text-align: right;">
          <button class="btn-primary" onclick="openEmailModal('audit', '${r.latest_audit.id}')" style="padding: 0.35rem 0.75rem; font-size: 0.75rem; background: #0284c7;">
            📄 View Line Report
          </button>
        </td>
      </tr>
    `;
  }).join('');"""

code = code.replace(pattern, replacement)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
