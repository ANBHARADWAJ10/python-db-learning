from time import sleep
from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright, *, url: str) -> dict:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    sleep(1)
    # this helps us to see the browser in action

    page.goto(url)

    sleep(1)

    title = page.title()

    browser.close()

    return {'url': url, 'title': title}

def main():
    with sync_playwright() as playwright:
        result = run(playwright, url="https://crawlee.dev")
        print(result)

if __name__ == '__main__':
    main()
