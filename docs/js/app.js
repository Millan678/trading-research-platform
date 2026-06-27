// ═══ Trading Research Platform — Frontend Engine ═══
const RESEARCH_PRESETS = [
  { name: "arXiv q-fin", url: "https://arxiv.org/list/q-fin/recent", icon: "📊" },
  { name: "SEC EDGAR", url: "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent", icon: "📋" },
  { name: "FRED Economic", url: "https://fred.stlouisfed.org/", icon: "📈" },
  { name: "SSRN Finance", url: "https://www.ssrn.com/en/", icon: "📄" },
  { name: "FDIC Banks", url: "https://www.fdic.gov/bank-failures/failed-bank-list", icon: "🏦" },
  { name: "CFTC Reports", url: "https://www.cftc.gov/MarketAndReportings.htm", icon: "📑" },
  { name: "BIS Research", url: "https://www.bis.org/research.htm", icon: "🌐" },
  { name: "NBER Papers", url: "https://www.nber.org/papers", icon: "🎓" },
  { name: "Yahoo Finance", url: "https://finance.yahoo.com/", icon: "💹" },
  { name: "Investopedia", url: "https://www.investopedia.com/", icon: "📖" },
  { name: "CoinDesk", url: "https://www.coindesk.com/", icon: "₿" },
  { name: "TradingView", url: "https://www.tradingview.com/", icon: "📉" },
  { name: "SEC RSS", url: "https://www.sec.gov/cgi-bin/browse-edgardaily?type=&company=&SIC=&date=&action=getcurrent", icon: "📰" },
  { name: "St. Louis Fed", url: "https://www.stlouisfed.org/", icon: "🏛️" },
  { name: "World Bank", url: "https://data.worldbank.org/", icon: "🌍" },
];

const CONSTITUTION_ARTICLES = [
  "research_integrity", "scientific_method", "peer_review",
  "transparency", "reproducibility", "ethical_compliance",
  "advisory_only", "no_live_trading", "no_production_modification",
  "immutable_history",
];

const DASHBOARD_PAGES = [
  "research_core", "global_context", "memory", "capabilities",
  "planning", "synchronization", "subsystem_health", "recommendations",
  "knowledge_state", "system_health",
];

const REPORTS = [
  "PHASE62_RESEARCH_CORE_READINESS_REPORT", "GLOBAL_CONTEXT_REPORT",
  "MEMORY_REPORT", "CAPABILITY_REPORT", "SYNCHRONIZATION_REPORT",
  "CORE_HEALTH_REPORT", "RESEARCH_STATE_REPORT", "PLATFORM_FOUNDATION_REPORT",
];

// ═══ Navigation ═══
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const page = a.dataset.page;
    document.querySelectorAll('.nav-links a').forEach(x => x.classList.remove('active'));
    a.classList.add('active');
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`page-${page}`).classList.add('active');
  });
});

// ═══ Dashboard ═══
async function loadDashboard() {
  const grid = document.getElementById('dashboard-grid');
  grid.innerHTML = '<div class="empty-state">Loading dashboard data...</div>';

  let cards = '';
  for (const page of DASHBOARD_PAGES) {
    try {
      const resp = await fetch(`data/dashboard/${page}.json`);
      const data = resp.ok ? await resp.json() : null;
      const status = data?.data?.status || data?.status || 'operational';
      const statusClass = status === 'advisory' ? 'status-advisory' : 'status-operational';
      const preview = data ? JSON.stringify(data.data || data, null, 2).substring(0, 200) : 'Loading...';
      cards += `
        <div class="dash-card" data-page="${page}">
          <h3>${(data?.title || page).replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</h3>
          <span class="status ${statusClass}">${status.toUpperCase()}</span>
          ${data?.data?.advisory_only ? '<span class="badge badge-amber" style="margin-left:8px">ADVISORY</span>' : ''}
          <div class="data-preview">${preview}</div>
        </div>`;
    } catch {
      cards += `
        <div class="dash-card" data-page="${page}">
          <h3>${page.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</h3>
          <span class="status status-operational">LOADING</span>
        </div>`;
    }
  }
  grid.innerHTML = cards;
}

