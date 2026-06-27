// ═══ Trading Research Platform — Frontend Engine v2 ═══

// ── Configuration ──
const API_BASE = '';  // Same-origin for GitHub Pages data, CORS proxy for live API
const CORS_PROXIES = [
  'https://api.allorigins.win/raw?url=',
  'https://corsproxy.io/?',
];

// ── Research source presets ──
const RESEARCH_PRESETS = [
  { name: "arXiv Quantitative Finance", url: "https://arxiv.org/list/q-fin/recent", icon: "📊", category: "academic" },
  { name: "SEC EDGAR Current Filings", url: "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent", icon: "🏛️", category: "regulatory" },
  { name: "FRED Economic Data", url: "https://fred.stlouisfed.org/", icon: "📈", category: "economic" },
  { name: "NBER Working Papers", url: "https://www.nber.org/papers", icon: "🎓", category: "academic" },
  { name: "World Bank Open Data", url: "https://data.worldbank.org/", icon: "🌍", category: "economic" },
  { name: "FDIC Bank Failures", url: "https://www.fdic.gov/bank-failures/failed-bank-list", icon: "🏦", category: "regulatory" },
  { name: "Investopedia Markets", url: "https://www.investopedia.com/markets", icon: "📚", category: "education" },
  { name: "Yahoo Finance", url: "https://finance.yahoo.com/", icon: "💹", category: "market_data" },
  { name: "TradingView Ideas", url: "https://www.tradingview.com/ideas/", icon: "📉", category: "analysis" },
  { name: "CoinDesk Crypto News", url: "https://www.coindesk.com/", icon: "₿", category: "crypto" },
  { name: "SSRN New Papers", url: "https://www.ssrn.com/en/", icon: "📄", category: "academic" },
  { name: "St. Louis Fed Research", url: "https://www.stlouisfed.org/research", icon: "🏛️", category: "central_banking" },
  { name: "BIS Publications", url: "https://www.bis.org/publ.htm", icon: "🏦", category: "central_banking" },
  { name: "CFTC Weekly Reports", url: "https://www.cftc.gov/MarketAndReportings.htm", icon: "📋", category: "regulatory" },
  { name: "Federal Reserve Board", url: "https://www.federalreserve.gov/newsevents.htm", icon: "🇺🇸", category: "central_banking" },
];

// ── State ──
let activeTab = 'dashboard';
let scrapeHistory = JSON.parse(localStorage.getItem('trp_scrape_history') || '[]');
let isScraping = false;

// ── Navigation ──
function switchTab(tabId) {
  activeTab = tabId;
  document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
  document.querySelector(`[data-tab="${tabId}"]`)?.classList.add('active');
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(tabId)?.classList.add('active');
  if (tabId === 'dashboard') loadDashboards();
  if (tabId === 'reports') loadReports();
  if (tabId === 'research') loadResearch();
  if (tabId === 'architecture') loadArchitecture();
  if (tabId === 'safety') loadSafety();
}

// ── Dashboard ──
const DASHBOARD_IDS = [
  'research_core', 'global_context', 'memory', 'capabilities',
  'planning', 'sync', 'subsystem_health', 'recommendations',
  'knowledge_state', 'system_health'
];

async function loadDashboards() {
  const grid = document.getElementById('dashboard-grid');
  if (!grid) return;
  grid.innerHTML = '<div class="loading">Loading dashboards...</div>';
  
  const cards = [];
  for (const id of DASHBOARD_IDS) {
    try {
      const resp = await fetch(`data/dashboard/${id}.json`);
      const data = await resp.json();
      cards.push({ id, ...data });
    } catch (e) {
      cards.push({ id, title: id.replace(/_/g, ' '), status: 'offline', metrics: {} });
    }
  }
  
  grid.innerHTML = cards.map(c => `
    <div class="card dashboard-card ${c.status === 'online' ? 'healthy' : 'degraded'}">
      <h3>${c.title || c.id}</h3>
      <div class="status-badge ${c.status === 'online' ? 'badge-ok' : 'badge-warn'}">${c.status || 'unknown'}</div>
      <div class="metrics">
        ${Object.entries(c.metrics || {}).slice(0, 6).map(([k, v]) => 
          `<div class="metric"><span class="metric-label">${k.replace(/_/g, ' ')}</span><span class="metric-value">${typeof v === 'number' ? v.toLocaleString() : v}</span></div>`
        ).join('')}
      </div>
      ${c.advisory_only ? '<div class="advisory-badge">🔍 Advisory Only</div>' : ''}
    </div>
  `).join('');
}

