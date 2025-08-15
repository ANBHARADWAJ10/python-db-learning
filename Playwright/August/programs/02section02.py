from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context1 = browser.new_context()
    page1 = context1.new_page()
    page1.goto("https://google.com")

    context2 = browser.new_context()
    page2 = context2.new_page()
    page2.goto("https://bing.com")

    print("Title of the first page:")
    print(f"title: {page1.title()}")
    print("Title of the Second page:")
    print(f"title: {page2.title()}")

    browser.close()

