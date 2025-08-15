from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://playwright.dev/")
    print(f"title: {page.title()}")
    page.screenshot(path="tmp/screenshot.png")
    browser.close()


