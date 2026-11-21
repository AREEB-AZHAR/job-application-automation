// Areeb Azhar — Engineering Career Pipeline Dashboard
let state = {
  metrics: {},
  applications: [],
  scanned: [],
  candidate: {},
  activeTab: 'applications',
  searchQuery: '',
  selectedDomain: 'all',
  selectedStatus: 'all',
  selectedSort: 'time_desc',
  currentDrawerApp: null
};

const domainLabels = {
  full_stack: 'Full-Stack Web',
  rust_blockchain: 'Rust & Blockchain',
  flutter: 'Flutter / Mobile',
  ai_ml: 'AI / Machine Learning',
  game_dev: 'Game Development',
  other: 'General Engineering'
};

document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  loadData();
});

function initEventListeners() {
  // Tabs
  document.querySelectorAll('.seg-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tab = btn.dataset.tab;
      switchTab(tab);
    });
  });

  // Search Input & Keyboard Shortcut
  const searchInput = document.getElementById('input-search');
  searchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value.toLowerCase();
    renderActiveView();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== searchInput && !document.activeElement.matches('input, textarea')) {
      e.preventDefault();
      searchInput.focus();
    } else if (e.key === 'Escape') {
      closeDrawer();
      closeEvalModal();
      closeLightbox();
    }
  });

  // Sort Dropdown
  const sortSelect = document.getElementById('filter-sort');
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      state.selectedSort = e.target.value;
      renderActiveView();
    });
  }

  // Filters
  document.getElementById('filter-domain').addEventListener('change', (e) => {
    state.selectedDomain = e.target.value;
    renderActiveView();
  });

  document.getElementById('filter-status').addEventListener('change', (e) => {
    state.selectedStatus = e.target.value;
    renderActiveView();
  });

  // Refresh
  document.getElementById('btn-refresh').addEventListener('click', loadData);

  // Drawer
  document.getElementById('btn-close-drawer').addEventListener('click', closeDrawer);
  document.getElementById('drawer-packet').addEventListener('click', (e) => {
    if (e.target.id === 'drawer-packet') closeDrawer();
  });

  document.getElementById('btn-copy-cover').addEventListener('click', copyCoverLetter);
  document.getElementById('btn-save-status').addEventListener('click', saveDrawerStatus);

  // Lightbox
  document.getElementById('btn-close-lightbox').addEventListener('click', closeLightbox);
  document.getElementById('modal-lightbox').addEventListener('click', (e) => {
    if (e.target.id === 'modal-lightbox') closeLightbox();
  });

  // Quick Evaluate
  document.getElementById('btn-quick-evaluate').addEventListener('click', openEvalModal);
  document.getElementById('btn-close-eval').addEventListener('click', closeEvalModal);
  document.getElementById('btn-cancel-eval').addEventListener('click', closeEvalModal);
  document.getElementById('modal-evaluate').addEventListener('click', (e) => {
    if (e.target.id === 'modal-evaluate') closeEvalModal();
  });
  document.getElementById('form-evaluate').addEventListener('submit', handleEvaluateSubmit);
}

function resolveProofPath(path) {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) return path;
  
  // Clean relative path
  const cleanPath = path.replace(/^\/+/, '');
  
  // If hosted on GitHub Pages (with repository subpath)
  if (window.location.hostname.includes('github.io')) {
    const segments = window.location.pathname.split('/').filter(Boolean);
    const repoName = segments.length > 0 ? segments[0] : '';
    return repoName ? `/${repoName}/${cleanPath}` : `/${cleanPath}`;
  }
  return `/${cleanPath}`;
}

function formatCardDate(isoStr) {
  if (!isoStr) return 'Today';
  try {
    const d = new Date(isoStr);
    if (isNaN(d.getTime())) return 'Today';
    return d.toLocaleDateString(undefined, {
      month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    });
  } catch (e) {
    return 'Today';
  }
}

async function loadData() {
  try {
    let data = null;

    // 1. Try local server API endpoint first
    try {
      const res = await fetch('/api/data');
      if (res.ok) {
        data = await res.json();
      }
    } catch (e) {
      // Local server offline or running on static hosting
    }

    // 2. Resilient fallback for static hosting / GitHub Pages
    if (!data) {
      const staticCandidates = ['data.json', './data.json', 'api/data.json', './api/data.json'];
      for (const candidate of staticCandidates) {
        try {
          const resStatic = await fetch(candidate);
          if (resStatic.ok) {
            data = await resStatic.json();
            break;
          }
        } catch (err) {
          // try next candidate
        }
      }
    }

    if (!data) throw new Error('Data fetch failed across all local API and static endpoints.');

    state.metrics = data.metrics || {};
    state.applications = data.applications || [];
    state.scanned = data.scanned || [];
    state.candidate = data.candidate || {};

    updateKPIs();
    renderActiveView();
    renderAnalytics();
  } catch (err) {
    console.error('Error fetching data:', err);
  }
}

