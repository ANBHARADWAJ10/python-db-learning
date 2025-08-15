from playwright.sync_api import sync_playwright
import os
import re

def sanitize_title(name):
    return re.sub(r'[\\/*?:"<>|]','_', name)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # new context opens a new browser, and it has its own cache, cookies and usually acts like incognito browser.
    # context 01
    context1 = browser.new_context()
    page1 = context1.new_page()
    page1.goto("https://google.com")

    # context 02
    context2 = browser.new_context()
    page2 = context2.new_page()
    page2.goto("https://bing.com")

    for ctx_idx, context in enumerate(browser.contexts, start=1):
        for pg_idx, page in enumerate(context.pages, start=1):
            title = page.title()
            file_name = sanitize_title(title)
            file_path = os.path.join('tmp2', f'{file_name}.png')
            page.screenshot(path=file_path, full_page=True)
            print(f"[Context {ctx_idx} - Page {pg_idx}] Screenshot saved as {file_name} in {file_path}")

    browser.close()