import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r"alert\(`[^\`]*Audit Submitted Successfully![^\`]*\[ID: \$\{auditId\}\]`\);"
replacement = r"""
        // Prompt for Audit Report Generation
        if (newStatus === 'OK' || newStatus === 'NG') {
            if (confirm(`Audit Submitted Successfully! [ID: ${auditId}]\n\nWould you like to generate and send the PDF/HTML Audit Report for this station?`)) {
                openEmailModal('audit', auditId);
            }
        } else {
            alert(`Audit Submitted Successfully! [ID: ${auditId}]`);
        }
"""
code = re.sub(pattern, replacement, code)
with open('public/js/app.js', 'w', encoding='utf-8') as f: f.write(code)
