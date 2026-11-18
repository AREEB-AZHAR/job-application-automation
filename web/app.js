// AutoJobBot Dashboard Application Logic
let state = {
  metrics: {},
  applications: [],
  scanned: [],
  candidate: {},
  activeTab: 'applications',
  searchQuery: '',
  selectedDomain: 'all',
  selectedStatus: 'all',
  currentModalApp: null
};

// Domain display mapping
const domainLabels = {
  full_stack: 'Full-Stack Web',
  rust_blockchain: 'Rust & Blockchain',
  flutter: 'Flutter / Mobile',
  ai_ml: 'AI / Machine Learning',
  game_dev: 'Game Development',
  other: 'Other'
};

document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  loadData();
});

function initEventListeners() {
  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.dataset.tab;
      switchTab(tab);
    });
  });

  // Search & Filters
  const searchInput = document.getElementById('input-search');
  searchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value.toLowerCase();
    renderActiveTab();
  });

  const domainSelect = document.getElementById('filter-domain');
  domainSelect.addEventListener('change', (e) => {
    state.selectedDomain = e.target.value;
    renderActiveTab();
  });

  const statusSelect = document.getElementById('filter-status');
  statusSelect.addEventListener('change', (e) => {
    state.selectedStatus = e.target.value;
    renderActiveTab();
  });

  // Refresh
  document.getElementById('btn-refresh').addEventListener('click', loadData);

  // Modals
  document.getElementById('btn-close-modal').addEventListener('click', closeModal);
  document.getElementById('modal-packet').addEventListener('click', (e) => {
    if (e.target.id === 'modal-packet') closeModal();
  });

  document.getElementById('btn-copy-cover').addEventListener('click', copyCoverLetter);
  document.getElementById('btn-save-status').addEventListener('click', saveModalStatus);

  // Quick Evaluate
  document.getElementById('btn-quick-evaluate').addEventListener('click', openEvalModal);
  document.getElementById('btn-close-eval-modal').addEventListener('click', closeEvalModal);
  document.getElementById('modal-evaluate').addEventListener('click', (e) => {
    if (e.target.id === 'modal-evaluate') closeEvalModal();
  });
  document.getElementById('form-evaluate').addEventListener('submit', handleEvaluateSubmit);
}

async function loadData() {
  try {
    const res = await fetch('/api/data');
    if (!res.ok) throw new Error('Failed to fetch data');
    const data = await res.json();
    
    state.metrics = data.metrics || {};
    state.applications = data.applications || [];
    state.scanned = data.scanned || [];
    state.candidate = data.candidate || {};

    updateKPIs();
    renderActiveTab();
    renderAnalytics();
  } catch (err) {
    console.error('Error loading data:', err);
  }
}

function updateKPIs() {
  const m = state.metrics;
  document.getElementById('stat-scanned').textContent = m.total_scanned || 0;
  document.getElementById('stat-qual-rate').textContent = `${m.qualification_rate || 0}% Qualified Rate`;
  
  const readyCount = (m.by_status && m.by_status['READY_FOR_REVIEW']) || 0;
  const submittedCount = (m.by_status && m.by_status['SUBMITTED']) || 0;
  
  document.getElementById('stat-ready').textContent = readyCount;
  document.getElementById('stat-submitted').textContent = submittedCount;
  document.getElementById('stat-disqualified').textContent = m.total_disqualified || 0;

  document.getElementById('badge-applications-count').textContent = state.applications.length;
  document.getElementById('badge-scanned-count').textContent = state.scanned.length;
}

function switchTab(tab) {
  state.activeTab = tab;
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.querySelectorAll('.tab-view').forEach(view => {
    view.classList.toggle('active', view.id === `view-${tab}`);
  });
  renderActiveTab();
}

function renderActiveTab() {
  if (state.activeTab === 'applications') {
    renderApplications();
  } else if (state.activeTab === 'scanned') {
    renderScanned();
  } else if (state.activeTab === 'analytics') {
    renderAnalytics();
  }
}

