from playwright.sync_api import sync_playwright
import csv

def search(query):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        page = browser.new_page()
        page.goto("https://bing.com/")

        # search for the query
        page.fill("textarea[name='q']", query)
        page.press("input[type='Submit']", "Enter")

        # wait
        page.wait_for_selector("li.b_algo h2 a")

        links = page.query_selector_all("li.b_algo h2 a")[:5]
        results = []

        for link in links:
            title = link.inner_text()
            url = link.get_attribute("href")
            results.append({"title": title, "url": url})
            print(f"{title} -> {url}")
        browser.close()

        return results

def sav_to_csv(results, filename='results.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'url'])
        writer.writeheader()
        writer.writerows(results)
        print(f"\n✅ Saved {len(results)} results to {filename}")


if __name__ == "__main__":
    query = "Playwright Python"
    results = search(query)
    sav_to_csv(results)