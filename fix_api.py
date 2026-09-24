import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix get_stations time_block encoding
code = code.replace(
    'valid_audits = supabase_db_query("audits", params=f"time_block=eq.{time_block}&select=*")',
    '''import urllib.parse
        tb_enc = urllib.parse.quote(time_block)
        valid_audits = supabase_db_query("audits", params=f"time_block=eq.{tb_enc}&select=*")'''
)

# 2. Fix submit_audit
submit_pattern = r'def submit_audit\(data: AuditSubmitModel\):.*?return \{\n.*?"message": f"Audit submitted with \{len\(new_capas\)\} CAPAs logged\."\n    \}'

new_submit_logic = '''def submit_audit(data: AuditSubmitModel):
    audit_record = data.dict()
    
    # Map fields for Supabase
    s_record = {
        "id": audit_record.get("audit_id"),
        "station_code": audit_record.get("station_code"),
        "station_name": audit_record.get("station_name"),
        "line_name": audit_record.get("line_name"),
        "auditor": audit_record.get("auditor"),
        "shift": audit_record.get("shift"),
        "time_block": audit_record.get("time_block"),
        "model_no": audit_record.get("model_no"),
        "audit_time": datetime.now().isoformat(),
        "overall_status": audit_record.get("overall_status", "OK"),
        "pass_count": audit_record.get("pass_count", 0),
        "fail_count": audit_record.get("fail_count", 0),
        "na_count": audit_record.get("na_count", 0),
        "work_order": audit_record.get("work_order", "N/A")
    }
    
    supabase_db_query("audits", method="POST", data=s_record)
    
    new_capas = []
    has_ng = False
    
    for detail in data.details:
        d_record = {
            "audit_id": data.audit_id,
            "item_no": detail.item_no,
            "result": detail.result,
            "qty": detail.qty or 0,
            "remark": detail.remark or "",
            "photo_url": detail.photo_url or ""
        }
        supabase_db_query("audit_details", method="POST", data=d_record)
        
        if detail.result == "X" or detail.result == "NG":
            has_ng = True
            capa_id = f"CAPA-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(2).upper()}"
            capa_entry = {
                "id": capa_id,
                "audit_id": data.audit_id,
                "station_code": data.station_code,
                "line_name": data.line_name or "N/A",
                "item_no": detail.item_no,
                "defect_description": detail.remark or f"Check Item #{detail.item_no} Failed (NG)",
                "severity": "HIGH",
                "status": "OPEN",
                "owner": "Line Supervisor",
                "photo_url": detail.photo_url or "",
                "created_at": datetime.now().isoformat()
            }
            supabase_db_query("capa", method="POST", data=capa_entry)
            new_capas.append(capa_id)

    return {
        "status": "SUCCESS",
        "audit_id": data.audit_id,
        "capas": new_capas,
        "message": f"Audit submitted with {len(new_capas)} CAPAs logged."
    }'''

code = re.sub(submit_pattern, new_submit_logic, code, flags=re.DOTALL)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Done patching.")
