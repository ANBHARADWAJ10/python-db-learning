from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://demo.automationtesting.in/Selectable.html')
        page.wait_for_timeout(3000)

## Legacy (Not recommended)
    # elements = page.query_selector_all('b')
## Modern
        b_tag = page.locator('b')
        all_b_tags = b_tag.all()
        print(f'Total no of b tags in the page: {len(all_b_tags)}')
        for i in all_b_tags:
            print(i.text_content())

    ## get something from the website in the form of string
        ## use get_attribute()
        a_tag = page.locator('a')
        all_a_tags = a_tag.all()
        for i in all_a_tags:
            print(i.get_attribute('href'))
        page.wait_for_timeout(5000)
    except Exception as e:
        print(str(e))
    finally:
        browser.close()