import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern_email = r"""@router\.post\("/reports/audit/email"\)
def send_audit_report_email\(data: EmailAuditReportModel\):
(.*?)
        "message": f"Audit Report dispatched to \{data\.recipient_email\} via SMTP!" if success else f"Audit Report queued for \{data\.recipient_email\}\. \(SMTP Note: \{smtp_msg\}\)"
    \}"""

new_email = """@router.post("/reports/audit/email")
def send_audit_report_email(data: EmailAuditReportModel):
    # Fetch from Supabase
    audits = supabase_db_query("audits", params=f"id=eq.{data.audit_id}&select=*")
    if isinstance(audits, list) and len(audits) > 0:
        audit = audits[0]
    else:
        audit = {
            "audit_id": data.audit_id,
            "line_name": "Unknown Line"
        }

    report_html = preview_audit_report(data.audit_id).body.decode("utf-8")
    report_title = f"IPQC Line Audit Execution Report - {audit.get('line_name', 'Line')}"
    attachment_name = f"Line_Audit_Report_{data.audit_id}.html"

    notes_html = f"<div style='background:#1e293b; padding:12px; border-left:4px solid #38bdf8; margin-bottom:15px; font-family:sans-serif; color:#f8fafc;'><b>Auditor Remarks & Context:</b> {data.notes}</div>" if data.notes else ""
    full_html = f"<!DOCTYPE html><html><body>{notes_html}{report_html}</body></html>"

    success, smtp_msg = send_smtp_email(
        recipient_email=data.recipient_email,
        subject=report_title,
        html_body=full_html,
        attachment_name=attachment_name,
        attachment_content=report_html
    )

    return {
        "status": "SUCCESS" if success else "WARNING",
        "real_email_sent": success,
        "recipient": data.recipient_email,
        "subject": report_title,
        "attachment_name": attachment_name,
        "smtp_details": smtp_msg,
        "message": f"Audit Report dispatched to {data.recipient_email} via SMTP!" if success else f"Audit Report queued for {data.recipient_email}. (SMTP Note: {smtp_msg})"
    }"""

code = re.sub(pattern_email, new_email, code, flags=re.DOTALL)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
