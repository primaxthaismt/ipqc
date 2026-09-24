import json
import re
import urllib.request
import os
from api.index import supabase_db_query

print('Extracting masterStationsData...')
with open('public/js/checklist_data.js', 'r', encoding='utf-8') as f:
    code = f.read()
m = re.search(r'const masterStationsData = (\[.*?\]);\s*const masterChecklistData', code, flags=re.DOTALL)
data = json.loads(m.group(1))

print('Clearing existing...')
existing = supabase_db_query('stations', params='select=id')
if existing:
    for s in existing:
        supabase_db_query('stations', method='DELETE', params=f"id=eq.{s['id']}")

print('Inserting 165 stations...')
inserted = 0
for st in data:
    new_st = {
        'id': st.get('id'),
        'station_code': st.get('station_code') or st.get('code'),
        'station_name': st.get('station_name') or st.get('name'),
        'line_name': st.get('line_name') or st.get('line'),
        'area_name': st.get('area_name') or st.get('area'),
        'process_type': st.get('process_type') or st.get('process') or st.get('tag'),
        'sequence_order': st.get('sequence_order', 1),
        'pos_x': st.get('pos_x', 50),
        'pos_y': st.get('pos_y', 50),
        'width': 210,
        'height': 135,
        'status': 'OK',
        'is_active': True
    }
    
    req = urllib.request.Request(f'https://yfpowaudcciepubtjkdr.supabase.co/rest/v1/stations', data=json.dumps(new_st).encode('utf-8'), method='POST')
    req.add_header('apikey', os.environ.get('SUPABASE_ANON_KEY', 'sb_publishable_shOnteL2raHE5OynKjPkPw_aHX3vp5F'))
    req.add_header('Authorization', 'Bearer sb_publishable_shOnteL2raHE5OynKjPkPw_aHX3vp5F')
    req.add_header('Content-Type', 'application/json')
    try:
        urllib.request.urlopen(req)
        inserted += 1
    except Exception as e:
        print('Error on', new_st['station_code'], e.read().decode())

print(f'Done! Inserted {inserted}')
