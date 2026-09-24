import json
import os
import hashlib

def hash_password(password: str) -> str:
    salt = b'IPQC_SALT_2026'
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

sql = []
default_users = [
    ('USR-ADMIN-01', 'admin', hash_password('admin123'), 'Norman Nan (QA Manager)', 'admin', 'All Lines', 'zh'),
    ('USR-SUP-01', 'supervisor1', hash_password('password123'), 'John Tan (Line Supervisor)', 'supervisor', 'SMT Line 1', 'en'),
    ('USR-AUD-01', 'auditor1', hash_password('password123'), 'Somchai (IPQC Inspector)', 'auditor', 'SMT Line 1', 'th')
]
for uid, uname, p_hash, fname, urole, uline, ulang in default_users:
    sql.append(f"INSERT INTO public.users (id, username, password_hash, full_name, role, line_assignment, language_pref) VALUES ('{uid}', '{uname}', '{p_hash}', '{fname}', '{urole}', '{uline}', '{ulang}') ON CONFLICT (username) DO NOTHING;")

default_stations = [
  ('SMT-L1-ESD-01', 'SMT-L1-ESD-01', 'Central ESD & IQC Material Station', 'SMT Line 1', 'Quality & ESD Area', 'ESD', 1, 30, 40),
  ('SMT-L1-PRINT-01', 'SMT-L1-PRINT-01', 'Solder Paste Printer #1', 'SMT Line 1', 'SMT Surface Mount Area', 'SMT-Printer', 2, 280, 40),
  ('SMT-L1-SPI-01', 'SMT-L1-SPI-01', '3D Solder Paste Inspector #1', 'SMT Line 1', 'SMT Surface Mount Area', 'SMT-SPI', 3, 530, 40),
  ('SMT-L1-MNT-01', 'SMT-L1-MNT-01', 'High-Speed Chip Mounter #1', 'SMT Line 1', 'SMT Surface Mount Area', 'SMT-Mounter', 4, 780, 40),
  ('SMT-L1-OVEN-01', 'SMT-L1-OVEN-01', '10-Zone Nitrogen Reflow Oven #1', 'SMT Line 1', 'SMT Surface Mount Area', 'SMT-Reflow', 5, 1030, 40),
  ('SMT-L1-AOI-01', 'SMT-L1-AOI-01', '3D AOI Post-Reflow Inspection #1', 'SMT Line 1', 'SMT Surface Mount Area', 'SMT-AOI', 6, 1280, 40),
  ('DIP-L1-INS-01', 'DIP-L1-INS-01', 'DIP Through-Hole Insertion #1', 'DIP Line 1', 'DIP Through-Hole Area', 'DIP-Insertion', 7, 280, 230),
  ('DIP-L1-WAVE-01', 'DIP-L1-WAVE-01', 'Dual-Wave Lead-Free Soldering #1', 'DIP Line 1', 'DIP Through-Hole Area', 'DIP-Wave', 8, 530, 230),
  ('ASY-L1-MAIN-01', 'ASY-L1-MAIN-01', 'Main Mechanical Assembly #1', 'Assembly Line 1', 'Assembly & Packaging Area', 'Assembly', 9, 280, 420),
  ('ASY-L1-FCT-01', 'ASY-L1-FCT-01', 'FCT & ICT Programming Station #1', 'Assembly Line 1', 'Assembly & Packaging Area', 'Programming & FCT', 10, 530, 420),
  ('ASY-L1-PACK-01', 'ASY-L1-PACK-01', 'Final Inspection & Box Packaging #1', 'Assembly Line 1', 'Assembly & Packaging Area', 'Inspection & Packaging', 11, 780, 420)
]
for sid, scode, sname, sline, sarea, sproc, seq, px, py in default_stations:
    sql.append(f"INSERT INTO public.stations (id, station_code, station_name, line_name, area_name, process_type, sequence_order, pos_x, pos_y, width, height, qr_code_url) VALUES ('{sid}', '{scode}', '{sname}', '{sline}', '{sarea}', '{sproc}', {seq}, {px}, {py}, 210, 135, 'https://audit.company.com/station/{scode}') ON CONFLICT (station_code) DO NOTHING;")

json_path = os.path.join(os.getcwd(), 'checklist_master.json')
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data.get('all_items', []):
            z = item.get('zh', '').replace("'", "''")
            e = item.get('en', '').replace("'", "''")
            t = item.get('th', '').replace("'", "''")
            rq = 'TRUE' if item.get('requires_qty') else 'FALSE'
            sql.append(f"INSERT INTO public.checklist_master (item_no, process, station_tag, requires_qty, zh, en, th) VALUES ({item['item_no']}, '{item.get('process', '')}', '{item.get('station_tag', 'ESD')}', {rq}, '{z}', '{e}', '{t}') ON CONFLICT (item_no) DO NOTHING;")

sql.append("INSERT INTO public.capa (id, audit_id, station_code, line_name, item_no, defect_description, photo_url, severity, status, owner, due_date) VALUES ('CAPA-2026-001', 'AUD-1001', 'SMT-L1-OVEN-01', 'SMT Line 1', 70, 'Nitrogen Flow rate below 150L/min threshold', 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=500', 'HIGH', 'OPEN', 'Norman Nan (Line Supervisor)', CURRENT_DATE + INTERVAL '2 days'), ('CAPA-2026-002', 'AUD-1002', 'SMT-L1-ESD-01', 'Global Factory', 3, 'Operator wrist strap grounding wire unclipped at Station 4', 'https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=500', 'MEDIUM', 'INVESTIGATING', 'John Tan (QA Eng)', CURRENT_DATE + INTERVAL '2 days') ON CONFLICT DO NOTHING;")

with open('supabase/seed.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql))
