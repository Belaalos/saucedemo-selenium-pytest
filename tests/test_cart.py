import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
@pytest.mark.regression
def test_add_item_updates_cart_badge(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.add_to_cart(BACKPACK)
    assert page.cart_count() == 1


@pytest.mark.regression
def test_add_multiple_items_updates_badge(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.add_to_cart(BACKPACK)
    page.add_to_cart(BIKE_LIGHT)
    assert page.cart_count() == 2


@pytest.mark.regression
def test_remove_item_from_inventory_clears_badge(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.add_to_cart(BACKPACK)
    page.remove_from_cart(BACKPACK)
    assert page.cart_count() == 0


@pytest.mark.regression
def test_cart_page_shows_added_items(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.add_to_cart(BACKPACK)
    page.add_to_cart(BIKE_LIGHT)
    page.open_cart()
    cart = CartPage(logged_in_driver)
    assert cart.title() == "Your Cart"
    assert sorted(cart.item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.regression
def test_remove_item_from_cart_page(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.add_to_cart(BACKPACK)
    page.open_cart()
    cart = CartPage(logged_in_driver)
    cart.remove(BACKPACK)
    assert cart.item_names() == []