function formatStatusLabel(status, is_closed, alt_email) {
  if (status === 'TEST_RECORD' || status === 'TEST_DUPLICATE_PRUNED') {
    return '🧪 Test Record';
  } else if (status === 'DISQUALIFIED_DURING_AUDIT') {
    return '🚫 Disqualified';
  } else if (status === 'NO_LONGER_ACCEPTING_APPLICATIONS' || (is_closed && !alt_email)) {
    return '⛔ Closed by Hirer';
  } else if (status === 'APPLIED_VIA_DIRECT_EMAIL' || alt_email) {
    return '✉️ Email Dispatched';
  } else if (status === 'APPLIED' || status === 'SUBMITTED') {
    return '● Applied';
  } else if (status === 'INTERVIEWING') {
    return '● Interviewing';
  } else if (status === 'OFFER') {
    return '★ Offer';
  } else if (status === 'REJECTED') {
    return '× Rejected';
  }
  return status;
}

function updateKPIs() {
  const m = state.metrics;
  const genuineApps = state.applications.filter(a => !a.is_test);
  const appliedCount = genuineApps.filter(a => a.status === 'APPLIED' || a.status === 'SUBMITTED' || a.status === 'APPLIED_VIA_DIRECT_EMAIL').length;
  const closedCount = genuineApps.filter(a => a.status === 'NO_LONGER_ACCEPTING_APPLICATIONS' || a.is_closed).length || m.total_closed || 0;
  const scannedCount = state.scanned.length || m.total_scanned || 0;
  const filteredCount = m.total_disqualified || Math.max(0, scannedCount - appliedCount - closedCount);
  const yieldRate = scannedCount > 0 ? Math.round((appliedCount / scannedCount) * 1000) / 10 : 0;

  document.getElementById('stat-applied').textContent = appliedCount;
  document.getElementById('stat-scanned').textContent = scannedCount;
  document.getElementById('stat-rate').textContent = `${yieldRate}%`;
  document.getElementById('stat-filtered').textContent = filteredCount;
  const closedEl = document.getElementById('stat-closed');
  if (closedEl) closedEl.textContent = closedCount;

  document.getElementById('count-applications').textContent = appliedCount;
  document.getElementById('count-scanned').textContent = scannedCount;
}

function switchTab(tab) {
  state.activeTab = tab;
  document.querySelectorAll('.seg-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.querySelectorAll('.view-panel').forEach(view => {
    view.classList.toggle('active', view.id === `view-${tab}`);
  });
  renderActiveView();
}

function renderActiveView() {
  if (state.activeTab === 'applications') {
    renderApplications();
  } else if (state.activeTab === 'audit') {
    renderAuditTable();
  } else if (state.activeTab === 'analytics') {
    renderAnalytics();
  }
}

