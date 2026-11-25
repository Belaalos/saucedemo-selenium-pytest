from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def title(self):
        return self.text_of(self.TITLE)

    def item_names(self):
        if not self.is_present(self.ITEM_NAMES):
            return []
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove(self, product_name):
        slug = product_name.lower().replace(" ", "-")
        self.click((By.ID, f"remove-{slug}"))

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