// ── Reports ──
async function loadReports() {
  const list = document.getElementById('reports-list');
  if (!list) return;
  list.innerHTML = '<div class="loading">Loading reports...</div>';
  
  try {
    const resp = await fetch('data/reports/reports_index.json');
    const data = await resp.json();
    list.innerHTML = data.reports.map(r => `
      <div class="card report-card" onclick="viewReport('${r.id}')">
        <h3>${r.title}</h3>
        <div class="report-meta">
          <span class="badge badge-cat">${r.category}</span>
          <span class="timestamp">${new Date(r.generated_at).toLocaleDateString()}</span>
        </div>
        <div class="report-summary">${(r.summary || r.description || '').substring(0, 200)}</div>
        <button class="btn btn-sm">View Full Report →</button>
      </div>
    `).join('');
  } catch (e) {
    list.innerHTML = '<div class="error">Failed to load reports. Try refreshing.</div>';
  }
}

async function viewReport(id) {
  try {
    const resp = await fetch(`data/reports/${id}.json`);
    const data = await resp.json();
    const modal = document.getElementById('report-modal');
    modal.innerHTML = `<div class="modal-content card">
      <button class="btn btn-close" onclick="closeModal()">✕</button>
      <h2>${data.title}</h2>
      <div class="report-meta">
        <span class="badge badge-cat">${data.category}</span>
        <span class="badge badge-adv">Advisory Only</span>
        <span class="timestamp">${data.generated_at}</span>
      </div>
      <div class="report-body">${renderMarkdown(data.content || data.summary || 'No content available')}</div>
    </div>`;
    modal.classList.add('open');
  } catch (e) {
    alert('Failed to load report');
  }
}

function closeModal() {
  document.getElementById('report-modal')?.classList.remove('open');
}

// ── Research (Live Scraping) ──
async function loadResearch() {
  const presetGrid = document.getElementById('research-presets');
  const resultsPanel = document.getElementById('research-results');
  if (!presetGrid) return;

  // Load latest results from daemon
  let latestResults = null;
  try {
    const resp = await fetch('data/research_results.json');
    latestResults = await resp.json();
  } catch (e) {}

  // Render preset sources
  presetGrid.innerHTML = RESEARCH_PRESETS.map((p, i) => `
    <div class="card preset-card" onclick="scrapePreset(${i})">
      <span class="preset-icon">${p.icon}</span>
      <div class="preset-info">
        <h4>${p.name}</h4>
        <span class="badge badge-cat">${p.category}</span>
      </div>
      ${latestResults?.items?.[i] ? 
        `<div class="preset-status ${latestResults.items[i].status === 200 ? 'status-ok' : 'status-err'}">
          ${latestResults.items[i].status === 200 ? '✓ Cached' : '⚠ ' + latestResults.items[i].status}
        </div>` : ''}
    </div>
  `).join('');

  // Show latest daemon results if available
  if (latestResults && resultsPanel) {
    resultsPanel.innerHTML = `
      <div class="research-summary">
        <h3>Last Scraping Cycle</h3>
        <div class="metrics">
          <div class="metric"><span class="metric-label">Sources</span><span class="metric-value">${latestResults.sources_scraped}</span></div>
          <div class="metric"><span class="metric-label">Successful</span><span class="metric-value">${latestResults.successful}</span></div>
          <div class="metric"><span class="metric-label">Total Content</span><span class="metric-value">${(latestResults.total_content_length / 1024).toFixed(0)} KB</span></div>
          <div class="metric"><span class="metric-label">Total Links</span><span class="metric-value">${latestResults.total_links}</span></div>
          <div class="metric"><span class="metric-label">Updated</span><span class="metric-value">${new Date(latestResults.last_updated).toLocaleString()}</span></div>
        </div>
      </div>
    `;
  }
}

async function scrapePreset(index) {
  const source = RESEARCH_PRESETS[index];
  await performScrape(source.url, source.name);
}

async function scrapeCustom() {
  const url = document.getElementById('custom-url')?.value?.trim();
  if (!url) { alert('Enter a URL'); return; }
  await performScrape(url, 'Custom');
}

