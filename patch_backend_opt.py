import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Patch get_stations valid_audits logic
pattern_stations = r"""    if date and time_block:
        import urllib\.parse
        tb_enc = urllib\.parse\.quote\(time_block\)
        valid_audits = supabase_db_query\("audits", params=f"time_block=eq\.\{tb_enc\}&select=\*"\)
        if not isinstance\(valid_audits, list\): valid_audits = \[\]
        valid_audits = \[a for a in valid_audits if a\.get\("audit_time", ""\)\.startswith\(date\)\]"""

replacement_stations = """    if date and time_block:
        import urllib.parse
        tb_enc = urllib.parse.quote(time_block)
        
        # Optimize query by passing date filters directly to Supabase to save egress!
        valid_audits = supabase_db_query("audits", params=f"time_block=eq.{tb_enc}&audit_time=gte.{date}T00:00:00&audit_time=lte.{date}T23:59:59&select=*")
        if not isinstance(valid_audits, list): valid_audits = []"""

code = re.sub(pattern_stations, replacement_stations, code)


# 2. Patch get_audits endpoint
pattern_audits = r"""@router\.get\("/audits"\)
def get_audits\(user=Depends\(require_role\(\['admin', 'supervisor', 'auditor'\]\)\)\):
    audits = supabase_db_query\("audits", params="select=\*"\)
    if not isinstance\(audits, list\): audits = \[\]
    return audits"""

replacement_audits = """@router.get("/audits")
def get_audits(
    date: Optional[str] = None,
    line_name: Optional[str] = None,
    model_no: Optional[str] = None,
    work_order: Optional[str] = None,
    limit: int = 150,
    user=Depends(require_role(['admin', 'supervisor', 'auditor']))
):
    import urllib.parse
    filters = []
    
    if date:
        filters.append(f"audit_time=gte.{date}T00:00:00")
        filters.append(f"audit_time=lte.{date}T23:59:59")
    if line_name and line_name != "All Lines":
        filters.append(f"line_name=eq.{urllib.parse.quote(line_name)}")
    if model_no:
        filters.append(f"model_no=ilike.*{urllib.parse.quote(model_no)}*")
    if work_order:
        filters.append(f"work_order=ilike.*{urllib.parse.quote(work_order)}*")
        
    param_str = "select=*"
    if filters:
        param_str += "&" + "&".join(filters)
        
    param_str += f"&order=audit_time.desc&limit={limit}"
    
    audits = supabase_db_query("audits", params=param_str)
    if not isinstance(audits, list): audits = []
    return audits"""

code = re.sub(pattern_audits, replacement_audits, code)


with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
