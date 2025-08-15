from playwright.sync_api import sync_playwright
import os
import re

# Function to make title safe for filenames
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context1 = browser.new_context()
    page1 = context1.new_page()
    page1.goto("https://bing.com")

    context2 = browser.new_context()
    page2 = context2.new_page()
    page2.goto("https://google.com")

    print(page1.title())
    # page1.screenshot(path="tmp/bing.png")
    print(page2.title())
    # page2.screenshot(path="tmp/google.png")

    for ctx_index, context in enumerate(browser.contexts, start=1):
        for page_index, page in enumerate(context.pages, start=1):
            title = page.title()
            safe_title = sanitize_filename(title)
            file_path = os.path.join("tmp", f"{safe_title}.png")
            page.screenshot(path=file_path, full_page=True)
            print(f"[Context {ctx_index} - Page {page_index}] Screenshot saved as {file_path}")
    browser.close()