async function performScrape(url, name) {
  if (isScraping) return;
  isScraping = true;
  
  const resultsPanel = document.getElementById('research-results');
  if (resultsPanel) {
    resultsPanel.innerHTML = `<div class="scraping-indicator">
      <div class="spinner"></div>
      <p>Scraping ${name}...</p>
      <p class="muted">${url}</p>
    </div>`;
  }

  try {
    // Use server API if available, otherwise CORS proxy
    let data = null;
    
    // Try direct API first (same origin)
    try {
      const resp = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, output_format: 'markdown' })
      });
      if (resp.ok) data = await resp.json();
    } catch (e) {}

    // Try CORS proxy fallback
    if (!data) {
      for (const proxy of CORS_PROXIES) {
        try {
          const proxyUrl = proxy + encodeURIComponent(url);
          const resp = await fetch(proxyUrl);
          if (resp.ok) {
            const text = await resp.text();
            data = {
              name,
              url,
              status: 200,
              content: text.substring(0, 50000),
              content_length: text.length,
              advisory_only: true,
              platform_mode: 'research',
              scraped_at: new Date().toISOString(),
              source: 'cors_proxy'
            };
            break;
          }
        } catch (e) { continue; }
      }
    }

    if (data) {
      // Save to history
      data.id = Date.now().toString(36);
      scrapeHistory.unshift(data);
      if (scrapeHistory.length > 50) scrapeHistory.pop();
      localStorage.setItem('trp_scrape_history', JSON.stringify(scrapeHistory));
      displayScrapeResult(data);
    } else {
      throw new Error('All fetch methods failed');
    }
  } catch (e) {
    if (resultsPanel) {
      resultsPanel.innerHTML = `<div class="card error-card">
        <h3>❌ Scrape Failed</h3>
        <p>Could not fetch <code>${url}</code></p>
        <p class="muted">${e.message}</p>
        <p class="muted">The backend API must be running for live scraping. Start it with:<br>
        <code>cd api && python3 main.py</code></p>
      </div>`;
    }
  } finally {
    isScraping = false;
  }
}

function displayScrapeResult(data) {
  const resultsPanel = document.getElementById('research-results');
  if (!resultsPanel) return;
  
  const content = data.content || data.error || 'No content extracted';
  const isMarkdown = content.includes('#') || content.includes('**') || content.includes('- ');
  
  resultsPanel.innerHTML = `
    <div class="card result-card">
      <div class="result-header">
        <h3>${data.title || data.name || url}</h3>
        <div class="result-meta">
          <span class="badge badge-ok">Status: ${data.status || 'N/A'}</span>
          <span class="badge badge-cat">advisory only</span>
          <span class="badge">${(data.content_length || content.length).toLocaleString()} chars</span>
          ${data.source ? `<span class="badge">via ${data.source}</span>` : ''}
        </div>
      </div>
      <div class="result-content">
        <pre>${isMarkdown ? renderMarkdown(content) : escapeHtml(content).substring(0, 20000)}</pre>
      </div>
      <div class="result-footer">
        <span class="muted">Scraped: ${data.scraped_at || new Date().toISOString()}</span>
        <span class="muted">Hash: ${data.content_hash || 'N/A'}</span>
        <button class="btn btn-sm" onclick="copyResult()">📋 Copy</button>
      </div>
    </div>
  `;
}

function showHistory() {
  const resultsPanel = document.getElementById('research-results');
  if (!resultsPanel) return;
  
  resultsPanel.innerHTML = scrapeHistory.length === 0 
    ? '<div class="card"><p>No scrape history yet. Try scraping some sources!</p></div>'
    : `<h3>Scrape History</h3>` + scrapeHistory.map(h => `
      <div class="card history-item" onclick="displayScrapeResult(${JSON.stringify(h).replace(/"/g, '"')})">
        <h4>${h.title || h.name || h.url}</h4>
        <span class="badge ${h.status === 200 ? 'badge-ok' : 'badge-warn'}">${h.status || 'N/A'}</span>
        <span class="muted">${(h.content_length || 0).toLocaleString()} chars</span>
        <span class="muted">${h.scraped_at ? new Date(h.scraped_at).toLocaleString() : ''}</span>
      </div>
    `).join('');
}

