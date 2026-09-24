css_content_to_append = """
/* ==========================================================================
   CINEMATIC UNLOCK SPLASH OVERLAY
   ========================================================================== */
.unlock-overlay {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at center, rgba(15, 23, 42, 0.98) 0%, rgba(2, 6, 23, 0.99) 100%);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  z-index: 99999;
  display: none;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.unlock-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.unlock-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: unlockZoomIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes unlockZoomIn {
  0% { transform: scale(0.6); opacity: 0; }
  60% { transform: scale(1.35); opacity: 1; }
  100% { transform: scale(1.2); opacity: 1; }
}

.unlock-glow-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 240px;
  height: 240px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.3) 0%, rgba(52, 211, 153, 0) 70%);
  filter: blur(25px);
  pointer-events: none;
  transition: all 0.6s ease;
}

.unlock-overlay.unlocked .unlock-glow-ring {
  background: radial-gradient(circle, rgba(52, 211, 153, 0.5) 0%, rgba(52, 211, 153, 0) 70%);
  transform: translate(-50%, -50%) scale(1.5);
}

.unlock-icon-wrap {
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 12px 30px rgba(0, 0, 0, 0.6));
}

.padlock-svg {
  display: block;
  overflow: visible;
  transition: all 0.5s ease;
}

.padlock-shackle {
  transition: transform 0.7s cubic-bezier(0.34, 1.56, 0.64, 1), stroke 0.4s ease;
  transform-origin: 32px 30px;
}

.padlock-body {
  transition: stroke 0.4s ease;
}

.padlock-keyhole {
  transition: fill 0.4s ease;
}

.padlock-svg.unlocked .padlock-shackle {
  transform: translateY(-20px) rotate(-24deg);
  stroke: #34d399 !important;
}

.padlock-svg.unlocked .padlock-body {
  stroke: #34d399 !important;
}

.padlock-svg.unlocked .padlock-keyhole {
  fill: #34d399 !important;
}

.unlock-text-group {
  margin-top: 2rem;
  text-align: center;
  animation: unlockFadeUp 0.6s ease 0.3s forwards;
  opacity: 0;
  z-index: 2;
}

@keyframes unlockFadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.unlock-title {
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: 2.5px;
  color: #38bdf8;
  text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
  text-transform: uppercase;
  transition: all 0.4s ease;
}

.unlock-overlay.unlocked .unlock-title {
  color: #34d399;
  text-shadow: 0 0 25px rgba(52, 211, 153, 0.6);
}

.unlock-subtitle {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-top: 0.4rem;
  font-weight: 500;
}
"""

with open('public/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.unlock-overlay' not in css:
    css += css_content_to_append
    with open('public/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Appended unlock styles to styles.css")
else:
    # replace existing
    import re
    css = re.sub(r'/\* =+ CINEMATIC UNLOCK SPLASH OVERLAY =+ \*/.*', css_content_to_append.strip(), css, flags=re.DOTALL)
    with open('public/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Updated unlock styles in styles.css")
