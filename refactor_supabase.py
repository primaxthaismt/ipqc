import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace STATIONS_DB references with Supabase
code = re.sub(r'def get_stations\(.*?\):.*?return results', '''def get_stations(
    phase: Optional[str] = None,
    line_name: Optional[str] = None,
    line_type: Optional[str] = None,
    standard_doc: Optional[str] = None,
    area_name: Optional[str] = None,
    date: Optional[str] = None,
    time_block: Optional[str] = None
):
    import copy
    db_stations = supabase_db_query("stations", params="select=*")
    if not isinstance(db_stations, list): db_stations = []
    
    results = copy.deepcopy(db_stations)
    if phase and phase != "All Phases":
        results = [s for s in results if s.get("phase") == phase]
    if line_name and line_name != "All Lines":
        results = [s for s in results if s.get("line_name") == line_name or s.get("line") == line_name]
    if line_type and line_type != "All":
        results = [s for s in results if s.get("line_type") == line_type]
    if standard_doc and standard_doc != "All":
        results = [s for s in results if s.get("standard_doc") == standard_doc]
    if area_name and area_name != "All Areas":
        results = [s for s in results if s.get("area_name") == area_name or s.get("area") == area_name]

    if date and time_block:
        valid_audits = supabase_db_query("audits", params=f"time_block=eq.{time_block}&select=*")
        if not isinstance(valid_audits, list): valid_audits = []
        valid_audits = [a for a in valid_audits if a.get("audit_time", "").startswith(date)]
        
        for s in results:
            s_code = s.get("station_code") or s.get("code")
            s_audits = [a for a in valid_audits if a.get("station_code") == s_code]
            if not s_audits:
                s["status"] = "PENDING"
            else:
                latest_audit = sorted(s_audits, key=lambda x: x.get("audit_time", ""), reverse=True)[0]
                total_items = 100
                if s.get("standard_doc") == "5Q4-046":
                    total_items = 109
                elif s.get("standard_doc") == "5Q4-053":
                    total_items = 103
                    
                total_answered = latest_audit.get("pass_count", 0) + latest_audit.get("fail_count", 0) + latest_audit.get("na_count", 0)
                
                if total_answered < total_items:
                    s["status"] = "PARTIAL"
                else:
                    s["status"] = latest_audit.get("overall_status", "OK")
    return results''', code, flags=re.DOTALL)

# Refactor create_station
code = re.sub(r'def create_station\(.*?\):.*?return new_st', '''def create_station(station: StationCreateModel, user=Depends(require_role(["admin"]))):
    import uuid
    st_id = str(uuid.uuid4())
    new_st = {
        "id": st_id,
        "station_code": station.station_code,
        "station_name": station.station_name,
        "line_name": station.line_name,
        "area_name": station.area_name,
        "process_type": station.process_type,
        "sequence_order": station.sequence_order,
        "pos_x": station.pos_x,
        "pos_y": station.pos_y,
        "status": "OK"
    }
    supabase_db_query("stations", method="POST", data=new_st)
    return new_st''', code, flags=re.DOTALL)

# Refactor update_station_layout_bulk
code = re.sub(r'def update_station_layout_bulk\(.*?\):.*?return \{"status": "SUCCESS"\}', '''def update_station_layout_bulk(nodes: List[NodePositionModel], user=Depends(require_role(["admin", "supervisor"]))):
    for node in nodes:
        supabase_db_query("stations", method="PATCH", params=f"station_code=eq.{node.station_code}", data={"pos_x": node.pos_x, "pos_y": node.pos_y})
    return {"status": "SUCCESS"}''', code, flags=re.DOTALL)

# Refactor update_station
code = re.sub(r'def update_station\(.*?\):.*?return target', '''def update_station(station_id: str, updates: dict, user=Depends(require_role(["admin", "supervisor"]))):
    supabase_db_query("stations", method="PATCH", params=f"id=eq.{station_id}", data=updates)
    return updates''', code, flags=re.DOTALL)

# Refactor delete_station
code = re.sub(r'def delete_station\(.*?\):.*?return \{"status": "DELETED"\}', '''def delete_station(station_id: str, user=Depends(require_role(["admin"]))):
    supabase_db_query("stations", method="DELETE", params=f"id=eq.{station_id}")
    return {"status": "DELETED"}''', code, flags=re.DOTALL)

