import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r"""        // Prompt for Audit Report Generation
        if \(newStatus === 'OK' || newStatus === 'NG'\) \{
            if \(confirm\(`Audit Submitted Successfully! \[ID: \$\{auditId\}\]\n\nWould you like to generate and send the PDF/HTML Audit Report for this station\?`\)\) \{
                openEmailModal\('audit', auditId\);
            \}
        \} else \{
            alert\(`Audit Submitted Successfully! \[ID: \$\{auditId\}\]`\);
        \}"""

replacement = """        // Add current station to audited set
        if (typeof window.auditedStationCodes === 'undefined') window.auditedStationCodes = new Set();
        window.auditedStationCodes.add(stationCode);

        // Check if entire line is audited
        let activeDataset = (typeof fetchedStations !== 'undefined' && fetchedStations.length > 0) ? fetchedStations : ((typeof masterStationsData !== 'undefined' && masterStationsData.length > 0) ? masterStationsData : defaultStations);
        const lineStations = activeDataset.filter(s => s.line_name === lineName || s.line === lineName);
        const allAudited = lineStations.every(s => s.status === 'OK' || s.status === 'NG' || window.auditedStationCodes.has(s.station_code || s.code || s.id));

        // Prompt for Audit Report Generation ONLY when entire line nodes have been audited
        if ((newStatus === 'OK' || newStatus === 'NG') && allAudited) {
            if (confirm(`Audit Submitted Successfully! [ID: ${auditId}]\\n\\nAll stations on ${lineName} have been audited!\\nWould you like to generate and send the PDF/HTML Audit Report for this line?`)) {
                openEmailModal('audit', auditId);
            }
        } else {
            alert(`Audit Submitted Successfully! [ID: ${auditId}]`);
        }"""

# Actually, to avoid regex issues, I will just find the index!
start = code.find("// Prompt for Audit Report Generation")
if start != -1:
    end = code.find("}", code.find("alert(`Audit")) + 1
    new_code = code[:start] + replacement + code[end:]
    with open('public/js/app.js', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Replaced!")
else:
    print("Not found!")