// -------------------------------------------------------------
// Applications View
// -------------------------------------------------------------
function renderApplications() {
  const grid = document.getElementById('applications-grid');
  const empty = document.getElementById('applications-empty');

  const filtered = state.applications.filter(app => {
    const q = state.searchQuery;
    const matchSearch = !q || 
      (app.title && app.title.toLowerCase().includes(q)) ||
      (app.company && app.company.toLowerCase().includes(q)) ||
      (app.location && app.location.toLowerCase().includes(q)) ||
      (app.domain && app.domain.toLowerCase().includes(q));

    const matchDomain = state.selectedDomain === 'all' || app.domain === state.selectedDomain;
    const matchStatus = state.selectedStatus === 'all' || app.status === state.selectedStatus;

    return matchSearch && matchDomain && matchStatus;
  });

  if (filtered.length === 0) {
    grid.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');

  grid.innerHTML = filtered.map(app => {
    const domainText = domainLabels[app.domain] || app.domain || 'Software Engineer';
    const cvName = app.cv_path ? app.cv_path.split('\\').pop().split('/').pop() : 'Default CV';
    const status = app.status || 'READY_FOR_REVIEW';

    return `
      <div class="job-card" data-id="${app.id}">
        <div>
          <div class="job-card-header">
            <div class="company-meta">
              <span>🏢 ${escapeHtml(app.company)}</span>
              <span>•</span>
              <span>${escapeHtml(app.location)}</span>
            </div>
            <span class="source-pill">${escapeHtml(app.source || 'Job Board')}</span>
          </div>

          <h3 class="job-card-title">${escapeHtml(app.title)}</h3>

          <div class="job-tags-row">
            <span class="tag-domain">${domainText}</span>
            <span class="status-badge status-${status}">
              ● ${status.replace(/_/g, ' ')}
            </span>
          </div>

          <div class="cv-pill" title="${escapeHtml(app.cv_path)}">
            <span>📎 Attached CV:</span>
            <code>${escapeHtml(cvName)}</code>
          </div>
        </div>

        <div class="job-card-actions">
          <button class="btn btn-secondary btn-sm" onclick="openPacketModal('${app.id}')">
            🔍 Inspect Packet & Cover Letter
          </button>
          ${app.url ? `<a href="${app.url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">Open Post ↗</a>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

// -------------------------------------------------------------
// Scanned Audit Log View
// -------------------------------------------------------------
function renderScanned() {
  const tbody = document.getElementById('scanned-tbody');
  const empty = document.getElementById('scanned-empty');

  const filtered = state.scanned.filter(item => {
    const q = state.searchQuery;
    const matchSearch = !q || 
      (item.title && item.title.toLowerCase().includes(q)) ||
      (item.company && item.company.toLowerCase().includes(q)) ||
      (item.location && item.location.toLowerCase().includes(q)) ||
      (item.reason && item.reason.toLowerCase().includes(q));

    const matchDomain = state.selectedDomain === 'all' || item.domain === state.selectedDomain;
    let matchStatus = true;
    if (state.selectedStatus === 'READY_FOR_REVIEW' || state.selectedStatus === 'SUBMITTED') {
      matchStatus = item.is_match === true;
    } else if (state.selectedStatus === 'REJECTED') {
      matchStatus = item.is_match === false;
    }

    return matchSearch && matchDomain && matchStatus;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');

  tbody.innerHTML = filtered.map(item => {
    const isMatch = item.is_match;
    const badgeClass = isMatch ? 'qual-match' : 'qual-disqualified';
    const badgeText = isMatch ? '✓ QUALIFIED' : '✗ DISQUALIFIED';
    const dateFormatted = item.scanned_at ? new Date(item.scanned_at).toLocaleDateString(undefined, {
      month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    }) : 'Today';

    return `
      <tr>
        <td>
          <span class="qual-badge ${badgeClass}">${badgeText}</span>
        </td>
        <td>
          <div style="font-weight: 700; color: #f1f5f9;">${escapeHtml(item.title)}</div>
          <div style="font-size: 0.75rem; color: #94a3b8;">${escapeHtml(item.company)}</div>
        </td>
        <td><span class="tag-location">${escapeHtml(item.location || 'Remote')}</span></td>
        <td><span class="source-pill">${escapeHtml(item.source || 'Alert')}</span></td>
        <td>
          <div class="reason-text">${escapeHtml(item.reason)}</div>
        </td>
        <td style="font-size: 0.75rem; color: #64748b; white-space: nowrap;">${dateFormatted}</td>
        <td>
          ${isMatch ? `
            <button class="btn btn-outline btn-sm" onclick="openPacketModal('${item.id}')">
              Inspect
            </button>
          ` : `
            <span style="font-size: 0.75rem; color: #64748b;">Filtered Out</span>
          `}
        </td>
      </tr>
    `;
  }).join('');
}

// -------------------------------------------------------------
// Analytics View
// -------------------------------------------------------------
function renderAnalytics() {
  const m = state.metrics;
  const rejectionBox = document.getElementById('rejection-breakdown');
  const domainBox = document.getElementById('domain-breakdown');

  // Rejection reasons
  const reasons = m.disqualification_reasons || {};
  if (Object.keys(reasons).length === 0) {
    rejectionBox.innerHTML = '<div style="color: #64748b;">No disqualification data recorded.</div>';
  } else {
    rejectionBox.innerHTML = Object.entries(reasons).map(([reason, count]) => `
      <div class="breakdown-row">
        <span class="breakdown-key">🛡️ ${escapeHtml(reason)}</span>
        <span class="breakdown-val">${count} jobs filtered</span>
      </div>
    `).join('');
  }

  // Domain breakdown
  const domains = m.by_domain || {};
  if (Object.keys(domains).length === 0) {
    domainBox.innerHTML = '<div style="color: #64748b;">No domain data recorded.</div>';
  } else {
    domainBox.innerHTML = Object.entries(domains).map(([dom, count]) => `
      <div class="breakdown-row">
        <span class="breakdown-key">💻 ${escapeHtml(domainLabels[dom] || dom)}</span>
        <span class="breakdown-val">${count} opportunities</span>
      </div>
    `).join('');
  }
}

// -------------------------------------------------------------
// Modal: Application Packet Inspector
// -------------------------------------------------------------
function openPacketModal(appId) {
  const app = state.applications.find(a => a.id === appId);
  if (!app) return;

  state.currentModalApp = app;

  document.getElementById('modal-job-title').textContent = app.title;
  document.getElementById('modal-company-meta').textContent = `${app.company} • ${app.location} (${app.source || 'Alert'})`;
  document.getElementById('modal-domain-tag').textContent = domainLabels[app.domain] || app.domain;

  // CV Info
  const cvName = app.cv_path ? app.cv_path.split('\\').pop().split('/').pop() : 'Standard CV';
  document.getElementById('modal-cv-filename').textContent = cvName;
  document.getElementById('modal-cv-path').textContent = app.cv_path || 'No path specified';

  // Cover Letter
  document.getElementById('modal-cover-letter').textContent = app.cover_letter || 'No cover letter drafted.';

  // Screening Answers
  const answersBox = document.getElementById('modal-screening-answers');
  const screening = app.screening_answers || {};
  answersBox.innerHTML = Object.entries(screening).map(([k, v]) => `
    <div class="screening-item">
      <div class="screening-key">${escapeHtml(k.replace(/_/g, ' '))}</div>
      <div class="screening-val">${escapeHtml(String(v))}</div>
    </div>
  `).join('');

  // URL
  const urlBtn = document.getElementById('modal-job-url');
  if (app.url) {
    urlBtn.href = app.url;
    urlBtn.classList.remove('hidden');
  } else {
    urlBtn.classList.add('hidden');
  }

  // Status Selector
  document.getElementById('modal-status-select').value = app.status || 'READY_FOR_REVIEW';

  // Show modal
  document.getElementById('modal-packet').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('modal-packet').classList.add('hidden');
  state.currentModalApp = null;
}

function copyCoverLetter() {
  const text = document.getElementById('modal-cover-letter').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('btn-copy-cover');
    const originalText = btn.innerHTML;
    btn.innerHTML = '✓ Copied to Clipboard!';
    setTimeout(() => {
      btn.innerHTML = originalText;
    }, 2000);
  });
}

async function saveModalStatus() {
  if (!state.currentModalApp) return;

  const newStatus = document.getElementById('modal-status-select').value;
  try {
    const res = await fetch('/api/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: state.currentModalApp.id,
        status: newStatus
      })
    });

    if (res.ok) {
      state.currentModalApp.status = newStatus;
      closeModal();
      await loadData();
    } else {
      alert('Failed to update status');
    }
  } catch (err) {
    console.error('Error saving status:', err);
    alert('Network error while updating status');
  }
}

// -------------------------------------------------------------
// Modal: Quick Evaluate Job
// -------------------------------------------------------------
function openEvalModal() {
  document.getElementById('form-evaluate').reset();
  document.getElementById('eval-result-box').classList.add('hidden');
  document.getElementById('modal-evaluate').classList.remove('hidden');
}

function closeEvalModal() {
  document.getElementById('modal-evaluate').classList.add('hidden');
}

async function handleEvaluateSubmit(e) {
  e.preventDefault();

  const title = document.getElementById('eval-title').value.trim();
  const company = document.getElementById('eval-company').value.trim();
  const location = document.getElementById('eval-location').value.trim();
  const source = document.getElementById('eval-source').value.trim() || 'Manual Scan';
  const url = document.getElementById('eval-url').value.trim();
  const description = document.getElementById('eval-description').value.trim();

  const submitBtn = document.getElementById('btn-submit-eval');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Analyzing...';

  try {
    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        company,
        location,
        source,
        url,
        description
      })
    });

    const result = await res.json();
    displayEvalResult(result);
    await loadData();
  } catch (err) {
    console.error('Evaluation error:', err);
    alert('Evaluation request failed');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Scan & Evaluate Opportunity';
  }
}

