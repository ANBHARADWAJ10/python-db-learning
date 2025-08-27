import asyncio
import yaml
import re
import os
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from playwright.async_api import async_playwright
from typing import List, Tuple, Optional

# ========== Config ==========
MAX_CONCURRENCY = 10  # limit concurrent browsers
CHECK_INTERVAL = 120  # seconds between checks
LOG_LEVEL = logging.INFO
BROWSER_TIMEOUT = 180_000  # 3 minutes
ELEMENT_TIMEOUT = 30_000  # 30 seconds


# ========== Setup Logging ==========
def setup_logging():
    """Setup logging with both file and console output - Windows compatible."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"monitor_{timestamp}.log"

    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create handlers
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


# ========== Load YAML ==========
def load_config(file_path: str = "Checks.yaml") -> dict:
    """Load and validate YAML configuration."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logger.info(f"[SUCCESS] Configuration loaded from {file_path}")
            return config
    except FileNotFoundError:
        logger.error(f"[ERROR] Configuration file {file_path} not found")
        raise
    except yaml.YAMLError as e:
        logger.error(f"[ERROR] Invalid YAML in {file_path}: {e}")
        raise


def safe_filename(url: str) -> str:
    """Create safe filename from URL."""
    return re.sub(r"[^\w\-_.]", "_", url)[:100]


# ========== Screenshot Management ==========
async def take_error_screenshot(page, url: str, error_dir: str, error_type: str = "error") -> str:
    """Take screenshot and save with detailed info - with better error handling."""
    os.makedirs(error_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_filename(url)}_{error_type}_{timestamp}.png"
    screenshot_path = os.path.join(error_dir, filename)

    try:
        # Check if page is still valid before taking screenshot
        if page.is_closed():
            logger.warning(f"[WARN] Cannot take screenshot - page is closed for {url}")
            return f"Screenshot skipped: page closed"

        await page.screenshot(path=screenshot_path, full_page=True)

        # Also save page info for debugging
        info_file = screenshot_path.replace('.png', '_info.json')
        try:
            page_info = {
                'url': url,
                'current_url': page.url,
                'title': await page.title(),
                'timestamp': timestamp,
                'error_type': error_type,
                'viewport': await page.evaluate(
                    '() => ({width: window.innerWidth, height: window.innerHeight})') if not page.is_closed() else None,
            }

            with open(info_file, 'w') as f:
                json.dump(page_info, f, indent=2)
        except Exception as info_error:
            logger.debug(f"[DEBUG] Could not save page info: {info_error}")

        logger.info(f"[SCREENSHOT] Screenshot saved: {screenshot_path}")
        return screenshot_path

    except Exception as e:
        logger.error(f"[ERROR] Failed to take screenshot for {url}: {e}")
        return f"Screenshot failed: {e}"


# ========== Enhanced Steps Execution ==========
async def run_steps(page, steps: List[dict]) -> Tuple[bool, str]:
    """Execute user-defined steps before assertions with enhanced error handling."""
    for i, step in enumerate(steps, 1):
        s_type = step.get("type")
        selector = step.get("selector")
        value = step.get("value")
        timeout = step.get("timeout", ELEMENT_TIMEOUT)

        try:
            logger.debug(f"[STEP] Executing step {i}/{len(steps)}: {s_type}")

            # Check if page is still open
            if page.is_closed():
                return False, f"Step {i} failed: Page was closed"

            if s_type == "fill":
                await page.wait_for_selector(selector, timeout=timeout)
                await page.fill(selector, value)

            elif s_type == "click":
                await page.wait_for_selector(selector, timeout=timeout)
                await page.click(selector)

            elif s_type == "wait_for_selector":
                await page.wait_for_selector(selector, timeout=timeout)

            elif s_type == "wait":
                await asyncio.sleep(float(value))

            elif s_type == "scroll":
                await page.evaluate(f"window.scrollBy(0, {value or 500})")

            elif s_type == "hover":
                await page.hover(selector)

            elif s_type == "select":
                await page.select_option(selector, value)

            else:
                logger.warning(f"[WARN] Unknown step type: {s_type}")

        except Exception as e:
            error_msg = f"Step {i} failed: {s_type} {selector or ''} ({str(e)[:100]})"
            logger.error(f"[ERROR] {error_msg}")
            return False, error_msg

    logger.debug("[SUCCESS] All steps executed successfully")
    return True, "All steps executed successfully"


