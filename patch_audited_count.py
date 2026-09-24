import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r"const auditedCount = lineStations\.filter\(s => auditedSet\.has\(s\.station_code \|\| s\.code \|\| s\.id\)\)\.length;"
replacement = r"const auditedCount = lineStations.filter(s => s.status === 'OK' || auditedSet.has(s.station_code || s.code || s.id)).length;"

code = re.sub(pattern, replacement, code)
with open('public/js/app.js', 'w', encoding='utf-8') as f: f.write(code)
