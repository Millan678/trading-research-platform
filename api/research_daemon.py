#!/usr/bin/env python3
"""
TRP Research Daemon — Continuous scraping pipeline
Runs on the Hermes server, periodically scrapes research sources,
saves results to data/, and pushes updates to GitHub Pages.

Research-only: no live trading, broker execution, or production modification.
"""
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone

from scrapling.fetchers import Fetcher

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(CONFIG_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

RESEARCH_SOURCES = [
    {"name": "arXiv Quantitative Finance", "url": "https://arxiv.org/list/q-fin/recent", "category": "academic"},
    {"name": "SEC EDGAR Current Filings", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent", "category": "regulatory"},
    {"name": "FRED Economic Data", "url": "https://fred.stlouisfed.org/", "category": "economic"},
    {"name": "NBER Working Papers", "url": "https://www.nber.org/papers", "category": "academic"},
    {"name": "World Bank Open Data", "url": "https://data.worldbank.org/", "category": "economic"},
    {"name": "FDIC Bank Failures", "url": "https://www.fdic.gov/bank-failures/failed-bank-list", "category": "regulatory"},
    {"name": "Investopedia Markets", "url": "https://www.investopedia.com/markets", "category": "education"},
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/", "category": "market_data"},
    {"name": "TradingView Ideas", "url": "https://www.tradingview.com/ideas/", "category": "analysis"},
    {"name": "CoinDesk Crypto News", "url": "https://www.coindesk.com/", "category": "crypto"},
    {"name": "SSRN New Papers", "url": "https://www.ssrn.com/en/", "category": "academic"},
    {"name": "St. Louis Fed Research", "url": "https://www.stlouisfed.org/research", "category": "central_banking"},
    {"name": "BIS Publications", "url": "https://www.bis.org/publ.htm", "category": "central_banking"},
    {"name": "CFTC Weekly Reports", "url": "https://www.cftc.gov/MarketAndReportings.htm", "category": "regulatory"},
    {"name": "Federal Reserve Board", "url": "https://www.federalreserve.gov/newsevents.htm", "category": "central_banking"},
]

FORBIDDEN_PATTERNS = [
    "live_trading", "broker_execution", "order_placement",
    "place_order", "execute_trade", "buy_sell",
]


def check_safety(url: str) -> bool:
    """Enforce research-only mode."""
    lower = url.lower()
    return not any(p in lower for p in FORBIDDEN_PATTERNS)


def extract_text(page, css_selector=None):
    """Extract text content from a Scrapling page, trying multiple methods."""
    # Method 1: Specific CSS selector
    if css_selector:
        try:
            elements = page.css(css_selector)
            texts = []
            for el in elements:
                # Try get_all_text on element first
                try:
                    t = el.get_all_text()
                    if t and t.strip():
                        texts.append(t.strip())
                except Exception:
                    pass
                # Fallback to .text
                if not texts or not texts[-1]:
                    try:
                        t = el.text
                        if t and t.strip():
                            texts.append(t.strip())
                    except Exception:
                        pass
            if texts:
                return "\n\n".join(texts)
        except Exception:
            pass

    # Method 2: get_all_text on full page (best for static fetcher)
    try:
        t = page.get_all_text()
        if t and len(t.strip()) > 50:
            return t.strip()
    except Exception:
        pass

    # Method 3: page.text
    try:
        t = page.text
        if t and len(t.strip()) > 50:
            return t.strip()
    except Exception:
        pass

    return ""


def extract_links(page, max_links=30):
    """Extract links from page."""
    links = []
    try:
        for a in page.css("a"):
            href = a.attrib.get("href", "")
            text = (a.text or "").strip()[:100]
            if href and text and len(links) < max_links:
                links.append({"text": text, "href": href})
    except Exception:
        pass
    return links


def scrape_source(source: dict) -> dict:
    """Scrape a single research source."""
    url = source["url"]
    if not check_safety(url):
        return {"name": source["name"], "url": url, "error": "FORBIDDEN: research-only mode enforced"}

    try:
        page = Fetcher.get(url, timeout=30, stealthy_headers=True)
        content = extract_text(page, source.get("css"))
        title = ""
        try:
            title_els = page.css("title")
            if title_els:
                title = (title_els[0].get_all_text() if hasattr(title_els[0], 'get_all_text') else (title_els[0].text or "")).strip()
        except Exception:
            pass

        links = extract_links(page)

        return {
            "name": source["name"],
            "url": url,
            "category": source["category"],
            "status": page.status,
            "title": title,
            "content": content[:50000],
            "content_hash": hashlib.sha256(content.encode()).hexdigest(),
            "content_length": len(content),
            "links": links,
            "links_count": len(links),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "advisory_only": True,
        }
    except Exception as e:
        return {
            "name": source["name"],
            "url": url,
            "category": source.get("category", "unknown"),
            "status": "error",
            "error": str(e),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }


def run_research_cycle():
    """Run one full research scraping cycle."""
    print(f"\n[{datetime.now(timezone.utc).isoformat()}] Starting research cycle...")

    results = []
    for i, source in enumerate(RESEARCH_SOURCES):
        print(f"  [{i+1}/{len(RESEARCH_SOURCES)}] Scraping {source['name']}...", end=" ", flush=True)
        result = scrape_source(source)
        results.append(result)

        # Save individual result
        result_id = hashlib.sha256(f"{source['url']}{time.time()}".encode()).hexdigest()[:12]
        with open(os.path.join(RESULTS_DIR, f"{result_id}.json"), "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"→ {result.get('status','err')} | {result.get('content_length',0)} chars | {result.get('links_count',0)} links")

    # Save combined results
    summary = {
        "cycle_completed_at": datetime.now(timezone.utc).isoformat(),
        "sources_scraped": len(results),
        "successful": sum(1 for r in results if r.get("status") == 200),
        "total_content_length": sum(r.get("content_length", 0) for r in results),
        "total_links": sum(r.get("links_count", 0) for r in results),
        "results": results,
        "advisory_only": True,
        "platform_mode": "research",
    }
    with open(os.path.join(RESULTS_DIR, "latest_cycle.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    # Save compact version for frontend
    compact = {
        "last_updated": summary["cycle_completed_at"],
        "sources_scraped": summary["sources_scraped"],
        "successful": summary["successful"],
        "total_content_length": summary["total_content_length"],
        "total_links": summary["total_links"],
        "items": [
            {
                "name": r.get("name", ""),
                "url": r.get("url", ""),
                "category": r.get("category", ""),
                "status": r.get("status", "error"),
                "content_length": r.get("content_length", 0),
                "title": r.get("title", "")[:100],
                "links_count": r.get("links_count", 0),
                "scraped_at": r.get("scraped_at", ""),
            }
            for r in results
        ],
        "advisory_only": True,
    }
    # Write to both local results and docs/ for GitHub Pages
    frontend_path = os.path.join(CONFIG_DIR, "..", "docs", "data", "research_results.json")
    os.makedirs(os.path.dirname(frontend_path), exist_ok=True)
    with open(frontend_path, "w") as f:
        json.dump(compact, f, indent=2)

    print(f"  Cycle complete: {summary['successful']}/{summary['sources_scraped']} successful, {summary['total_content_length']} total chars, {summary['total_links']} total links")
    return summary


def push_to_github():
    """Push updated research data to GitHub Pages."""
    try:
        repo_dir = os.path.join(CONFIG_DIR, "..")
        result = subprocess.run(
            ["git", "add", "docs/data/research_results.json", "api/results/"],
            capture_output=True, text=True, cwd=repo_dir
        )
        # Only commit if there are changes
        check = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True, text=True, cwd=repo_dir
        )
        if check.returncode != 0:  # Changes exist
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            subprocess.run(
                ["git", "commit", "-m", f"research: update scraped data ({ts})"],
                capture_output=True, text=True, cwd=repo_dir
            )
            subprocess.run(
                ["git", "push", "origin", "main"],
                capture_output=True, text=True, cwd=repo_dir
            )
            print(f"  Pushed updated research data to GitHub Pages")
        else:
            print(f"  No data changes to push")
    except Exception as e:
        print(f"  Push error (non-fatal): {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        run_research_cycle()
        push_to_github()
    else:
        # Continuous mode — scrape every 4 hours
        interval = int(os.environ.get("RESEARCH_INTERVAL", 14400))
        print(f"TRP Research Daemon starting (interval: {interval}s = {interval//3600}h)")
        while True:
            try:
                run_research_cycle()
                push_to_github()
            except Exception as e:
                print(f"Cycle error: {e}")
            print(f"  Next cycle in {interval}s ({interval//3600}h)...")
            time.sleep(interval)
