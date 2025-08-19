from playwright.sync_api import sync_playwright
import csv
import time



def fill_form(page, firstname, lastname, email, mobilenumber):
    page.type("#firstName", firstname)
    page.type("#lastName", lastname)
    page.type("#userEmail", email)
    page.type("#userNumber", mobilenumber)
    page.click("button[type='submit']")

    time.sleep(2)
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demoqa.com/automation-practice-form")

        # Read csv file:
        increment = 1
        with open("file.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fill_form(page, row["firstname"], row["lastname"], row["email"], row["mobilenumber"])
                file_name = f"tmp/form_{increment}.png"
                page.screenshot(path=file_name, full_page=True)
                increment += 1
                page.goto("https://demoqa.com/automation-practice-form")

        browser.close()

if __name__ == "__main__":
    main()
