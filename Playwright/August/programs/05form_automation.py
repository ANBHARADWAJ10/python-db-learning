from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/automation-practice-form")

    # perform actions:
    # typing
    page.type("#firstName", "Nikhil")
    page.type("#lastName", "Anantharaju")
    page.fill("#userEmail","nikhil@gmail.com")

    # custom radio checkbox
    page.get_by_text("Male", exact=True).click()
    page.get_by_placeholder("Mobile Number").type("7036618674")

    # # Date of Birth
    # # open the datepicker by clicking input
    # page.click("#dateOfBirth")
    #
    # # Select month
    # page.select_option("select[class*=''] >> nth=0", "Aug")
    #
    # # Select Year
    # page.select_option("select[class*=''] >> nth=1", "2002")
    #
    # # Click the day

    page.get_by_text("Sports", exact=True).check()

    # Upload a file
    page.set_input_files("input[type='file']", "C:/Users/Administrator/Desktop/Accentiqa/python-db-learning/Playwright/August/programs/tmp/screenshot.png")

    page.screenshot(path="tmp/form.png", full_page=True)
    browser.close()