import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add nav tab
tab_pattern = r'(<button class="nav-tab" data-tab="analytics">)'
tab_replacement = r'<button class="nav-tab" data-tab="history"><span id="txt-navHistory">📝 Audit History</span></button>\n      \1'
html = re.sub(tab_pattern, tab_replacement, html)

# Add section
section_pattern = r'(<!-- 3\. Analytics & Pareto View -->)'
section_replacement = r"""<!-- 2.5 Audit History View -->
    <section id="view-history" class="view-section">
      <div class="glass-card" style="min-height: 80vh;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <div>
            <div class="card-title">📝 Audit History & Report Generation</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">Query completed audits by Date, Line, Model, or Work Order.</p>
          </div>
        </div>

        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
          <input type="date" id="history-filter-date" class="login-input" style="flex: 1; min-width: 150px; background: rgba(15,23,42,0.8);">
          <select id="history-filter-line" class="login-input" style="flex: 1; min-width: 150px; background: rgba(15,23,42,0.8);">
            <option value="">All Lines</option>
            <option value="SMT Line 1">SMT Line 1</option>
            <option value="SMT Line 2">SMT Line 2</option>
            <option value="SMT Line T1">SMT Line T1</option>
            <option value="DIP Line DIP1">DIP Line DIP1</option>
            <option value="DIP Line DIP2">DIP Line DIP2</option>
            <option value="Assembly Line 1">Assembly Line 1</option>
            <option value="Packaging Line">Packaging Line</option>
          </select>
          <input type="text" id="history-filter-model" class="login-input" placeholder="Model No (e.g. PRX-)" style="flex: 1; min-width: 150px; background: rgba(15,23,42,0.8);">
          <input type="text" id="history-filter-wo" class="login-input" placeholder="Work Order (e.g. WO-)" style="flex: 1; min-width: 150px; background: rgba(15,23,42,0.8);">
          <button class="btn-primary" onclick="loadAuditHistory()" style="padding: 0 1.5rem;">Search</button>
        </div>

        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border-color); color: var(--text-muted);">
                <th style="padding: 0.75rem;">Date/Time</th>
                <th style="padding: 0.75rem;">Audit ID</th>
                <th style="padding: 0.75rem;">Line Name</th>
                <th style="padding: 0.75rem;">Model / WO</th>
                <th style="padding: 0.75rem;">Station / Overall</th>
                <th style="padding: 0.75rem;">Auditor</th>
                <th style="padding: 0.75rem; text-align: right;">Actions</th>
              </tr>
            </thead>
            <tbody id="history-table-body">
              <tr>
                <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">Loading audit history...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    \1"""
html = re.sub(section_pattern, section_replacement, html)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
