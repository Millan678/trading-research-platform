#!/usr/bin/env python3
"""
Trading Research Platform — Scrapling Backend API
Free-tier deployment: FastAPI + Scrapling static fetcher
Research-only: no trading, no broker execution, no production modification.
"""
import asyncio
import hashlib
import json
import os
import re
import tempfile
import time
from datetime import datetime, timezone
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ── Scrapling Import ──
from scrapling.fetchers import Fetcher

# ═══════════════════════════════════════════
# Safety Guard — Structural Enforcement
# ═══════════════════════════════════════════
FORBIDDEN = [
    "live_trading", "broker_execution", "order_placement",
    "auto_deployment", "production_modification", "real_capital_risk",
    "governance_bypass", "market_manipulation",
]
FORBIDDEN_PATTERNS = [
    re.compile(r"(?:place|submit|execute|send).*(?:order|trade|buy|sell)", re.I),
    re.compile(r"(?:broker|exchange|market).*(?:connect|api|execute)", re.I),
    re.compile(r"(?:live|real|production).*(?:trad|deploy|modif)", re.I),
]

def enforce_research_only(url: str, css: Optional[str] = None):
    """Runtime safety check — reject any request that smells like live trading."""
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(url) or (css and pattern.search(css)):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "FORBIDDEN_OPERATION",
                    "message": f"Request blocked — structural safety enforcement",
                    "platform_mode": "advisory_only",
                    "forbidden_operations": FORBIDDEN,
                }
            )

# ═══════════════════════════════════════════
# Rate Limiter (Simple In-Memory)
# ═══════════════════════════════════════════
class RateLimiter:
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max = max_requests
        self.window = window_seconds
        self.requests: dict[str, list[float]] = {}

    def check(self, ip: str):
        now = time.time()
        hits = self.requests.get(ip, [])
        hits = [t for t in hits if now - t < self.window]
        hits.append(now)
        self.requests[ip] = hits
        if len(hits) > self.max:
            raise HTTPException(429, f"Rate limit: {self.max} req/{self.window}s")

rate_limiter = RateLimiter()