# ========== Enhanced Assertions ==========
async def run_assertions(page, url: str, assertions: List[dict], response_status: Optional[int]) -> Tuple[bool, str]:
    """Run assertions with detailed error reporting."""
    for i, assertion in enumerate(assertions, 1):
        a_type = assertion.get("type")
        value = assertion.get("value")
        timeout = assertion.get("timeout", 10_000)

        try:
            logger.debug(f"[ASSERTION] Running assertion {i}/{len(assertions)}: {a_type}")

            # Check if page is still open
            if page.is_closed():
                return False, f"Assertion {i} failed: Page was closed"

            if a_type == "title_contains":
                title = await page.title()
                if value not in title:
                    return False, f"Title assertion failed: expected '{value}' in '{title}'"

            elif a_type == "contains_text":
                body_text = await page.inner_text("body")
                if value not in body_text:
                    return False, f"Text assertion failed: '{value}' not found on page"

            elif a_type == "status":
                if response_status != value:
                    return False, f"Status assertion failed: expected {value}, got {response_status}"

            elif a_type == "url_contains":
                current_url = page.url
                if value not in current_url:
                    return False, f"URL assertion failed: expected '{value}' in '{current_url}'"

            elif a_type == "element_present":
                selector = assertion.get("selector")
                try:
                    await page.wait_for_selector(selector, timeout=timeout)
                except Exception:
                    return False, f"Element not found: {selector}"

            elif a_type == "element_not_present":
                selector = assertion.get("selector")
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    return False, f"Element should not be present but found: {selector}"
                except Exception:
                    pass  # Element not found, which is expected

            elif a_type == "element_text_equals":
                selector = assertion.get("selector")
                element_text = await page.inner_text(selector)
                if element_text.strip() != value:
                    return False, f"Element text mismatch: expected '{value}', got '{element_text.strip()}'"

            else:
                return False, f"Unknown assertion type: {a_type}"

        except Exception as e:
            error_msg = f"Assertion {i} error: {a_type} ({str(e)[:100]})"
            logger.error(f"[ERROR] {error_msg}")
            return False, error_msg

    logger.debug("[SUCCESS] All assertions passed")
    return True, "All assertions passed"


# ========== Process URL with Retry Logic ==========
async def process_url(sem, url_config: dict, app_name: str, error_dir: str, retry_count: int = 0) -> str:
    """Process a single URL with enhanced error handling and retry logic."""
    url = url_config["url"]
    assertions = url_config.get("assertions", [])
    steps = url_config.get("steps", [])
    max_retries = url_config.get("max_retries", 1)

    browser = None
    context = None
    page = None

    async with sem:  # concurrency limiter
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-web-security',
                          '--disable-features=VizDisplayCompositor']
                )
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = await context.new_page()

                logger.info(f"[CHECKING] {app_name}: {url}")

                # Navigate to URL with reduced timeout
                try:
                    resp = await page.goto(url, wait_until="domcontentloaded", timeout=60_000)  # Reduced timeout
                    status = resp.status if resp else None
                    logger.debug(f"[PAGE] Page loaded with status: {status}")
                except Exception as nav_error:
                    raise Exception(f"Navigation failed: {nav_error}")

                # Run steps if defined
                if steps:
                    step_success, step_message = await run_steps(page, steps)
                    if not step_success:
                        screenshot = await take_error_screenshot(page, url, error_dir, "step_failure")
                        result = f"[STEP_FAIL] {app_name} | {url} | {step_message} | Screenshot: {screenshot}"
                        logger.error(result)
                        return result

                # Run assertions
                success, message = await run_assertions(page, url, assertions, status)

                if success:
                    result = f"[PASS] {app_name} | {url} | Status: {status}"
                    logger.info(result)
                else:
                    screenshot = await take_error_screenshot(page, url, error_dir, "assertion_failure")
                    result = f"[FAIL] {app_name} | {url} | Status: {status} | {message} | Screenshot: {screenshot}"
                    logger.error(result)

                return result

        except Exception as e:
            screenshot = "No screenshot available"
            if page and not page.is_closed():
                screenshot = await take_error_screenshot(page, url, error_dir, "exception")

            error_msg = str(e)[:200] + "..." if len(str(e)) > 200 else str(e)
            result = f"[ERROR] {app_name} | {url} | Exception: {error_msg} | Screenshot: {screenshot}"

            # Retry logic
            if retry_count < max_retries:
                logger.warning(f"[RETRY] Retrying {url} (attempt {retry_count + 1}/{max_retries + 1})")
                await asyncio.sleep(10)  # Wait before retry
                return await process_url(sem, url_config, app_name, error_dir, retry_count + 1)

            logger.error(result)
            return result

        finally:
            # Cleanup resources
            try:
                if page and not page.is_closed():
                    await page.close()
                if context:
                    await context.close()
                if browser:
                    await browser.close()
            except Exception as cleanup_error:
                logger.debug(f"[DEBUG] Cleanup error: {cleanup_error}")


