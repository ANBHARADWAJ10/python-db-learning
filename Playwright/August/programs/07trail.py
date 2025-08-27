from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://bing.com/")
    # page.type("#sb_form_q", "Playwright")
    # page.type("textarea[name='q']","Playwright")
    search = page.locator("#sb_form_q")
    search.type("Playwright")
    time.sleep(2)
    page.press("textarea[name='q']", "Enter")
    page.wait_for_load_state("networkidle")
    page.screenshot(path="tmp/trail.png", full_page=True)
    browser.close()
    browser.close()