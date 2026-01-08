"""Enhanced scraper with Playwright support for JS-heavy sites.

Falls back to requests+BeautifulSoup if Playwright is not configured.
"""
from typing import Tuple, List
import os
import requests
from bs4 import BeautifulSoup


def _extract_text_bs4(html: str) -> str:
    """Extract text using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get visible text
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    if paragraphs:
        return "\n\n".join(paragraphs[:20])
    
    # Fallback to body text
    text = soup.get_text(separator="\n", strip=True)
    lines = [line for line in text.split("\n") if line.strip()]
    return "\n".join(lines[:50])


def _scrape_with_requests(url: str) -> str:
    """Scrape using requests + BeautifulSoup."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return _extract_text_bs4(resp.text)
        return f"(HTTP {resp.status_code})"
    except Exception as e:
        return f"(Error: {e})"


def _scrape_with_playwright(url: str) -> str:
    """Scrape using Playwright for JS-rendered content."""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000)
            page.wait_for_timeout(2000)  # Wait for JS to render
            content = page.content()
            browser.close()
            return _extract_text_bs4(content)
    except ImportError:
        return "(Playwright not installed)"
    except Exception as e:
        return f"(Playwright error: {e})"


def run(args: dict, context: dict) -> Tuple[List[str], dict]:
    logs = []
    outputs = []
    scraper_mode = os.getenv("SCRAPER_MODE", "requests")
    
    # Determine URLs to scrape
    if "url" in args and args["url"]:
        urls = [args["url"]]
    else:
        # Pull URLs from previous search results
        results = None
        for k, v in context.items():
            if isinstance(v, dict) and v.get("results"):
                results = v.get("results")
                break
        if not results:
            return ["No URLs or search results available to scrape"], {"pages": []}
        
        top_k = int(args.get("top_k", 3))
        urls = [r.get("url") for r in results[:top_k] if r.get("url")]
    
    # Scrape each URL
    for url in urls:
        logs.append(f"Fetching {url} (mode: {scraper_mode})")
        
        if scraper_mode == "playwright":
            text = _scrape_with_playwright(url)
        else:
            text = _scrape_with_requests(url)
        
        outputs.append({"url": url, "text": text})
        logs.append(f"Scraped {url} ({len(text)} chars)")
    
    return logs, {"pages": outputs}