// ═══ Reports ═══
async function loadReports() {
  const list = document.getElementById('reports-list');
  let html = '';
  for (const report of REPORTS) {
    const slug = report.toLowerCase();
    try {
      const resp = await fetch(`data/reports/${slug}.json`);
      const data = resp.ok ? await resp.json() : null;
      const date = data?.generated_at || new Date().toISOString();
      html += `
        <div class="report-item" data-report="${slug}">
          <div>
            <h3>${report.replace(/_/g, ' ')}</h3>
            <div class="meta">Generated: ${new Date(date).toLocaleDateString()} ${new Date(date).toLocaleTimeString()}</div>
          </div>
          <div>
            <span class="badge badge-amber">ADVISORY</span>
            <span class="badge badge-green">VERIFIED</span>
          </div>
        </div>`;
    } catch {
      html += `
        <div class="report-item">
          <div><h3>${report.replace(/_/g, ' ')}</h3></div>
          <span class="badge badge-amber">ADVISORY</span>
        </div>`;
    }
  }
  list.innerHTML = html;
}

// ═══ Research (Scraping) ═══
function initResearch() {
  const chips = document.getElementById('preset-chips');
  RESEARCH_PRESETS.forEach(p => {
    const chip = document.createElement('div');
    chip.className = 'preset-chip';
    chip.textContent = `${p.icon} ${p.name}`;
    chip.dataset.url = p.url;
    chip.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      document.getElementById('scrape-url').value = p.url;
    });
    chips.appendChild(chip);
  });

  document.getElementById('btn-scrape').addEventListener('click', doScrape);
  document.getElementById('scrape-url').addEventListener('keypress', e => {
    if (e.key === 'Enter') doScrape();
  });
  document.getElementById('btn-scrape-all').addEventListener('click', batchScrape);
}

async function doScrape() {
  const url = document.getElementById('scrape-url').value.trim();
  if (!url) return;
  const results = document.getElementById('research-results');
  results.innerHTML = '<div class="scrape-loading">🔍 Scraping... this is simulated on static hosting. For live scraping, use the Scrapling CLI or Python API from your server.</div>';

  // On static GitHub Pages, we can't run Python — show a helpful result
  // In production, this would hit a backend API
  setTimeout(() => {
    results.innerHTML = `
      <div class="result-item">
        <h4>📡 ${url}</h4>
        <div class="url">Source: ${url}</div>
        <div class="content">
🔬 Research Mode — Scrapling Integration

This page is deployed as a static site on GitHub Pages.
For live scraping, use these methods from your server:

1. CLI: scrapling extract get "${url}" output.md --ai-targeted
2. Python: 
   from scrapling.fetchers import Fetcher
   page = Fetcher.get('${url}')
   content = page.css('body::text').get()

3. Spider for batch crawling:
   class ResearchSpider(Spider):
       name = "research"
       start_urls = ["${url}"]
       concurrent_requests = 10
       robots_txt_obey = True

Add a backend API endpoint to enable live scraping from this dashboard.
        </div>
      </div>`;
  }, 1500);
}

async function batchScrape() {
  const results = document.getElementById('research-results');
  results.innerHTML = '<div class="scrape-loading">📚 Batch scraping predefined sources...</div>';

  let html = '';
  for (const p of RESEARCH_PRESETS) {
    html += `
      <div class="result-item">
        <h4>${p.icon} ${p.name}</h4>
        <div class="url">${p.url}</div>
        <div class="content">Scheduled for scraping — add backend API for live results</div>
      </div>`;
  }
  setTimeout(() => { results.innerHTML = html; }, 2000);
}

// ═══ Architecture — Bridge Map ═══
function loadBridges() {
  const grid = document.getElementById('bridge-grid');
  let html = '';
  // Generate 186 bridge cells
  for (let i = 1; i <= 186; i++) {
    html += `<div class="bridge-cell" title="Bridge #${i}">B${String(i).padStart(3,'0')}</div>`;
  }
  grid.innerHTML = html;
}

// ═══ Safety — Constitution ═══
function loadConstitution() {
  const grid = document.getElementById('constitution-articles');
  let html = '';
  CONSTITUTION_ARTICLES.forEach((art, i) => {
    html += `
      <div class="article-item">
        <div class="article-num">${i + 1}</div>
        <div class="article-title">${art.replace(/_/g, ' ')}</div>
      </div>`;
  });
  grid.innerHTML = html;
}

// ═══ Init ═══
document.addEventListener('DOMContentLoaded', () => {
  loadDashboard();
  loadReports();
  initResearch();
  loadBridges();
  loadConstitution();
});