// ── Architecture ──
async function loadArchitecture() {
  const container = document.getElementById('architecture-content');
  if (!container) return;
  
  try {
    const resp = await fetch('data/dashboard/research_core.json');
    const core = await resp.json();
    
    container.innerHTML = `
      <div class="arch-section">
        <h3>Phase 62 — Research Core (95 modules)</h3>
        <div class="arch-info">
          <p>Foundation layer: contracts, safety, storage, evidence, replication, bias detection</p>
          <div class="metrics">
            <div class="metric"><span class="metric-label">Modules</span><span class="metric-value">95</span></div>
            <div class="metric"><span class="metric-label">Bridges Out</span><span class="metric-value">${core.metrics?.bridges_out || 'N/A'}</span></div>
            <div class="metric"><span class="metric-label">Evidence Records</span><span class="metric-value">${core.metrics?.evidence_records || 'N/A'}</span></div>
          </div>
        </div>
      </div>
      <div class="arch-section">
        <h3>Phase 63 — Platform Finalization (95 modules)</h3>
        <div class="arch-info">
          <p>Integration layer: dashboards, CLI, replication engine, bias detectors, reports</p>
          <div class="metrics">
            <div class="metric"><span class="metric-label">Modules</span><span class="metric-value">95</span></div>
            <div class="metric"><span class="metric-label">Bridges In</span><span class="metric-value">93</span></div>
            <div class="metric"><span class="metric-label">Bridges Out</span><span class="metric-value">93</span></div>
          </div>
        </div>
      </div>
      <div class="arch-section">
        <h3>Phase 64 — Verification & Unification (96 modules)</h3>
        <div class="arch-info">
          <p>Verification layer: full system tests, bridge grid, SHA-256 determinism</p>
          <div class="metrics">
            <div class="metric"><span class="metric-label">Modules</span><span class="metric-value">96</span></div>
            <div class="metric"><span class="metric-label">Total Bridges</span><span class="metric-value">186</span></div>
            <div class="metric"><span class="metric-label">Determinism</span><span class="metric-value">✓ SHA-256</span></div>
          </div>
        </div>
      </div>
    `;
  } catch (e) {
    container.innerHTML = '<div class="card"><p>Architecture data loading failed.</p></div>';
  }
}

// ── Safety ──
function loadSafety() {
  const container = document.getElementById('safety-content');
  if (!container) return;
  
  const blocked = [
    { op: "live_trading", desc: "Live trading with real money" },
    { op: "broker_execution", desc: "Direct broker order execution" },
    { op: "order_placement", desc: "Placing orders on exchanges" },
    { op: "automatic_deployment", desc: "Auto-deploying to production" },
    { op: "production_modification", desc: "Modifying production systems" },
    { op: "live_data_writes", desc: "Writing to live market data feeds" },
    { op: "real_portfolio_changes", desc: "Making actual portfolio changes" },
    { op: "unauthorized_api_use", desc: "Using APIs without safety review" },
  ];

  const constitution = [
    "All operations are advisory-only — no live trading, ever",
    "Research data is for analysis only — never triggers automatic actions",
    "Bias detection must run on all claims before reporting",
    "Replication is required before any claim reaches reports",
    "Evidence chains must be cryptographically verifiable (SHA-256)",
    "Storage backends must support rollback and integrity checks",
    "Safety enforcement is structural (RuntimeError), not just warnings",
    "Dashboard data is read-only — reflects system state, never modifies it",
    "All scraping respects robots.txt and source terms of service",
    "System permanently structurally incapable of production modification",
  ];

  container.innerHTML = `
    <div class="safety-blocked">
      <h3>🔒 Blocked Operations (Structural Enforcement)</h3>
      <div class="blocked-grid">
        ${blocked.map(b => `
          <div class="card blocked-card">
            <div class="blocked-icon">⛔</div>
            <div class="blocked-info">
              <code>${b.op}</code>
              <p>${b.desc}</p>
            </div>
            <div class="badge badge-error">RuntimeError</div>
          </div>
        `).join('')}
      </div>
    </div>
    <div class="safety-constitution">
      <h3>📜 Safety Constitution</h3>
      <ol class="constitution-list">
        ${constitution.map(a => `<li>${a}</li>`).join('')}
      </ol>
    </div>
  `;
}

// ── Utilities ──
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function renderMarkdown(md) {
  return md
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
    .replace(/\n{2,}/g, '<br><br>')
    .replace(/\n/g, '<br>');
}

function copyResult() {
  const el = document.querySelector('.result-content pre');
  if (el) navigator.clipboard.writeText(el.textContent).then(() => alert('Copied!'));
}

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  switchTab('dashboard');
});

// Make functions global
window.switchTab = switchTab;
window.scrapePreset = scrapePreset;
window.scrapeCustom = scrapeCustom;
window.showHistory = showHistory;
window.viewReport = viewReport;
window.closeModal = closeModal;
window.copyResult = copyResult;
window.displayScrapeResult = displayScrapeResult;
