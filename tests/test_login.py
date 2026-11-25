import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

PASSWORD = "secret_sauce"


@pytest.mark.smoke
@pytest.mark.regression
def test_valid_login_opens_inventory(driver):
    login = LoginPage(driver).open()
    login.login("standard_user", PASSWORD)
    assert "inventory.html" in driver.current_url
    assert InventoryPage(driver).title() == "Products"


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("standard_user", "wrong_password",
         "Username and password do not match any user in this service"),
        ("not_a_user", PASSWORD,
         "Username and password do not match any user in this service"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["wrong-password", "unknown-user", "empty-username", "empty-password", "both-empty"],
)
def test_invalid_login_shows_error(driver, username, password, expected_error):
    login = LoginPage(driver).open()
    login.login(username, password)
    assert expected_error in login.error_message()
    assert "inventory.html" not in driver.current_url


@pytest.mark.regression
def test_locked_out_user_is_blocked(driver):
    login = LoginPage(driver).open()
    login.login("locked_out_user", PASSWORD)
    assert "locked out" in login.error_message().lower()


@pytest.mark.regression
def test_logout_returns_to_login_page(logged_in_driver):
    InventoryPage(logged_in_driver).logout()
    assert LoginPage(logged_in_driver).is_present(LoginPage.LOGIN_BUTTON)
    assert "inventory.html" not in logged_in_driver.current_url
