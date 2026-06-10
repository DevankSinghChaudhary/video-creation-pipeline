import asyncio
import hashlib
import time

from bs4 import BeautifulSoup
from ddgs import DDGS
import httpx
from langchain.tools import tool

# --------------------------------------------------
# CACHE
# --------------------------------------------------

CACHE = {}
CACHE_TTL = 3600


def cache_key(url: str):
    return hashlib.md5(url.encode()).hexdigest()


def get_cache(url: str):
    item = CACHE.get(cache_key(url))

    if not item:
        return None

    if time.time() - item["time"] > CACHE_TTL:
        return None

    return item["data"]


def set_cache(url: str, data: str):
    CACHE[cache_key(url)] = {
        "time": time.time(),
        "data": data,
    }


# --------------------------------------------------
# CLEAN HTML
# --------------------------------------------------

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "svg",
        ]
    ):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)[:5000]


# --------------------------------------------------
# NORMALIZE LLM INPUT
# --------------------------------------------------

def normalize_queries(raw_queries) -> list[str]:
    """
    Handles:
    ["AI"]
    [{"query":"AI"}]
    [{"title":"AI"}]
    """

    normalized = []

    for item in raw_queries:

        if isinstance(item, str):
            normalized.append(item)
            continue

        if isinstance(item, dict):

            if "query" in item:
                normalized.append(item["query"])
                continue

            if "title" in item:
                normalized.append(item["title"])
                continue

            normalized.append(str(item))
            continue

        normalized.append(str(item))

    return normalized


# --------------------------------------------------
# DDGS SEARCH
# --------------------------------------------------

async def get_urls_async(
    query: str,
    max_results: int = 3,
):

    def search():

        urls = []

        try:
            with DDGS() as ddgs:

                for result in ddgs.text(
                    query,
                    max_results=max_results,
                ):

                    for key in (
                        "href",
                        "url",
                        "link",
                    ):

                        value = result.get(key)

                        if value:
                            urls.append(value)
                            break

        except Exception:
            pass

        return urls[:max_results]

    return await asyncio.to_thread(search)


# --------------------------------------------------
# FETCH PAGE
# --------------------------------------------------

async def fetch_page(
    client: httpx.AsyncClient,
    url: str,
):

    cached = get_cache(url)

    if cached:
        return {
            "url": url,
            "content": cached,
        }

    try:

        response = await client.get(
            url,
            timeout=8,
        )

        if response.status_code == 200:

            content = extract_text(
                response.text
            )

            set_cache(
                url,
                content,
            )

            return {
                "url": url,
                "content": content,
            }

    except Exception:
        pass

    return {
        "url": url,
        "content": "",
    }


# --------------------------------------------------
# SEARCH PIPELINE
# --------------------------------------------------

async def search_multi_async(
    queries,
    max_results: int = 3,
):

    queries = normalize_queries(
        queries
    )

    # SEARCH PHASE

    url_lists = await asyncio.gather(
        *[
            get_urls_async(
                q,
                max_results,
            )
            for q in queries
        ]
    )

    query_map = {
        query: urls
        for query, urls in zip(
            queries,
            url_lists,
        )
    }

    # UNIQUE URLS

    unique_urls = list(
        {
            url
            for urls in url_lists
            for url in urls
        }
    )

    limits = httpx.Limits(
        max_connections=100,
        max_keepalive_connections=30,
    )

    async with httpx.AsyncClient(
        follow_redirects=True,
        limits=limits,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        },
        http2=True,
    ) as client:

        page_results = await asyncio.gather(
            *[
                fetch_page(
                    client,
                    url,
                )
                for url in unique_urls
            ]
        )

    url_map = {
        item["url"]: item
        for item in page_results
    }

    final_results = {}

    for query in queries:

        final_results[query] = [
            url_map[url]
            for url in query_map[query]
            if url_map[url]["content"]
        ]

    return {
        "queries": queries,
        "results": final_results,
    }


# --------------------------------------------------
# TOOL
# --------------------------------------------------

@tool("web_search", description="Multi-query hybrid web search tool", return_direct=False)
def web_search(
    queries: list[str],
    max_results: int = 3,
):

    return asyncio.run(
        search_multi_async(
            queries,
            max_results,
        )
    )