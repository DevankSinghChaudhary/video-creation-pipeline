"""
Multi-query hybrid web search tool:
- DuckDuckGo batch search
- Parallel HTTP fetching
- Optional Playwright fallback
- Shared caching layer
"""

from ddgs import DDGS
import httpx
import asyncio
import time
import hashlib
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from langchain.tools import tool

# -------------------------
# GLOBAL CACHE
# -------------------------
CACHE = {}
CACHE_TTL = 60 * 60  # 1 hour


def cache_key(url: str):
    return hashlib.md5(url.encode()).hexdigest()


def get_cache(url: str):
    key = cache_key(url)
    entry = CACHE.get(key)
    if entry and time.time() - entry["time"] < CACHE_TTL:
        return entry["data"]
    return None


def set_cache(url: str, data: str):
    CACHE[cache_key(url)] = {
        "time": time.time(),
        "data": data
    }


# -------------------------
# SEARCH ENGINE (DDGS)
# -------------------------
def get_urls(query: str, max_results: int = 3):
    urls = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            for k in ["href", "url", "link"]:
                if isinstance(r, dict) and r.get(k):
                    urls.append(r[k])
                    break
    return urls[:max_results]


# -------------------------
# TEXT CLEANER
# -------------------------
def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines()]
    return "\n".join([l for l in lines if l])[:3500]


# -------------------------
# HTTP FETCH (FAST PATH)
# -------------------------
async def fetch_one(client, url):
    try:
        r = await client.get(url, timeout=10)
        return url, r.text
    except:
        return url, ""


async def fetch_all(urls):
    async with httpx.AsyncClient(
        headers={"User-Agent": "Mozilla/5.0"},
        follow_redirects=True
    ) as client:
        tasks = [fetch_one(client, u) for u in urls]
        return await asyncio.gather(*tasks)


# -------------------------
# PLAYWRIGHT FALLBACK
# -------------------------
def fetch_browser(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            html = page.content()
            browser.close()
            return html
    except:
        return ""


# -------------------------
# SMART FETCH
# -------------------------
def process_urls(urls):
    results = []

    # fast HTTP batch
    http_results = asyncio.run(fetch_all(urls))

    for url, html in http_results:
        if not html:
            continue

        cached = get_cache(url)
        if cached:
            results.append({"url": url, "content": cached})
            continue

        text = extract_text(html)
        set_cache(url, text)

        results.append({"url": url, "content": text})

    return results


# -------------------------
# MAIN MULTI-QUERY TOOL
# -------------------------
def search_multi(queries: list[str], max_results: int = 3):
    all_results = {}

    for q in queries:
        urls = get_urls(q, max_results=max_results)
        results = process_urls(urls)

        all_results[q] = results

    return {
        "queries": queries,
        "results": all_results
    }


# -------------------------
# LANGCHAIN TOOL WRAPPER
# -------------------------
@tool("web_search", description="Multi-query hybrid web search tool", return_direct=False)
def web_search(input: dict) -> dict:
    """
    Expected input:
    {
        "queries": ["query1", "query2", "query3"],
        "max_results": 3
    }
    """

    queries = input.get("queries", [])
    max_results = input.get("max_results", 3)

    return search_multi(queries, max_results)