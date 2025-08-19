from playwright.sync_api import sync_playwright, Page

def test_playwright(page: Page) -> None:
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     context = browser.new_context()
    #     page = context.new_page()
    #
    #     page.goto("https://example.com/")
    #
    #     assert page.title() == "Example Domain"
    #
    #     text = page.inner_text("h1")
    #     assert text == "Example Domain"
    #
    #     browser.close()

    page.goto("https://example.com/")

    assert page.title() == "Example Domain"

    text = page.get_by_text("Example Domain")
    assert page.inner_text("h1") == "Example Domain"