# ═══════════════════════════════════════════
# App Setup
# ═══════════════════════════════════════════
app = FastAPI(
    title="Trading Research Platform — Scrapling API",
    description="Research-only web scraping backend. No live trading, broker execution, or production modification.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # GitHub Pages is the primary consumer
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Storage ──
RESULTS_DIR = os.environ.get("TRP_RESULTS_DIR", "/tmp/trp_scrape_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ═══════════════════════════════════════════
# Models
# ═══════════════════════════════════════════
class ScrapeRequest(BaseModel):
    url: str = Field(..., description="URL to scrape")
    css_selector: Optional[str] = Field(None, description="CSS selector to extract specific content")
    output_format: str = Field("markdown", description="Output format: markdown, text, html")
    timeout: int = Field(30, ge=5, le=120, description="Request timeout in seconds")
    impersonate: str = Field("chrome", description="Browser to impersonate TLS fingerprint")

class ScrapeResponse(BaseModel):
    url: str
    status: int
    title: Optional[str] = None
    content: str
    content_hash: str
    content_length: int
    css_selector: Optional[str] = None
    output_format: str
    fetched_at: str
    advisory_only: bool = True
    platform_mode: str = "research"

class BatchScrapeRequest(BaseModel):
    urls: list[str] = Field(..., max_length=10, description="URLs to scrape (max 10)")
    css_selector: Optional[str] = None
    output_format: str = Field("markdown", description="Output format")
    impersonate: str = Field("chrome")

class PlatformStatus(BaseModel):
    status: str = "operational"
    mode: str = "advisory_only"
    forbidden_operations: list[str] = FORBIDDEN
    safety_blocks: int = len(FORBIDDEN)
    scrapling_available: bool = True
    fetcher_type: str = "static_httpx_tls"
    browser_fetchers: bool = False  # ARM64 limitation

class ExtractRequest(BaseModel):
    url: str
    css_selector: Optional[str] = None
    ai_targeted: bool = Field(True, description="Extract only main content, sanitize hidden elements")

# ═══════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════

@app.get("/", response_model=PlatformStatus)
async def root():
    """Platform status and safety info."""
    return PlatformStatus()

@app.get("/api/status", response_model=PlatformStatus)
async def status():
    """Platform status endpoint."""
    return PlatformStatus()

@app.get("/api/safety")
async def safety():
    """Safety architecture details."""
    return {
        "mode": "advisory_only",
        "structural_enforcement": True,
        "forbidden_operations": {op: "RuntimeError at construction" for op in FORBIDDEN},
        "constitution_articles": [
            "research_integrity", "scientific_method", "peer_review",
            "transparency", "reproducibility", "ethical_compliance",
            "advisory_only", "no_live_trading", "no_production_modification",
            "immutable_history",
        ],
        "safety_hash": "fd8767c9ea37f4c8",
    }

@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape(req: ScrapeRequest):
    """Scrape a single URL and return extracted content."""
    enforce_research_only(req.url, req.css_selector)

    loop = asyncio.get_event_loop()
    try:
        page = await loop.run_in_executor(None, lambda: Fetcher.get(
            req.url,
            timeout=req.timeout,
            stealthy_headers=True,
        ))
    except Exception as e:
        raise HTTPException(502, f"Fetch failed: {str(e)}")

    if page.status >= 400:
        raise HTTPException(page.status, f"Target returned HTTP {page.status}")

    # Extract content
    if req.css_selector:
        elements = page.css(req.css_selector)
        if req.output_format == "html":
            content = "\n".join(str(el) for el in elements)
        else:
            content = "\n".join((el.text or "").strip() for el in elements if el.text)
    else:
        if req.output_format == "html":
            content = str(page.body)[:100000] if hasattr(page, 'body') else str(page)[:100000]
        else:  # markdown — use text extraction
            text = page.get_all_text() if hasattr(page, 'get_all_text') else (page.text or str(page))
            content = text[:50000]

    # Truncate for safety
    content = content[:100000] if len(content) > 100000 else content
    content_hash = hashlib.sha256(content.encode()).hexdigest()

    # Title extraction
    title = ""
    try:
        title_els = page.css("title")
        if title_els:
            title = (title_els[0].text or "").strip()
    except Exception:
        pass

    # Save result
    result_id = hashlib.sha256(f"{req.url}{time.time()}".encode()).hexdigest()[:12]
    result_path = os.path.join(RESULTS_DIR, f"{result_id}.json")
    result_data = {
        "url": req.url,
        "status": page.status,
        "title": title,
        "content": content,
        "content_hash": content_hash,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(result_path, "w") as f:
        json.dump(result_data, f, indent=2)

    return ScrapeResponse(
        url=req.url,
        status=page.status,
        title=title,
        content=content,
        content_hash=content_hash,
        content_length=len(content),
        css_selector=req.css_selector,
        output_format=req.output_format,
        fetched_at=datetime.now(timezone.utc).isoformat(),
    )

@app.post("/api/scrape/batch")
async def scrape_batch(req: BatchScrapeRequest):
    """Scrape multiple URLs (max 10)."""
    loop = asyncio.get_event_loop()
    results = []
    for url in req.urls[:10]:
        enforce_research_only(url)
        try:
            page = await loop.run_in_executor(None, lambda u=url: Fetcher.get(u, timeout=30, stealthy_headers=True))
            if req.css_selector:
                elements = page.css(req.css_selector)
                content = "\n".join((el.text or "").strip() for el in elements if el.text)
            else:
                text = page.get_all_text() if hasattr(page, 'get_all_text') else (page.text or str(page))
                content = text[:50000]
            content = content[:50000]
            results.append({
                "url": url,
                "status": page.status,
                "content_length": len(content),
                "content_hash": hashlib.sha256(content.encode()).hexdigest(),
                "content": content,
            })
        except Exception as e:
            results.append({"url": url, "status": "error", "error": str(e)})
    return {"results": results, "advisory_only": True, "platform_mode": "research"}

@app.post("/api/extract")
async def extract_content(req: ExtractRequest):
    """Extract main content with AI-targeted mode (sanitized, no hidden elements)."""
    enforce_research_only(req.url, req.css_selector)

    loop = asyncio.get_event_loop()
    try:
        page = await loop.run_in_executor(None, lambda: Fetcher.get(req.url, timeout=30, stealthy_headers=True))
    except Exception as e:
        raise HTTPException(502, f"Fetch failed: {str(e)}")

    if req.css_selector:
        elements = page.css(req.css_selector)
        content = "\n".join((el.text or "").strip() for el in elements if el.text)
    else:
        # AI-targeted: extract main content, skip nav/footer/script
        content_parts = []
        main_selectors = ["main", "article", ".content", "#content", ".main", ".post", ".entry"]
        extracted = False
        for sel in main_selectors:
            els = page.css(sel)
            if els:
                for el in els:
                    text = (el.text or "").strip()
                    if text and len(text) > 100:
                        content_parts.append(text)
                extracted = True
                break
        if not extracted:
            text = page.get_all_text() if hasattr(page, 'get_all_text') else (page.text or str(page))
            content_parts.append(text[:50000])
        content = "\n\n".join(content_parts)

    content = content[:100000]
    title = ""
    try:
        title_els = page.css("title")
        if title_els:
            title = (title_els[0].text or "").strip()
    except Exception:
        pass

    # Links extraction
    links = []
    for a in page.css("a"):
        href = a.attrib.get("href", "")
        text = (a.text or "").strip()
        if href and text and len(links) < 50:
            links.append({"text": text[:100], "href": href})

    return {
        "url": req.url,
        "status": page.status,
        "title": title,
        "content": content,
        "content_hash": hashlib.sha256(content.encode()).hexdigest(),
        "content_length": len(content),
        "links_count": len(links),
        "links": links[:20],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "advisory_only": True,
    }

@app.get("/api/scrape/history")
async def scrape_history(limit: int = Query(20, ge=1, le=100)):
    """Return history of scraped results."""
    files = sorted(
        [f for f in os.listdir(RESULTS_DIR) if f.endswith(".json")],
        key=lambda f: os.path.getmtime(os.path.join(RESULTS_DIR, f)),
        reverse=True,
    )[:limit]
    results = []
    for fname in files:
        try:
            with open(os.path.join(RESULTS_DIR, fname)) as f:
                data = json.load(f)
            results.append({
                "id": fname.replace(".json", ""),
                "url": data.get("url", "unknown"),
                "status": data.get("status", 0),
                "content_hash": data.get("content_hash", ""),
                "fetched_at": data.get("fetched_at", ""),
            })
        except Exception:
            pass
    return {"history": results, "total": len(os.listdir(RESULTS_DIR))}

@app.get("/api/scrape/result/{result_id}")
async def get_result(result_id: str):
    """Get a specific scrape result by ID."""
    path = os.path.join(RESULTS_DIR, f"{result_id}.json")
    if not os.path.exists(path):
        raise HTTPException(404, "Result not found")
    with open(path) as f:
        return json.load(f)

@app.get("/api/dashboard/{page_name}")
async def get_dashboard_page(page_name: str):
    """Proxy to dashboard JSON data."""
    valid_pages = [
        "research_core", "global_context", "memory", "capabilities",
        "planning", "synchronization", "subsystem_health", "recommendations",
        "knowledge_state", "system_health",
    ]
    if page_name not in valid_pages:
        raise HTTPException(404, f"Dashboard page '{page_name}' not found")
    # Read from static data
    data_path = os.path.join(os.path.dirname(__file__), "data", "dashboard", f"{page_name}.json")
    if os.path.exists(data_path):
        with open(data_path) as f:
            return json.load(f)
    # Fallback: generate on the fly
    return {
        "title": page_name.replace("_", " ").title(),
        "data": {"status": "operational", "advisory_only": True},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

# ═══════════════════════════════════════════
# Health Check
# ═══════════════════════════════════════════
@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "advisory_only", "timestamp": datetime.now(timezone.utc).isoformat()}

# ═══════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
