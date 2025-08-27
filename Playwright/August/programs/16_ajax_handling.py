from playwright.sync_api import sync_playwright

'''
    STEP 1:
        To find the ajax url first you have to click on inspect and then the option
        Network
    STEP 2:
        Then click on button on the top left which looks like do not disturb button in the phone
        Then in this case click on drop-down
    STEP 3:
        Then you can find the details in the header section
    STEP 4:
        You can see a url copy till the '?' symbol as the rest of the url is unique
        and changes every time.
'''



def handle_regex(response):
    if 'https://www.plus2net.com/php_tutorial/dd-ajax.php?' in response.url:
        status_s = response.status
        data = response.text()
        print(f'{status_s}: {data}')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://www.plus2net.com/php_tutorial/ajax_drop_down_list-demo.php')

    drop = page.locator('//select[@id="s1"]')
    page.on('response', lambda response: handle_regex(response))
    drop.select_option('2')
    page.wait_for_timeout(3000)
    drop_2 = page.locator('//select[@id="s2"]')
    drop_2.select_option('Blue')
    page.wait_for_timeout(3000)

