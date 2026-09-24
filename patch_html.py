import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Give the lock icon an ID
pattern_lock = r'<div style="font-size: 2\.5rem; margin-bottom: 0\.5rem;">(.)</div>'
replacement_lock = r'<div id="login-lock-icon" style="font-size: 2.5rem; margin-bottom: 0.5rem; display: inline-block; transition: all 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);">\1</div>'
html = re.sub(pattern_lock, replacement_lock, html)

# 2. Remove the quick login section
pattern_quick_login = r'<div style="margin-top: 0\.85rem; padding: 0\.65rem 0\.85rem; background: rgba\(56,189,248,0\.08\);.*?</div>\s*</div>'
html = re.sub(pattern_quick_login, '', html, flags=re.DOTALL)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
