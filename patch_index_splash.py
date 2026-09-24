import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Clean up modal-login and add unlock-splash-overlay
clean_login_and_splash = """  <!-- Login Modal -->
  <div id="modal-login" class="modal-overlay active">
    <div class="modal-content" style="max-width: 440px;">
      <div style="text-align: center; margin-bottom: 1.5rem;">
        <div id="login-lock-icon" style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔐</div>
        <h2 style="color: #fff; font-size: 1.4rem;" id="txt-loginModalTitle">登录 Smart IPQC 系统</h2>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">Enter your inspector or supervisor credentials to access the digital audit floor.</p>
      </div>

      <div style="margin-bottom: 1rem;">
        <label style="font-size: 0.8rem; color: var(--text-muted);">Username / Email / Employee ID 账号/邮箱/工号:</label>
        <input type="text" id="login-username" placeholder="e.g. admin or norman.nan or auditor1" autocomplete="username" style="width: 100%; margin-top: 0.3rem; background: #0f172a; border: 1px solid var(--border-color); border-radius: 8px; color: #fff; padding: 0.65rem;">
      </div>

      <div style="margin-bottom: 1.25rem;">
        <label style="font-size: 0.8rem; color: var(--text-muted);">Password 密码:</label>
        <input type="password" id="login-password" placeholder="Enter your password (e.g. admin123)" autocomplete="current-password" style="width: 100%; margin-top: 0.3rem; background: #0f172a; border: 1px solid var(--border-color); border-radius: 8px; color: #fff; padding: 0.65rem;">
      </div>

      <button id="btn-submit-login" class="btn-primary" style="width: 100%; padding: 0.85rem;">
        <span id="txt-loginBtn">登录 System Login</span>
      </button>

      <div style="text-align: center; margin-top: 1.25rem; border-top: 1px solid var(--border-color); padding-top: 1rem;">
        <button id="btn-toggle-to-register" class="btn-select" style="width: 100%; padding: 0.65rem; font-size: 0.82rem; color: var(--accent-cyan);">
          📝 首次使用？注册巡检员账号 (Register as Inspector)
        </button>
        <button type="button" onclick="if(navigator.serviceWorker){navigator.serviceWorker.getRegistrations().then(function(regs){for(let r of regs)r.unregister();});}caches.keys().then(function(k){for(let key of k)caches.delete(key);});localStorage.clear();sessionStorage.clear();alert('Cache cleared! Refreshing...');window.location.reload(true);" class="btn-select" style="width: 100%; padding: 0.5rem; margin-top: 0.5rem; font-size: 0.75rem; color: #ef4444; border-color: rgba(239, 68, 68, 0.3);">
          ⚠️ 系统更新修复 (Clear Cache & Reset System)
        </button>
      </div>
    </div>
  </div>

  <!-- Dedicated High-Tech Unlock Splash Overlay -->
  <div id="unlock-splash-overlay" class="unlock-overlay">
    <div class="unlock-container">
      <div class="unlock-glow-ring"></div>
      <div class="unlock-icon-wrap">
        <svg id="unlock-svg" class="padlock-svg" viewBox="0 0 100 100" width="130" height="130">
          <defs>
            <linearGradient id="padlock-body-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            <filter id="glow-filter" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>
          <!-- Padlock Shackle -->
          <path id="padlock-shackle" class="padlock-shackle" d="M32 46 V28 C32 17, 68 17, 68 28 V46" fill="none" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
          <!-- Padlock Body -->
          <rect id="padlock-body" class="padlock-body" x="20" y="44" width="60" height="48" rx="12" fill="url(#padlock-body-grad)" stroke="#38bdf8" stroke-width="3.5"/>
          <!-- Keyhole -->
          <circle class="padlock-keyhole" cx="50" cy="63" r="5" fill="#38bdf8"/>
          <path class="padlock-keyhole" d="M47.5 65 L52.5 65 L51.5 76 L48.5 76 Z" fill="#38bdf8"/>
        </svg>
      </div>
      <div class="unlock-text-group">
        <div id="unlock-title" class="unlock-title">VERIFYING ACCESS</div>
        <div id="unlock-subtitle" class="unlock-subtitle">Smart IPQC Digital Floor System</div>
      </div>
    </div>
  </div>"""

modal_pattern = r'<!-- Login Modal -->.*?<!-- Inspector Self-Registration Modal -->'
match = re.search(modal_pattern, html, flags=re.DOTALL)
if match:
    html = html[:match.start()] + clean_login_and_splash + '\n\n  <!-- Inspector Self-Registration Modal -->' + html[match.end():]
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully patched index.html with clean login modal and unlock splash overlay")
else:
    print("Could not match login modal pattern in index.html")
