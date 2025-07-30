# # core script
from playwright.sync_api import sync_playwright
import csv

def search_bing(query):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        page = browser.new_page()
        page.goto("https://bing.com/")

        page.fill("textarea[name='q']", query)
        page.press("input[type='Submit']",'Enter')

        page.wait_for_selector("li.b_algo h2 a")
        # Extract top 5 results
        links = page.query_selector_all("li.b_algo h2 a")[:5]
        results = []

        for link in links:
            title =  link.inner_text()
            url = link.get_attribute("href")
            results.append({"title": title, "url": url})
            print(f"{title} -> {url}")

        browser.close()

        return results


def save_to_csv(results, filename="results.csv"):
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(results)
        print(f"\n✅ Saved {len(results)} results to {filename}")

if __name__ == "__main__":
    query = "Playwright Python"
    results = search_bing(query)
    save_to_csv(results)


# from playwright.sync_api import sync_playwright
# import csv
#
# def search_bing(query):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         print("Opening Bing...")
#         page.goto("https://www.bing.com", timeout=20000)
#
#         # Accept cookies popup if it shows up
#         try:
#             page.locator("button:has-text('Accept')").click(timeout=5000)
#         except:
#             print("No cookie popup.")
#
#         # Check if the search bar exists
#         try:
#             search_selector = "input[name='q']"  # Fallback selector
#             page.wait_for_selector(search_selector, timeout=10000)
#             page.fill(search_selector, query)
#             page.press(search_selector, "Enter")
#         except Exception as e:
#             print(f"❌ Couldn't find search input: {e}")
#             browser.close()
#             return []
#
#         # Wait for search results
#         page.wait_for_selector("li.b_algo h2 a", timeout=10000)
#
#         results = []
#         links = page.query_selector_all("li.b_algo h2 a")[:5]
#
#         for link in links:
#             title = link.inner_text()
#             url = link.get_attribute("href")
#             results.append({"title": title, "url": url})
#             print(f"{title} -> {url}")
#
#         browser.close()
#         return results
#
# def save_to_csv(results, filename="results.csv"):
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=["title", "url"])
#         writer.writeheader()
#         writer.writerows(results)
#         print(f"\n✅ Saved {len(results)} results to {filename}")
#
# if __name__ == "__main__":
#     query = "Playwright Python"
#     results = search_bing(query)
#     save_to_csv(results)
