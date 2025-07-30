from playwright.sync_api import sync_playwright
def test_something():

    assert title() == "Fast and reliable end-to-end testing for modern web apps | Playwright"

def title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://playwright.dev/")
        result = page.title()
        print(page.title())
        browser.close()
        return result