// -------------------------------------------------------------
// View: Applications Cards
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
    let matchStatus = true;
    if (state.selectedStatus !== 'all') {
      matchStatus = app.status === state.selectedStatus;
    }

    // Default to genuine live applications only; show test scaffold only when explicitly filtered
    const matchTest = (state.selectedStatus === 'TEST_RECORD' || state.selectedStatus === 'DISQUALIFIED_DURING_AUDIT')
      ? true 
      : !app.is_test;

    return matchSearch && matchDomain && matchStatus && matchTest;
  });

  // Apply sorting
  filtered.sort((a, b) => {
    if (state.selectedSort === 'time_asc') {
      const tA = new Date(a.applied_at || a.created_at || 0).getTime();
      const tB = new Date(b.applied_at || b.created_at || 0).getTime();
      return tA - tB;
    } else if (state.selectedSort === 'company_asc') {
      return (a.company || '').localeCompare(b.company || '');
    } else if (state.selectedSort === 'title_asc') {
      return (a.title || '').localeCompare(b.title || '');
    } else { // default: 'time_desc'
      const tA = new Date(a.applied_at || a.created_at || 0).getTime();
      const tB = new Date(b.applied_at || b.created_at || 0).getTime();
      return tB - tA;
    }
  });

  if (filtered.length === 0) {
    grid.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');

  grid.innerHTML = filtered.map(app => {
    const domainText = domainLabels[app.domain] || app.domain || 'Engineering';
    const cvName = app.cv_path ? app.cv_path.split('\\').pop().split('/').pop() : 'Standard CV';
    const initials = getInitials(app.company || 'CO');
    const status = app.status || 'APPLIED';
    const statusLabel = formatStatusLabel(status, app.is_closed, app.alt_email);
    const dateFormatted = formatCardDate(app.applied_at || app.created_at);

    return `
      <div class="app-card" onclick="openDrawer('${app.id}')" tabindex="0" role="button" aria-label="View application details for ${escapeHtml(app.title)}" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();openDrawer('${app.id}');}">
        <div>
          <div class="app-card-top">
            <div class="company-avatar">${escapeHtml(initials)}</div>
            <div class="app-card-headings">
              <h3 class="app-role-title" title="${escapeHtml(app.title)}">${escapeHtml(app.title)}</h3>
              <div class="app-company-line">
                <span>${escapeHtml(app.company)}</span>
                <span style="color: var(--text-dim);">&bull;</span>
                <span>${escapeHtml(app.location)}</span>
              </div>
            </div>
            <span class="status-chip ${status}">${escapeHtml(statusLabel)}</span>
          </div>

          <div class="app-card-meta">
            <div class="meta-row">
              <span class="tag-badge">${domainText}</span>
              <span class="tag-badge">${escapeHtml(app.source || 'Portal')}</span>
              <span class="tag-badge" style="background: rgba(148, 163, 184, 0.1); color: var(--text-dim); border-color: rgba(148, 163, 184, 0.2);">⏱️ ${dateFormatted}</span>
              ${app.alt_email ? `<span class="tag-badge" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border-color: rgba(56, 189, 248, 0.3);">✉️ ${escapeHtml(app.alt_email)}</span>` : ''}
              ${app.is_closed && !app.alt_email ? `<span class="tag-badge" style="background: rgba(251, 146, 60, 0.15); color: #fb923c; border-color: rgba(251, 146, 60, 0.3);">⛔ Closed</span>` : ''}
            </div>
            <div class="meta-row">
              <span class="cv-tag" title="${escapeHtml(app.cv_path)}">📎 ${escapeHtml(cvName)}</span>
            </div>
          </div>
        </div>

        <div class="app-card-foot">
          <button class="btn btn-secondary btn-sm" onclick="event.stopPropagation(); openDrawer('${app.id}')">
            Inspect Submission
          </button>
          ${app.url ? `
            <a href="${app.url}" target="_blank" rel="noopener noreferrer" class="btn btn-ghost btn-sm" onclick="event.stopPropagation()">
              Open Portal ↗
            </a>
          ` : ''}
        </div>
      </div>
    `;
  }).join('');
}

// -------------------------------------------------------------
// View: Audit Trail
// -------------------------------------------------------------
function renderAuditTable() {
  const tbody = document.getElementById('audit-tbody');
  const empty = document.getElementById('audit-empty');

  const filtered = state.scanned.filter(item => {
    const q = state.searchQuery;
    const matchSearch = !q ||
      (item.title && item.title.toLowerCase().includes(q)) ||
      (item.company && item.company.toLowerCase().includes(q)) ||
      (item.location && item.location.toLowerCase().includes(q)) ||
      (item.reason && item.reason.toLowerCase().includes(q));

    const matchDomain = state.selectedDomain === 'all' || item.domain === state.selectedDomain;
    let matchStatus = true;
    if (state.selectedStatus === 'APPLIED') {
      matchStatus = item.is_match === true;
    } else if (state.selectedStatus === 'REJECTED') {
      matchStatus = item.is_match === false;
    }

    return matchSearch && matchDomain && matchStatus;
  });

  // Apply sorting
  filtered.sort((a, b) => {
    if (state.selectedSort === 'time_asc') {
      const tA = new Date(a.scanned_at || 0).getTime();
      const tB = new Date(b.scanned_at || 0).getTime();
      return tA - tB;
    } else if (state.selectedSort === 'company_asc') {
      return (a.company || '').localeCompare(b.company || '');
    } else if (state.selectedSort === 'title_asc') {
      return (a.title || '').localeCompare(b.title || '');
    } else { // default: 'time_desc'
      const tA = new Date(a.scanned_at || 0).getTime();
      const tB = new Date(b.scanned_at || 0).getTime();
      return tB - tA;
    }
  });

  if (filtered.length === 0) {
    tbody.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');

  tbody.innerHTML = filtered.map(item => {
    const isMatch = item.is_match;
    let badgeText = isMatch ? 'APPLIED' : 'FILTERED';
    let badgeClass = isMatch ? 'APPLIED' : 'REJECTED';
    if (item.is_closed) {
      badgeText = 'CLOSED';
      badgeClass = 'NO_LONGER_ACCEPTING_APPLICATIONS';
    } else if (item.alt_email) {
      badgeText = 'EMAIL';
      badgeClass = 'APPLIED_VIA_DIRECT_EMAIL';
    }

    const dateFormatted = item.scanned_at ? new Date(item.scanned_at).toLocaleDateString(undefined, {
      month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    }) : 'Today';

    const canOpen = Boolean(item.id);

    return `
      <tr ${canOpen ? `onclick="openDrawer('${item.id}')" style="cursor: pointer;"` : ''} tabindex="0" role="button" aria-label="Inspect ${escapeHtml(item.title)}">
        <td>
          <span class="status-chip ${badgeClass}">${badgeText === 'CLOSED' ? '⛔' : '●'} ${badgeText}</span>
        </td>
        <td>
          <div class="table-role-main">${escapeHtml(item.title)}</div>
          <div class="table-company-sub">${escapeHtml(item.company)}</div>
        </td>
        <td><span style="color: var(--text-secondary);">${escapeHtml(item.location || 'Remote')}</span></td>
        <td><span class="tag-badge">${escapeHtml(item.source || 'Alert')}</span></td>
        <td>
          <div class="filter-reason-tag" ${item.is_closed ? 'style="border-left: 2px solid #fb923c;"' : ''}>
            ${item.is_closed ? '⛔ ' : ''}${escapeHtml(item.reason)}
          </div>
        </td>
        <td style="font-size: 0.72rem; color: var(--text-dim); white-space: nowrap; font-family: var(--font-mono);">${dateFormatted}</td>
        <td style="text-align: right;">
          ${canOpen ? `
            <button class="btn btn-secondary btn-xs" onclick="event.stopPropagation(); openDrawer('${item.id}')">
              Details
            </button>
          ` : `
            <span style="font-size: 0.72rem; color: var(--text-dim);">Excluded</span>
          `}
        </td>
      </tr>
    `;
  }).join('');
}

// -------------------------------------------------------------
// View: Analytics & Rules
// -------------------------------------------------------------
function renderAnalytics() {
  const m = state.metrics;
  const rejectionBox = document.getElementById('rejection-breakdown');
  const domainBox = document.getElementById('domain-breakdown');

  const reasons = m.disqualification_reasons || {};
  if (Object.keys(reasons).length === 0) {
    rejectionBox.innerHTML = '<div style="color: var(--text-dim); font-size: 0.78rem;">No exclusion records logged.</div>';
  } else {
    rejectionBox.innerHTML = Object.entries(reasons).map(([reason, count]) => `
      <div class="breakdown-item">
        <span class="breakdown-item-key">${escapeHtml(reason)}</span>
        <span class="breakdown-item-val">${count} roles</span>
      </div>
    `).join('');
  }

  const domains = m.by_domain || {};
  if (Object.keys(domains).length === 0) {
    domainBox.innerHTML = '<div style="color: var(--text-dim); font-size: 0.78rem;">No domain records available.</div>';
  } else {
    domainBox.innerHTML = Object.entries(domains).map(([dom, count]) => `
      <div class="breakdown-item">
        <span class="breakdown-item-key">${escapeHtml(domainLabels[dom] || dom)}</span>
        <span class="breakdown-item-val">${count} applications</span>
      </div>
    `).join('');
  }
}

// -------------------------------------------------------------
// Slide-Over Drawer
// -------------------------------------------------------------
function openDrawer(appId) {
  const app = state.applications.find(a => a.id === appId) || state.scanned.find(s => s.id === appId);
  if (!app) return;

  state.currentDrawerApp = app;

  document.getElementById('drawer-title').textContent = app.title;
  document.getElementById('drawer-company-meta').textContent = `${app.company} • ${app.location} (${app.source || 'Portal'})`;
  document.getElementById('drawer-domain').textContent = domainLabels[app.domain] || app.domain;
  
  const status = app.status || (app.is_match ? 'APPLIED' : 'FILTERED');
  const statusBadge = document.getElementById('drawer-status');
  statusBadge.textContent = status;
  statusBadge.className = `tag-status-badge ${status}`;

  // Verification Proofs & Pre/Post Snapshots
  const verifBanner = document.getElementById('drawer-verif-banner');
  if (app.status === 'APPLIED_VIA_DIRECT_EMAIL' || app.alt_email) {
    verifBanner.className = 'verification-banner info';
    verifBanner.innerHTML = `<span>✉</span> <div><strong>Direct Email Route Prepared:</strong> ${escapeHtml(app.verification_details || `Recruiter email: ${app.alt_email}`)} (Attached: <code style="font-family: var(--font-mono);">${escapeHtml(app.cv_path ? app.cv_path.split('\\').pop() : 'CV.pdf')}</code>)</div>`;
  } else if (app.status === 'NO_LONGER_ACCEPTING_APPLICATIONS' || app.is_closed) {
    verifBanner.className = 'verification-banner error';
    verifBanner.innerHTML = `<span>⛔</span> <div><strong>No Longer Accepting Applications:</strong> ${escapeHtml(app.verification_details || 'Employer disabled Easy Apply / closed job on LinkedIn/ATS')}</div>`;
  } else if (app.verification_status === 'CONFIRMED_SUBMITTED' || app.status === 'APPLIED') {
    verifBanner.className = 'verification-banner success';
    verifBanner.innerHTML = `<span>✓</span> <div><strong>Verified Submitted:</strong> ${escapeHtml(app.verification_details || '200 OK — Success confirmation token verified')} (ID: <code style="font-family: var(--font-mono);">${escapeHtml(app.confirmation_id || 'CONF-OK')}</code>)</div>`;
  } else if (app.verification_status === 'SUBMISSION_ERROR') {
    verifBanner.className = 'verification-banner error';
    verifBanner.innerHTML = `<span>⚠</span> <div><strong>Submission Error Detected:</strong> ${escapeHtml(app.verification_details || 'Form validation failure')}</div>`;
  } else {
    verifBanner.className = 'verification-banner';
    verifBanner.innerHTML = `<span>●</span> <div><strong>Status:</strong> ${escapeHtml(app.status || 'Pending')}</div>`;
  }

  const preImg = document.getElementById('drawer-img-pre');
  const postImg = document.getElementById('drawer-img-post');
  preImg.onerror = () => {
    preImg.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="240" viewBox="0 0 400 240"><rect width="100%" height="100%" fill="%231e293b"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%2364748b" font-family="sans-serif" font-size="14">No pre-submit image captured</text></svg>';
  };
  postImg.onerror = () => {
    postImg.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="240" viewBox="0 0 400 240"><rect width="100%" height="100%" fill="%231e293b"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%2364748b" font-family="sans-serif" font-size="14">No post-submit receipt captured</text></svg>';
  };
  preImg.src = resolveProofPath(app.pre_submit_snapshot || `/proofs/${app.id}/pre_submit.png`);
  postImg.src = resolveProofPath(app.post_submit_snapshot || `/proofs/${app.id}/post_submit.png`);

  const cvName = app.cv_path ? app.cv_path.split('\\').pop().split('/').pop() : 'Standard Resume';
  document.getElementById('drawer-cv-name').textContent = cvName;
  document.getElementById('drawer-cv-path').textContent = app.cv_path || 'No path specified';

  document.getElementById('drawer-cover-letter').textContent = app.cover_letter || 'Direct application submission packet.';

  const screeningBox = document.getElementById('drawer-screening');
  const screening = app.screening_answers || {};
  if (Object.keys(screening).length === 0) {
    screeningBox.innerHTML = '<div style="color: var(--text-dim); font-size: 0.75rem;">Standard candidate screening profile applied.</div>';
  } else {
    screeningBox.innerHTML = Object.entries(screening).map(([k, v]) => `
      <div class="screening-cell">
        <div class="screening-cell-label">${escapeHtml(k.replace(/_/g, ' '))}</div>
        <div class="screening-cell-val">${escapeHtml(String(v))}</div>
      </div>
    `).join('');
  }

  const urlAnchor = document.getElementById('drawer-job-url');
  if (app.url) {
    urlAnchor.href = app.url;
    urlAnchor.parentElement.classList.remove('hidden');
  } else {
    urlAnchor.parentElement.classList.add('hidden');
  }

  document.getElementById('drawer-status-select').value = app.status || 'APPLIED';
  document.getElementById('drawer-packet').classList.remove('hidden');
}

function closeDrawer() {
  document.getElementById('drawer-packet').classList.add('hidden');
  state.currentDrawerApp = null;
}

function copyCoverLetter() {
  const text = document.getElementById('drawer-cover-letter').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('btn-copy-cover');
    const original = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(() => {
      btn.textContent = original;
    }, 1800);
  });
}

function openLightbox(type) {
  if (!state.currentDrawerApp) return;
  const img = document.getElementById('lightbox-img');
  const title = document.getElementById('lightbox-title');
  const badge = document.getElementById('lightbox-badge');

  const prePath = resolveProofPath(state.currentDrawerApp.pre_submit_snapshot || `/proofs/${state.currentDrawerApp.id}/pre_submit.png`);
  const postPath = resolveProofPath(state.currentDrawerApp.post_submit_snapshot || `/proofs/${state.currentDrawerApp.id}/post_submit.png`);

  img.onerror = () => {
    img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="360" viewBox="0 0 600 360"><rect width="100%" height="100%" fill="%231e293b"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%2364748b" font-family="sans-serif" font-size="16">No visual proof image captured</text></svg>';
  };

  if (type === 'pre') {
    img.src = prePath;
    title.textContent = `Pre-Submission Form Snapshot — ${state.currentDrawerApp.title} @ ${state.currentDrawerApp.company}`;
    badge.textContent = "Pre-Submit Audit";
  } else {
    img.src = postPath;
    title.textContent = `Post-Submission Confirmation Receipt — ${state.currentDrawerApp.title} @ ${state.currentDrawerApp.company}`;
    badge.textContent = "Submission Receipt";
  }
  document.getElementById('modal-lightbox').classList.remove('hidden');
}

function closeLightbox() {
  document.getElementById('modal-lightbox').classList.add('hidden');
}

async function saveDrawerStatus() {
  if (!state.currentDrawerApp) return;

  const newStatus = document.getElementById('drawer-status-select').value;
  try {
    const res = await fetch('/api/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: state.currentDrawerApp.id,
        status: newStatus
      })
    });

    if (res.ok) {
      state.currentDrawerApp.status = newStatus;
      closeDrawer();
      await loadData();
    }
  } catch (err) {
    console.error('Error saving status:', err);
  }
}

// -------------------------------------------------------------
// Quick Evaluate Modal
// -------------------------------------------------------------
function openEvalModal() {
  document.getElementById('form-evaluate').reset();
  document.getElementById('eval-result-card').classList.add('hidden');
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
  const source = document.getElementById('eval-source').value.trim() || 'Direct';
  const url = document.getElementById('eval-url').value.trim();
  const description = document.getElementById('eval-description').value.trim();

  const submitBtn = document.getElementById('btn-submit-eval');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Processing...';

  try {
    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, company, location, source, url, description })
    });

    const result = await res.json();
    displayEvalResult(result);
    await loadData();
  } catch (err) {
    console.error('Evaluation failed:', err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Process & Apply';
  }
}

function displayEvalResult(result) {
  const card = document.getElementById('eval-result-card');
  card.classList.remove('hidden');

  const isMatch = result.is_match;
  const statusBadge = isMatch ? 'status-chip APPLIED' : 'status-chip REJECTED';
  const statusLabel = isMatch ? '● APPLIED' : '● FILTERED';

  card.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
      <span class="${statusBadge}">${statusLabel}</span>
      <span style="font-size: 0.72rem; color: var(--text-tertiary);">${escapeHtml(domainLabels[result.domain] || '')}</span>
    </div>
    <div style="font-size: 0.82rem; font-weight: 500; color: var(--text-primary); margin-bottom: 0.35rem;">
      ${escapeHtml(result.reason)}
    </div>
    ${isMatch ? `
      <div style="font-size: 0.72rem; color: var(--text-secondary); margin-top: 0.35rem;">
        Attached CV: <code>${escapeHtml(result.cv_path ? result.cv_path.split('\\').pop() : 'Standard CV')}</code>
      </div>
      <button class="btn btn-secondary btn-xs" style="margin-top: 0.65rem;" onclick="closeEvalModal(); openDrawer('${result.app_record.id}');">
        View Submission Details ↗
      </button>
    ` : ''}
  `;
}

// Utility Helpers
function getInitials(name) {
  if (!name) return 'CO';
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
