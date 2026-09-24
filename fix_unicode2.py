with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re
pattern = r"function animateLoginSuccess\(callback\) \{.*?async function handleLoginSubmit\(\) \{"
match = re.search(pattern, code, flags=re.DOTALL)
if match:
    old_str = match.group(0)
    replacement = """function animateLoginSuccess(callback) {
  const icon = document.getElementById('login-lock-icon');
  if (icon) {
    icon.textContent = '\\uD83D\\uDD13'; // 🔓
    icon.style.transform = 'scale(1.8) translateY(-10px)';
  }
  const title = document.getElementById('txt-loginModalTitle');
  if (title) {
    title.textContent = 'Login Successful / \\u767b\\u5f55\\u6210\\u529f';
    title.style.color = '#34d399';
  }
  const loginBtn = document.getElementById('btn-submit-login');
  if (loginBtn) {
    loginBtn.style.background = '#34d399';
    loginBtn.style.borderColor = '#34d399';
    loginBtn.textContent = 'Access Granted \\u2714\\uFE0F';
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
      if (title) {
        title.textContent = '\\u767b\\u5f55 Smart IPQC \\u7cfb\\u7edf';
        title.style.color = '#fff';
      }
      if (loginBtn) {
        loginBtn.style.background = '';
        loginBtn.style.borderColor = '';
        loginBtn.innerHTML = '<span id="txt-loginBtn">\\u767b\\u5f55 System Login</span>';
      }
    }, 1000);
  }, 3000);
}

async function handleLoginSubmit() {"""
    code = code.replace(old_str, replacement)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
