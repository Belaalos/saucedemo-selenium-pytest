import pytest

from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.regression
def test_inventory_lists_six_products(logged_in_driver):
    assert InventoryPage(logged_in_driver).product_count() == 6


@pytest.mark.regression
def test_sort_by_name_a_to_z(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.sort_by("Name (A to Z)")
    names = page.product_names()
    assert names == sorted(names)


@pytest.mark.regression
def test_sort_by_name_z_to_a(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.sort_by("Name (Z to A)")
    names = page.product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.regression
def test_sort_by_price_low_to_high(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.sort_by("Price (low to high)")
    prices = page.product_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_by_price_high_to_low(logged_in_driver):
    page = InventoryPage(logged_in_driver)
    page.sort_by("Price (high to low)")
    prices = page.product_prices()
    assert prices == sorted(prices, reverse=True)
