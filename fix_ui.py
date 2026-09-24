import re

# 1. Update index.html inline styles for responsiveness
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add flex-wrap to Row 1
html = html.replace(
    'justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 0.75rem;"',
    'justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 0.75rem; flex-wrap: wrap;"'
)

# Make ui-layout-mode-tabs responsive
html = html.replace(
    'id="ui-layout-mode-tabs"',
    'id="ui-layout-mode-tabs" class="layout-mode-tabs"'
)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update styles.css with enhanced media queries
with open('public/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_media_queries = """
/* ==========================================================================
   RESPONSIVE LAYOUT (Mobile & Tablet Optimization)
   ========================================================================== */

/* Tablet & Smaller Desktops (<= 1024px) */
@media (max-width: 1024px) {
  .navbar { padding: 0.75rem 1rem; }
  .container { padding: 0 0.85rem; }
  .kanban-board { grid-template-columns: 1fr 1fr; }
  .filter-toolbar {
    padding: 6px;
    gap: 4px;
  }
  .filter-chip {
    padding: 3px 8px;
    font-size: 0.65rem;
  }
  .toolbar-stats {
    font-size: 0.6rem;
  }
}

/* Mobile & Touchscreens (<= 768px) */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  .nav-controls {
    justify-content: space-between;
    width: 100%;
  }
  .card-title {
    font-size: 1.05rem;
  }
  .wo-header-bar {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  .kanban-board {
    grid-template-columns: 1fr;
  }
  .modal-content {
    padding: 1rem;
    width: 95%;
  }
  .factory-layout-canvas {
    min-height: 400px;
  }
  
  /* Header UI Refinements for Mobile */
  .layout-mode-tabs {
    width: 100%;
    justify-content: space-between;
  }
  .layout-mode-btn {
    flex: 1;
    text-align: center;
    padding: 6px 4px;
    font-size: 0.7rem;
  }
  
  .filter-toolbar {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    flex-wrap: nowrap;
    scrollbar-width: none; /* Firefox */
  }
  .filter-toolbar::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
  }
}
"""

# Replace the existing media queries at the bottom of the file
# Using a regex to carefully replace everything from "/* Tablet & Smaller Desktops" to just before ".canvas-node-card.status-partial"
css = re.sub(r'/\* Tablet & Smaller Desktops.*?(?=\.canvas-node-card\.status-partial)', new_media_queries, css, flags=re.DOTALL)

with open('public/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("UI optimization applied successfully.")
