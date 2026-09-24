with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re

pattern = r"function animateLoginSuccess\(callback\) \{.*?async function handleLoginSubmit\(\) \{"

replacement = """function animateLoginSuccess(callback) {
  const icon = document.getElementById('login-lock-icon');
  const iconContainer = document.getElementById('login-lock-icon-container');
  const formContent = document.getElementById('login-form-content');
  
  if (formContent) {
    formContent.style.opacity = '0';
    setTimeout(() => {
      formContent.style.display = 'none';
    }, 500);
  }

  if (icon) {
    icon.textContent = '\\uD83D\\uDD13'; // 🔓
    // Make the lock huge and zoom in
    icon.style.transform = 'scale(4) translateY(20px)';
  }
  
  setTimeout(() => {
    document.getElementById('modal-login')?.classList.remove('active');
    if (callback) callback();
    
    // Reset modal for future logout
    setTimeout(() => {
      if (icon) {
        icon.textContent = '\\uD83D\\uDD12'; // 🔒
        icon.style.transform = 'scale(1) translateY(0)';
      }
      if (formContent) {
        formContent.style.display = 'block';
        setTimeout(() => formContent.style.opacity = '1', 50);
      }
      const loginBtn = document.getElementById('btn-submit-login');
      if (loginBtn) {
        loginBtn.innerHTML = '<span id="txt-loginBtn">\\u767b\\u5f55 System Login</span>';
      }
    }, 1000);
  }, 3000);
}

async function handleLoginSubmit() {"""

match = re.search(pattern, code, flags=re.DOTALL)
if match:
    code = code.replace(match.group(0), replacement)
    with open('public/js/app.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Patched app.js")
else:
    print("Function not found")
