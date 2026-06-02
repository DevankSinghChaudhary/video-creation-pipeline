"""Browser-based web search tool using DuckDuckGo + Playwright for content extraction."""

from ddgs import DDGS
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from langchain.tools import tool

# -------------------------
# BROWSER MANAGER (REUSED)
# -------------------------
class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def new_page(self):
        return self.browser.new_page()

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()


# -------------------------
# SEARCH URLs
# -------------------------
def get_urls(query: str, max_results: int = 5):
    urls = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if isinstance(r, dict):
                for key in ["href", "url", "link"]:
                    if r.get(key):
                        urls.append(r[key])
                        break

    return urls[:max_results]


# -------------------------
# CLEAN HTML
# -------------------------
def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # remove noise
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)

    return cleaned


# -------------------------
# MAIN TOOL FUNCTION
# -------------------------
def search_web(query: str, max_results: int = 5) -> dict:
    """
    Search web using DuckDuckGo + extract pages using a reusable Playwright browser.
    Returns structured results for LLM / RAG / agents.
    """

    urls = get_urls(query, max_results)

    results = []

    bm = BrowserManager()
    bm.start()

    try:
        for url in urls:
            try:
                page = bm.new_page()

                page.goto(url, timeout=30000)
                html = page.content()

                text = extract_text(html)

                results.append({
                    "url": url,
                    "content": text[:4000]  # safe context limit
                })

                page.close()

            except Exception as e:
                results.append({
                    "url": url,
                    "content": "",
                    "error": str(e)
                })

    finally:
        bm.close()

    return {
        "query": query,
        "results": results
    }


@tool('web_search', description='Search the web for information.', return_direct=False)
def web_search(query: str) -> str:
    """Search the web for information."""
    results = search_web(query)
    return results