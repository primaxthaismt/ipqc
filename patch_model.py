import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'class AuditSubmitModel\(BaseModel\):\n    audit_id: str\n    station_code: str\n    station_name: str\n    line_name: str\n    auditor: str\n    shift: str\n    time_block: str\n    model_no: str\n    work_order: str\n    details: List\[AuditDetailModel\]'

replacement = 'class AuditSubmitModel(BaseModel):\n    audit_id: str\n    station_code: str\n    station_name: str\n    line_name: str\n    auditor: str\n    shift: str\n    time_block: str\n    model_no: str\n    work_order: str\n    details: List[AuditDetailModel]\n    overall_status: str = "OK"\n    pass_count: int = 0\n    fail_count: int = 0\n    na_count: int = 0'

new_code = re.sub(pattern, replacement, code, flags=re.MULTILINE)

if new_code != code:
    with open('api/index.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print('Patched AuditSubmitModel')
else:
    print('Failed to patch AuditSubmitModel')
