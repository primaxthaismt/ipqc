import re
with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"window\.auditedStationCodes\.add\(stationCode\);"
replacement = """window.auditedStationCodes.add(stationCode);
        try { localStorage.setItem('ipqc_audited_stations', JSON.stringify([...window.auditedStationCodes])); } catch(e){}"""

code = re.sub(pattern, replacement, code)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
