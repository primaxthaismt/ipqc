import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern_preview = r"""@router\.get\("/reports/audit/preview", response_class=HTMLResponse\)
def preview_audit_report\(audit_id: str\):
(.*?)
    return HTMLResponse\(content=html\)"""

new_preview = """@router.get("/reports/audit/preview", response_class=HTMLResponse)
def preview_audit_report(audit_id: str):
    import urllib.parse
    audits = supabase_db_query("audits", params=f"id=eq.{audit_id}&select=*")
    if not isinstance(audits, list) or not audits:
        return HTMLResponse(content="<div style='color:red; padding:20px;'>Audit Not Found</div>", status_code=404)
    audit = audits[0]
    
    line_name = audit.get("line_name")
    time_block = audit.get("time_block")
    audit_date = audit.get("audit_time", "")[:10] if audit.get("audit_time") else ""
    
    line_audits = supabase_db_query("audits", params=f"line_name=eq.{urllib.parse.quote(line_name)}&time_block=eq.{urllib.parse.quote(time_block)}&select=*")
    if not isinstance(line_audits, list): line_audits = [audit]
    
    # Filter by date
    if audit_date:
        line_audits = [a for a in line_audits if a.get("audit_time", "").startswith(audit_date)]
        
    if not line_audits:
        line_audits = [audit]
        
    audit_ids = [a["id"] for a in line_audits]
    
    # Fetch details for all these audits
    all_details = []
    for aid in audit_ids:
        details = supabase_db_query("audit_details", params=f"audit_id=eq.{aid}&select=*")
        if isinstance(details, list):
            all_details.extend(details)
            
    # Enrich with master questions
    master_items = get_master_data().get("all_items", [])
    for d in all_details:
        m = next((m for m in master_items if m.get("item_no") == d.get("item_no")), None)
        if m:
            d["question_en"] = m.get("en", "")
            d["category"] = m.get("process", "")
            
    # Group details by station for the report
    stations_data = {}
    for a in line_audits:
        stations_data[a["id"]] = {
            "station_code": a.get("station_code"),
            "station_name": a.get("station_name"),
            "auditor": a.get("auditor"),
            "audit_time": a.get("audit_time"),
            "details": []
        }
        
    for d in all_details:
        aid = d.get("audit_id")
        if aid in stations_data:
            stations_data[aid]["details"].append(d)
            
    total_items = len(all_details)
    passed = len([d for d in all_details if d.get("result") in ["O", "V"]])
    failed = len([d for d in all_details if d.get("result") == "X"])
    
    # Build HTML for each station
    stations_html = ""
    for aid, sdata in stations_data.items():
        st_details = sdata["details"]
        if not st_details: continue
        
        stations_html += f'''
        <div style="margin-top: 30px; border-left: 4px solid #38bdf8; padding-left: 15px; background: #1e293b; padding-top: 10px; padding-bottom: 10px; padding-right: 10px; border-radius: 0 8px 8px 0;">
            <h3 style="color: #38bdf8; margin-top: 0; margin-bottom: 5px;">Station: {sdata['station_code']} - {sdata['station_name']}</h3>
            <div style="font-size: 12px; color: #94a3b8; margin-bottom: 15px;">Auditor: {sdata['auditor']} | Time: {sdata['audit_time']}</div>
            <table>
              <thead>
                <tr> <th>Item #</th> <th>Result</th> <th>Question / Auditor Remarks</th> </tr>
              </thead>
              <tbody>
        '''
        
        for d in st_details:
            is_pass = d['result'] in ['O', 'V']
            is_fail = d['result'] == 'X'
            res_class = 'pass' if is_pass else ('fail' if is_fail else '')
            res_text = '✓ OK' if is_pass else ('❌ NG' if is_fail else '- NA')
            
            photo_html = f"<div style='margin-top:6px;'><img src='{d.get('photo_url')}' style='max-width:180px; max-height:140px; border-radius:4px; border:1px solid #334155;'/></div>" if d.get("photo_url") else ""
            
            stations_html += f'''
                <tr>
                    <td>#{d['item_no']}</td>
                    <td class="{res_class}">{res_text}</td>
                    <td>
                        <div style="color:#94a3b8; font-size:11px; margin-bottom:4px;">{d.get('question_en', '')}</div>
                        <div>{d.get('remark') or ('No defects reported' if is_pass else '')}</div>
                        {photo_html}
                    </td>
                </tr>
            '''
            
        stations_html += '''
              </tbody>
            </table>
        </div>
        '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; margin: 0; }}
        .header {{ border-bottom: 2px solid #38bdf8; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .badge {{ background: #0284c7; color: #fff; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; background: #1e293b; padding: 15px; border-radius: 8px; font-size: 13px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #334155; text-align: left; }}
        th {{ background: #0f172a; color: #94a3b8; }}
        .pass {{ color: #34d399; font-weight: bold; }}
        .fail {{ color: #ef4444; font-weight: bold; }}
      </style>
    </head>
    <body>
      <div class="header">
        <div>
          <h2 style="margin:0; color:#38bdf8;">📊 IPQC Layered Process Audit Execution Report (Line Level)</h2>
          <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Smart Digital Audit & Verification System</div>
        </div>
        <span class="badge">AUDIT COMPLETE</span>
      </div>

      <div class="grid">
        <div><b>Audit Group ID:</b> {audit.get('id')}</div>
        <div><b>Date/Time:</b> {audit_date} {time_block}</div>
        <div><b>Line Name:</b> {line_name}</div>
        <div><b>Work Order:</b> <span style="color:#38bdf8; font-weight:bold;">{audit.get('work_order', 'N/A')}</span></div>
        <div><b>Product Model:</b> {audit.get('model_no', 'N/A')}</div>
        <div><b>Stations Audited:</b> {len(stations_data)}</div>
      </div>

      <div style="background:#1e293b; padding:15px; border-radius:8px; display:flex; justify-content:space-around; text-align:center; font-weight:bold;">
        <div>Total Check Items<br><span style="font-size:20px; color:#38bdf8;">{total_items}</span></div>
        <div>Passed (OK)<br><span style="font-size:20px; color:#34d399;">{passed}</span></div>
        <div>Failed (NG)<br><span style="font-size:20px; color:#ef4444;">{failed}</span></div>
      </div>

      <h3 style="margin-top: 25px; margin-bottom: 5px;">Detailed Check Item Log by Station:</h3>
      {stations_html}
    </body>
    </html>
    '''
    return HTMLResponse(content=html)"""

code = re.sub(pattern_preview, new_preview, code, flags=re.DOTALL)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