# Refactor submit_audit
code = re.sub(r'def submit_audit\(.*?\):.*?return \{"status": "SUCCESS", "audit_id": audit_id\}', '''def submit_audit(payload: dict, user=Depends(require_auth)):
    import datetime, uuid
    audit_id = f"AUD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4]}"
    
    audit_record = {
        "id": audit_id,
        "station_code": payload.get("station_code"),
        "station_name": payload.get("station_name"),
        "line_name": payload.get("line_name", ""),
        "auditor": user["full_name"],
        "shift": payload.get("shift", "Day Shift"),
        "time_block": payload.get("time_block", "08:00 - 10:00"),
        "model_no": payload.get("model_no", "UNKNOWN"),
        "audit_time": datetime.datetime.now().isoformat(),
        "overall_status": payload.get("overall_status", "OK"),
        "pass_count": payload.get("pass_count", 0),
        "fail_count": payload.get("fail_count", 0),
        "na_count": payload.get("na_count", 0),
        "work_order": payload.get("work_order", "N/A")
    }
    
    supabase_db_query("audits", method="POST", data=audit_record)
    
    details = payload.get("details", [])
    for d in details:
        det = {
            "audit_id": audit_id,
            "item_no": d.get("item_no"),
            "result": d.get("result"),
            "qty": d.get("qty", 0),
            "remark": d.get("remark", ""),
            "photo_url": d.get("photo_url", "")
        }
        supabase_db_query("audit_details", method="POST", data=det)
        
        if d.get("result") == "NG":
            capa_id = f"CAPA-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4]}"
            capa_record = {
                "id": capa_id,
                "audit_id": audit_id,
                "station_code": payload.get("station_code"),
                "line_name": payload.get("line_name", ""),
                "item_no": d.get("item_no"),
                "defect_description": d.get("remark", "Defect recorded"),
                "photo_url": d.get("photo_url", ""),
                "severity": "HIGH",
                "status": "OPEN",
                "owner": "Line Supervisor",
                "created_at": datetime.datetime.now().isoformat()
            }
            supabase_db_query("capa", method="POST", data=capa_record)
            
    return {"status": "SUCCESS", "audit_id": audit_id}''', code, flags=re.DOTALL)

# Refactor get_audits
code = re.sub(r'def get_audits\(.*?\):.*?return AUDITS_DB', '''def get_audits(user=Depends(require_auth)):
    audits = supabase_db_query("audits", params="select=*")
    if not isinstance(audits, list): audits = []
    return audits''', code, flags=re.DOTALL)

# Refactor get_capas
code = re.sub(r'def get_capas\(.*?\):.*?return CAPA_DB', '''def get_capas(user=Depends(require_auth)):
    capas = supabase_db_query("capa", params="select=*")
    if not isinstance(capas, list): capas = []
    return capas''', code, flags=re.DOTALL)

# Refactor update_capa
code = re.sub(r'def update_capa\(.*?\):.*?return \{"status": "UPDATED"\}', '''def update_capa(capa_id: str, payload: dict, user=Depends(require_auth)):
    supabase_db_query("capa", method="PATCH", params=f"id=eq.{capa_id}", data=payload)
    return {"status": "UPDATED"}''', code, flags=re.DOTALL)

# Refactor get_analytics
code = re.sub(r'def get_analytics\(.*?\):.*?return results', '''def get_analytics(user=Depends(require_auth)):
    audits = supabase_db_query("audits", params="select=*")
    if not isinstance(audits, list): audits = []
    
    total = len(audits)
    ng = len([a for a in audits if a.get("overall_status") == "NG"])
    ok = total - ng
    yield_rate = (ok / total * 100) if total > 0 else 100.0

    capas = supabase_db_query("capa", params="select=*")
    if not isinstance(capas, list): capas = []
    open_capas = len([c for c in capas if c.get("status") in ["OPEN", "INVESTIGATING", "ACTIONING"]])

    top_defects = {}
    for c in capas:
        item = c.get("item_no")
        if item is not None:
            top_defects[item] = top_defects.get(item, 0) + 1
    
    sorted_defects = [{"item": str(k), "count": v} for k, v in sorted(top_defects.items(), key=lambda item: item[1], reverse=True)[:10]]

    results = {
        "total_audits": total,
        "yield_rate": round(yield_rate, 2),
        "open_capas": open_capas,
        "top_defects": sorted_defects
    }
    return results''', code, flags=re.DOTALL)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done refactoring!")
