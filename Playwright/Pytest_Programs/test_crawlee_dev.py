# from playwright.sync_api import Page
#
# def test_get_started_button(page: Page) -> None:
#
#     page.goto('https://crawlee.dev')
#
#     # create a locator for the 'Get started' button on the page.
#     button = page.locator('text=Get started with Python')
#
#     # Assert that exactly one 'Get started with Python'  button exists
#     assert button.count() == 1
#
#     # Assert that the button is visible to the user/
#     assert button.is_visible()
#
#     # Assert that the button is enabled and clicked or interacted with.
#     assert button.is_enabled()
#
#     # assert the button's href attribute points to the expected URL path
#     assert button.get_attribute('href') == 'docs/quick-start'
#

from playwright.sync_api import Page

def test_get_started_button(page: Page) -> None:
    # Navigate to the 'Crawlee' website.
    page.goto('https://playwright.dev/python/')

    # Create a locator for the 'Get Started' button on the page.
    button = page.locator('text=Get Started')

    # Assert that exactly one 'Get Started' button exists.
    assert button.count() == 1

    # Assert that the button is visible to the user.
    assert button.is_visible()

    # Assert that the button is enabled and can be clicked or interacted with.
    assert button.is_enabled()

    # Assert the button's href attribute points to the expected URL path.
    assert button.get_attribute('href') == '/python/docs/Three_main_building_blocks'

    # Validate the button's CSS styling to ensure it matches the expected design.
    # assert button.evaluate('el => window.getComputedStyle(el).backgroundColor') == 'rgb(237, 53, 69)'
    # assert button.evaluate('el => window.getComputedStyle(el).borderRadius') == '8px'
    # assert button.evaluate('el => window.getComputedStyle(el).color') == 'rgb(255, 255, 255)'
    # assert button.evaluate('el => window.getComputedStyle(el).fontSize') == '18px'
    # assert button.evaluate('el => window.getComputedStyle(el).fontWeight') == '600'
    # assert button.evaluate('el => window.getComputedStyle(el).lineHeight') == '28px'
    # assert button.evaluate('el => window.getComputedStyle(el).padding') == '12px 24px'
