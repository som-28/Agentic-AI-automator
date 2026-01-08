"""Scraper tool using requests + BeautifulSoup.

Given `args` with either a `url` or `top_k` and a `context` that may contain
search results, it fetches pages and extracts text paragraphs.
"""
from typing import Tuple, List
import requests
from bs4 import BeautifulSoup


def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Grab visible paragraph text
    ps = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
    return "\n\n".join(ps[:20])


def run(args: dict, context: dict) -> Tuple[List[str], dict]:
    logs = []
    outputs = []

    if "url" in args and args["url"]:
        urls = [args["url"]]
    else:
        # pull URLs from previous search results in context
        results = None
        for k, v in context.items():
            if isinstance(v, dict) and v.get("results"):
                results = v.get("results")
                break
        if not results:
            return ["No URLs or search results available to scrape"], {"pages": []}
        top_k = int(args.get("top_k", 3))
        urls = [r.get("url") for r in results[:top_k]]

    for u in urls:
        try:
            logs.append(f"Fetching {u}")
            r = requests.get(u, timeout=10)
            if r.status_code == 200:
                text = _extract_text(r.text)
                outputs.append({"url": u, "text": text or "(no text)"})
                logs.append(f"Scraped {u} ({len(text)} chars)")
            else:
                logs.append(f"Failed to fetch {u}: status {r.status_code}")
        except Exception as e:
            logs.append(f"Error fetching {u}: {e}")

    return logs, {"pages": outputs}