# ========== Enhanced Scheduler ==========
async def schedule_url(sem, url_config: dict, app_name: str, error_dir: str):
    """Schedule URL monitoring with enhanced logging and error tracking."""
    url = url_config["url"]
    run_count = 0
    consecutive_failures = 0
    last_success = None

    while True:
        run_count += 1
        start_time = datetime.now()

        try:
            result = await process_url(sem, url_config, app_name, error_dir)
            duration = (datetime.now() - start_time).total_seconds()

            # Track success/failure patterns
            if "[PASS]" in result:
                consecutive_failures = 0
                last_success = datetime.now()
                status_text = "PASS"
            else:
                consecutive_failures += 1
                status_text = "FAIL"

            next_run = datetime.now() + timedelta(seconds=CHECK_INTERVAL)

            # Enhanced logging with more details - no emojis
            log_msg = (f"[Run {run_count:03d}] {status_text} {app_name} | {url} | "
                       f"Duration: {duration:.1f}s | "
                       f"Failures: {consecutive_failures} | "
                       f"Next: {next_run.strftime('%H:%M:%S')}")

            print(log_msg)

            # Alert on consecutive failures
            if consecutive_failures >= 3:
                logger.warning(f"[HIGH ALERT] {url} has failed {consecutive_failures} consecutive times!")

        except Exception as e:
            logger.error(f"[ERROR] Scheduler error for {url}: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


# ========== Enhanced Main Function ==========
async def main():
    """Main function with improved initialization and monitoring."""
    try:
        logger.info("[STARTUP] Starting website monitoring system...")

        config = load_config("Checks.yaml")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_dir = f"errors_{timestamp}"

        # Create directories
        Path(error_dir).mkdir(exist_ok=True)

        sem = asyncio.Semaphore(MAX_CONCURRENCY)
        tasks = []

        total_urls = 0
        for app in config.get("applications", []):
            app_name = app["name"]
            urls = app.get("urls", [])
            total_urls += len(urls)

            for url_config in urls:
                tasks.append(schedule_url(sem, url_config, app_name, error_dir))

        logger.info(
            f"[STARTUP] Started monitoring {total_urls} URLs across {len(config.get('applications', []))} applications")
        logger.info(f"[CONFIG] Concurrency: {MAX_CONCURRENCY}, Check interval: {CHECK_INTERVAL}s")
        logger.info(f"[CONFIG] Error screenshots will be saved to: {error_dir}")

        # Run all monitoring tasks
        await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logger.info("[SHUTDOWN] Monitoring stopped by user")
    except Exception as e:
        logger.error(f"[FATAL] Fatal error: {e}")
        raise
        tasks.append(schedule_url(sem, url_config, app_name, error_dir))

        tasks.append(schedule_url(sem, url_config, app_name, error_dir))

        logger.info(
            f"[STARTUP] Started monitoring {total_urls} URLs across {len(config.get('applications', []))} applications")
        logger.info(f"[CONFIG] Concurrency: {MAX_CONCURRENCY}, Check interval: {CHECK_INTERVAL}s")
        logger.info(f"[CONFIG] Error screenshots will be saved to: {error_dir}")

        # Run all monitoring tasks
        await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logger.info("[SHUTDOWN] Monitoring stopped by user")
    except Exception as e:
        logger.error(f"[FATAL] Fatal error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())