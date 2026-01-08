"""Fake Search Tool for demo purposes.

Returns a list of simulated search results for a query. Replace or extend with
SerpAPI / Google Custom Search if you have API keys.
"""
from typing import Tuple, List


def run(args: dict, context: dict) -> Tuple[List[str], dict]:
    query = args.get("query", "")
    limit = int(args.get("limit", 5))
    results = []
    # Fake results: in real life call external search API
    for i in range(1, limit + 1):
        results.append({
            "title": f"Result {i} for {query}",
            "url": f"https://example.com/{query.replace(' ', '-')}/{i}",
            "snippet": f"This is a short snippet describing {query} result #{i}.",
        })

    logs = [f"Search: found {len(results)} results for '{query}'"]
    # Return logs and output (search results)
    return logs, {"results": results}
