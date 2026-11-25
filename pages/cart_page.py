from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import TIMEOUT, BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def title(self):
        return self.text_of(self.TITLE)

    def item_names(self):
        # Re-query inside the wait so a re-rendered DOM (stale element) is retried.
        try:
            return WebDriverWait(
                self.driver, TIMEOUT, ignored_exceptions=(StaleElementReferenceException,)
            ).until(lambda d: [e.text for e in d.find_elements(*self.ITEM_NAMES)] or None)
        except TimeoutException:
            return []

    def remove(self, product_name):
        slug = product_name.lower().replace(" ", "-")
        self.click((By.ID, f"remove-{slug}"))

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
