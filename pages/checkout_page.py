from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    SUMMARY_ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")

    def fill_info(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)

    def continue_to_overview(self):
        self.click(self.CONTINUE)

    def finish(self):
        self.click(self.FINISH)

    def error_message(self):
        return self.text_of(self.ERROR)

    def summary_items(self):
        return [e.text for e in self.driver.find_elements(*self.SUMMARY_ITEM_NAMES)]

    def confirmation_text(self):
        return self.text_of(self.COMPLETE_HEADER)

    def title(self):
        return self.text_of(self.TITLE)
