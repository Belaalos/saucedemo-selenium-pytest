from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 10


class BasePage:
    """Shared helpers for all page objects (explicit waits, common actions)."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0
