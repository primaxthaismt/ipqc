import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find the exact modal content
modal_start = html.find('<div id="modal-login" class="modal-overlay active">')
modal_end = html.find('<!-- Inspector Self-Registration Modal -->', modal_start)

modal_html = html[modal_start:modal_end]

# Modify the modal HTML
# Extract lock icon
lock_pattern = r'<div id="login-lock-icon"[^>]*>.*?</div>'
lock_match = re.search(lock_pattern, modal_html)
if lock_match:
    lock_html = lock_match.group(0)
    
    # Remove lock from original position
    modal_html = modal_html.replace(lock_html, '')
    
    # Change modal-content to center things and have a fixed height so it doesn't collapse when we hide form
    content_start = modal_html.find('<div class="modal-content"')
    content_end = modal_html.find('>', content_start) + 1
    
    # Wrap the rest of the contents in login-form-content
    inner_start = content_end
    inner_end = modal_html.rfind('</div>', 0, modal_html.rfind('</div>')) # The closing div of modal-content
    
    new_inner = f'\n        <div id="login-lock-icon-container" style="text-align: center; width: 100%; transition: all 1s ease-in-out;">\n          {lock_html}\n        </div>\n        <div id="login-form-content" style="width: 100%; transition: opacity 0.5s ease; opacity: 1;">\n' + modal_html[inner_start:inner_end] + '\n        </div>\n'
    
    new_modal_html = modal_html[:inner_start] + new_inner + modal_html[inner_end:]
    
    # Put back into main HTML
    final_html = html[:modal_start] + new_modal_html + html[modal_end:]
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("Patched index.html")
else:
    print("Lock icon not found")
