import re

with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

# Pattern for preview_audit_report
pattern_preview = r'# AUDIT REPORT LIVE PREVIEW ENDPOINT.*?return HTMLResponse\(content=html\)'

replacement_preview = '''# AUDIT REPORT LIVE PREVIEW ENDPOINT
@router.get("/reports/audit/preview", response_class=HTMLResponse)
def preview_audit_report(audit_id: str):
    audits = supabase_db_query("audits", params=f"id=eq.{audit_id}&select=*")
    if not isinstance(audits, list) or not audits:
        return HTMLResponse(content="<div style='color:red; padding:20px;'>Audit Not Found</div>", status_code=404)
    audit = audits[0]
    
    details = supabase_db_query("audit_details", params=f"audit_id=eq.{audit_id}&select=*")
    if not isinstance(details, list): details = []
    
    total_items = len(details)
    passed = len([d for d in details if d.get("result") == "O" or d.get("result") == "V"])
    failed = len([d for d in details if d.get("result") == "X"])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; margin: 0; }}
        .header {{ border-bottom: 2px solid #38bdf8; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .badge {{ background: #0284c7; color: #fff; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; background: #1e293b; padding: 15px; border-radius: 8px; font-size: 13px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #334155; text-align: left; }}
        th {{ background: #1e293b; color: #94a3b8; }}
        .pass {{ color: #34d399; font-weight: bold; }}
        .fail {{ color: #ef4444; font-weight: bold; }}
      </style>
    </head>
    <body>
      <div class="header">
        <div>
          <h2 style="margin:0; color:#38bdf8;">📊 IPQC Layered Process Audit Execution Report</h2>
          <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Smart Digital Audit & Verification System</div>
        </div>
        <span class="badge">AUDIT COMPLETE</span>
      </div>

      <div class="grid">
        <div><b>Audit ID:</b> {audit.get('id')}</div>
        <div><b>Date/Time:</b> {audit.get('audit_time')}</div>
        <div><b>Station Code:</b> {audit.get('station_code')}</div>
        <div><b>Station Name:</b> {audit.get('station_name')}</div>
        <div><b>Line Name:</b> {audit.get('line_name')}</div>
        <div><b>Work Order:</b> <span style="color:#38bdf8; font-weight:bold;">{audit.get('work_order', 'N/A')}</span></div>
        <div><b>Product Model:</b> {audit.get('model_no', 'N/A')}</div>
        <div><b>Auditor:</b> {audit.get('auditor')}</div>
      </div>

      <div style="background:#1e293b; padding:15px; border-radius:8px; display:flex; justify-content:space-around; text-align:center; font-weight:bold;">
        <div>Check Items<br><span style="font-size:20px; color:#38bdf8;">{total_items}</span></div>
        <div>Passed (OK)<br><span style="font-size:20px; color:#34d399;">{passed}</span></div>
        <div>Failed (NG)<br><span style="font-size:20px; color:#ef4444;">{failed}</span></div>
      </div>

      <h3>Detailed Check Item Log:</h3>
      <table>
        <thead>
          <tr> <th>Item #</th> <th>Result</th> <th>Question / Auditor Remarks</th> </tr>
        </thead>
        <tbody>
          {"".join([f"<tr><td>#{d['item_no']}</td><td class='{'pass' if d['result'] in ['O', 'V'] else ('fail' if d['result']=='X' else '')}'>{'✔️ OK' if d['result'] in ['O', 'V'] else ('❌ NG' if d['result']=='X' else '- NA')}</td><td><div style='color:#94a3b8; font-size:11px; margin-bottom:4px;'>{d.get('question_en', '')}</div><div>{d.get('remark') or ('No defects reported' if d['result'] in ['O', 'V'] else '')}</div>" + (f"<div style='margin-top:6px;'><img src='{d.get('photo_url')}' style='max-width:180px; max-height:140px; border-radius:4px; border:1px solid #334155;'/></div>" if d.get("photo_url") else "") + "</td></tr>" for d in details])}
        </tbody>
      </table>
    </body>
    </html>
    """
    return HTMLResponse(content=html)'''

code = re.sub(pattern_preview, replacement_preview, code, flags=re.DOTALL)

# Pattern for send_audit_report_email
pattern_email = r'# STEP 6: EMAIL AUDIT REPORT DISPATCH.*?return {"status": "SUCCESS"}'

replacement_email = '''# STEP 6: EMAIL AUDIT REPORT DISPATCH
@router.post("/reports/audit/email")
def send_audit_report_email(data: EmailAuditReportModel):
    audits = supabase_db_query("audits", params=f"id=eq.{data.audit_id}&select=*")
    if not isinstance(audits, list) or not audits:
        raise HTTPException(status_code=404, detail="Audit not found")
    audit = audits[0]

    report_html = preview_audit_report(data.audit_id).body.decode("utf-8")
    report_title = f"IPQC Audit Execution Summary Report - {audit.get('station_code')}"
    attachment_name = f"Audit_Report_{data.audit_id}.html"

    import os
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    host = os.environ.get("SMTP_HOST")
    if host:
        try:
            port = int(os.environ.get("SMTP_PORT", 587))
            user = os.environ.get("SMTP_USER")
            password = os.environ.get("SMTP_PASS")
            
            msg = MIMEMultipart()
            msg["Subject"] = report_title
            msg["From"] = user
            msg["To"] = data.recipient_email
            
            body = f"Please find attached the IPQC Audit Execution Report for {audit.get('station_code')} (ID: {data.audit_id}).\\n\\nNotes: {data.notes}"
            msg.attach(MIMEText(body, "plain"))
            
            html_part = MIMEApplication(report_html.encode("utf-8"))
            html_part.add_header("Content-Disposition", "attachment", filename=attachment_name)
            msg.attach(html_part)
            
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("SMTP Error:", e)
            
    return {"status": "SUCCESS"}'''

code = re.sub(pattern_email, replacement_email, code, flags=re.DOTALL)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Patched api/index.py for reports')
