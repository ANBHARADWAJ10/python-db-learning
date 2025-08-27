# import asyncio
# from playwright.async_api import async_playwright
# import os
#
#
# async def use_saved_session():
#     session_file = "site24x7_session.json"
#
#     if not os.path.exists(session_file):
#         print("❌ No saved session found. Run login_with_otp.py first!")
#         return
#
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#
#         try:
#             # Load saved session
#             context = await browser.new_context(storage_state=session_file)
#             page = await context.new_page()
#
#             # Go directly to Site24x7 dashboard
#             print("🔄 Loading Site24x7 with saved session...")
#             await page.goto('https://www.site24x7.com/app/client?a=f#/home/monitors')
#
#             # Check if we're logged in
#             await page.wait_for_load_state('networkidle')
#
#             # You can add your automation tasks here
#             print("✅ Successfully logged in using saved session!")
#             print("🎯 Ready for your automation tasks...")
#
#             # Example: Get page title
#             title = await page.title()
#             print(f"Page title: {title}")
#
#             # Downloading Outages
#             outages = page.locator('//a[@href="#/home/outages"]')
#             await outages.click()
#
#             # We have to check if the option share this is available or not
#             share_this_btn = page.locator('//button[@id="report_header_sharethis"]')
#             await share_this_btn.click()
#
#             # click on export pdf and download
#             pdf = page.locator('text="PDF"')
#
#             # downloads and saves the outages file in the downloads folder.
#             download_pdf(pdf)
#
#             # Keep browser open for manual inspection
#             input("Press Enter to close browser...")
#
#         except Exception as e:
#             print(f"❌ Error using saved session: {e}")
#             print("💡 Try running login_with_otp.py again to refresh session")
#         finally:
#             await browser.close()
#
# def download_pdf(pdf):
#     # Create downloads folder if it doesn't exist
#     downloads_dir = os.path.join(os.getcwd(), "downloads")
#     os.makedirs(downloads_dir, exist_ok=True)
#
#     # Wait for download and click the PDF export button
#     file = pdf.click()
#     download = file.value()
#
#     file_path = os.path.join(downloads_dir, "outages_file.pdf")
#     download.save_as(file_path)
#
#     print(f"File saved to: {file_path}")
#
# if __name__ == "__main__":
#     asyncio.run(use_saved_session())

import asyncio
from playwright.async_api import async_playwright
import os


async def use_saved_session():
    session_file = "site24x7_session.json"

    if not os.path.exists(session_file):
        print("❌ No saved session found. Run login_with_otp.py first!")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            # Load saved session with downloads enabled
            context = await browser.new_context(
                storage_state=session_file,
                accept_downloads=True  # Enable downloads
            )
            page = await context.new_page()

            # Go directly to Site24x7 dashboard
            print("🔄 Loading Site24x7 with saved session...")
            await page.goto('https://www.site24x7.com/app/client?a=f#/home/monitors')

            # Check if we're logged in
            await page.wait_for_load_state('networkidle')

            print("✅ Successfully logged in using saved session!")
            print("🎯 Ready for your automation tasks...")

            # Example: Get page title
            title = await page.title()
            print(f"Page title: {title}")

            # Downloading Outages
            outages = page.locator('//a[@href="#/home/outages"]')
            await outages.click()

            # Wait for page to load
            await page.wait_for_load_state('networkidle')

            # We have to check if the option share this is available or not
            share_this_btn = page.locator('//button[@id="report_header_sharethis"]')
            await share_this_btn.click()

            # Wait for dropdown/modal to appear
            await page.wait_for_timeout(1000)

            # Download PDF - corrected approach
            await download_pdf(page)

            # Keep browser open for manual inspection
            input("Press Enter to close browser...")

        except Exception as e:
            print(f"❌ Error using saved session: {e}")
            print("💡 Try running login_with_otp.py again to refresh session")
        finally:
            await browser.close()


async def download_pdf(page):
    """Download PDF file using async Playwright"""
    try:
        # Create downloads folder if it doesn't exist
        downloads_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        # Wait for download and click the PDF export button
        async with page.expect_download() as download_info:
            # Click PDF option
            pdf_locator = page.locator('text="PDF"')
            await pdf_locator.click()

        download = await download_info.value

        # Save file with custom name
        file_path = os.path.join(downloads_dir, "outages_file.pdf")
        await download.save_as(file_path)

        print(f"File saved to: {file_path}")

    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")


if __name__ == "__main__":
    asyncio.run(use_saved_session())