function displayEvalResult(result) {
  const resultBox = document.getElementById('eval-result-box');
  resultBox.classList.remove('hidden');

  const isMatch = result.is_match;
  const badgeClass = isMatch ? 'qual-match' : 'qual-disqualified';
  const badgeText = isMatch ? '✓ QUALIFIED & DRAFTED' : '✗ DISQUALIFIED BY FILTER';

  resultBox.innerHTML = `
    <div style="margin-bottom: 0.6rem;">
      <span class="qual-badge ${badgeClass}">${badgeText}</span>
    </div>
    <div style="font-size: 0.88rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.25rem;">
      ${escapeHtml(result.reason)}
    </div>
    ${isMatch ? `
      <div style="font-size: 0.78rem; color: #a5b4fc; margin-top: 0.4rem;">
        Domain: <strong>${escapeHtml(domainLabels[result.domain] || result.domain)}</strong>
      </div>
      <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem;">
        Mapped CV: <code>${escapeHtml(result.cv_path ? result.cv_path.split('\\').pop() : 'Standard CV')}</code>
      </div>
      <button class="btn btn-primary btn-sm" style="margin-top: 0.75rem;" onclick="closeEvalModal(); openPacketModal('${result.app_record.id}');">
        View Drafted Packet ↗
      </button>
    ` : `
      <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.4rem;">
        This role was filtered out and logged in the Scanned Audit Trail.
      </div>
    `}
  `;
}

// Utility: escape HTML
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
