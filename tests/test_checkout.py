import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"


def go_to_checkout_form(driver):
    inventory = InventoryPage(driver)
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()
    CartPage(driver).checkout()
    return CheckoutPage(driver)


@pytest.mark.smoke
@pytest.mark.regression
def test_complete_purchase_end_to_end(logged_in_driver):
    checkout = go_to_checkout_form(logged_in_driver)
    checkout.fill_info("Belal", "Magdy", "11341")
    checkout.continue_to_overview()
    assert BACKPACK in checkout.summary_items()
    checkout.finish()
    assert checkout.confirmation_text() == "Thank you for your order!"


@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Magdy", "11341", "First Name is required"),
        ("Belal", "", "11341", "Last Name is required"),
        ("Belal", "Magdy", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_form_validation(logged_in_driver, first, last, postal, expected_error):
    checkout = go_to_checkout_form(logged_in_driver)
    checkout.fill_info(first, last, postal)
    checkout.continue_to_overview()
    assert expected_error in checkout.error_message()


@pytest.mark.regression
def test_checkout_overview_lists_cart_items(logged_in_driver):
    checkout = go_to_checkout_form(logged_in_driver)
    checkout.fill_info("Belal", "Magdy", "11341")
    checkout.continue_to_overview()
    assert checkout.title() == "Checkout: Overview"
    assert checkout.summary_items() == [BACKPACK]
