import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://www.saucedemo.com"
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Chrome with a visible window (default is headless).",
    )


@pytest.fixture
def driver(request):
    options = Options()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)  # explicit waits only
    yield browser
    browser.quit()


@pytest.fixture
def logged_in_driver(driver):
    from pages.login_page import LoginPage

    login = LoginPage(driver)
    login.open()
    login.login(STANDARD_USER, PASSWORD)
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot whenever a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if browser:
            os.makedirs("screenshots", exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join("screenshots", f"{item.name}_{stamp}.png")
            browser.save_screenshot(path)
