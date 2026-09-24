import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r"""        // Prompt for Audit Report Generation
        if \(newStatus === 'OK' || newStatus === 'NG'\) \{
            if \(confirm\(`Audit Submitted Successfully! \[ID: \$\{auditId\}\]\\n\\nWould you like to generate and send the PDF/HTML Audit Report for this station\?`\)\) \{
                openEmailModal\('audit', auditId\);
            \}
        \} else \{
            alert\(`Audit Submitted Successfully! \[ID: \$\{auditId\}\]`\);
        \}"""

replacement = """
        if (typeof window.auditedStationCodes === 'undefined') window.auditedStationCodes = new Set();
        window.auditedStationCodes.add(stationCode);

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
        }
"""
code = re.sub(pattern, replacement, code)
with open('public/js/app.js', 'w', encoding='utf-8') as f: f.write(code)
