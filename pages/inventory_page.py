from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    @staticmethod
    def _slug(product_name):
        return product_name.lower().replace(" ", "-")

    def title(self):
        return self.text_of(self.TITLE)

    def product_count(self):
        return len(self.find_all(self.ITEMS))

    def product_names(self):
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def product_prices(self):
        return [float(e.text.replace("$", "")) for e in self.find_all(self.ITEM_PRICES)]

    def add_to_cart(self, product_name):
        self.click((By.ID, f"add-to-cart-{self._slug(product_name)}"))

    def remove_from_cart(self, product_name):
        self.click((By.ID, f"remove-{self._slug(product_name)}"))

    def cart_count(self):
        """Number shown on the cart badge; 0 when the badge is absent."""
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def sort_by(self, visible_text):
        Select(self.find(self.SORT)).select_by_visible_text(visible_text)

    def open_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
