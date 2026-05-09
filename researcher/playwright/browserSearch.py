from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from urllib.parse import quote
import random
import time


def search_web(data: dict, max_results_per_query: int = 10):

    results = {
        "searchURLs": {}
    }

    queries = data.get("search_queries", [])

    with sync_playwright() as p:

        browser = p.chromium.launch_persistent_context(
            user_data_dir="playwright_cache",
            headless=False,
            slow_mo=50,
            viewport={
                "width": 1366,
                "height": 768
            },
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        page = browser.new_page()

        stealth_sync(page)

        for query in queries:

            print(f"\nSearching: {query}")

            encoded_query = quote(query)

            # DuckDuckGo HTML version
            url = f"https://duckduckgo.com/html/?q={encoded_query}"

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            time.sleep(random.uniform(2, 4))

            urls = []

            # DuckDuckGo result links
            result_links = page.locator("a.result__a")

            count = result_links.count()

            for i in range(count):

                try:

                    href = result_links.nth(i).get_attribute("href")

                    if not href:
                        continue

                    if href.startswith("http"):

                        if href not in urls:
                            urls.append(href)

                except:
                    continue

            # Fallback selector if needed
            if not urls:

                fallback_links = page.locator("a")

                fallback_count = fallback_links.count()

                for i in range(fallback_count):

                    try:

                        href = fallback_links.nth(i).get_attribute("href")

                        if not href:
                            continue

                        if href.startswith("http"):

                            blocked_domains = [
                                "duckduckgo.com",
                                "javascript:",
                                "#"
                            ]

                            if any(
                                blocked in href
                                for blocked in blocked_domains
                            ):
                                continue
                            if href not in urls:
                                urls.append(href)

                    except:
                        continue

            results["searchURLs"][query] = urls[:max_results_per_query]

            print(
                f"Found {len(results['searchURLs'][query])} URLs"
            )
            time.sleep(random.uniform(3, 6))

        browser.close()

    return results