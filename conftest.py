import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from data import urls, input_data, page_elements_data
from data.utils import rand_index

from locators.locators_saucedemo import LoginPageLocators as LPL
from locators.locators_saucedemo import InventoryPageLocators as IPL
from locators.locators_saucedemo import ItemCardDetailLocators as ICD
from locators.locators_saucedemo import CartPageLocators as CPL


@pytest.fixture()
def browser():
    """Chrome webdriver initialization"""

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture()
def auth_positive(browser):
    """Fixture: Positive authentication on the https://www.saucedemo.com"""

    browser.get(urls.BASE_URL)

    browser.find_element(*LPL.USERNAME_FIELD).send_keys(input_data.username_valid)
    browser.find_element(*LPL.PASSWORD_FIELD).send_keys(input_data.password_valid)

    browser.find_element(*LPL.LOGIN_BUTTON).click()


@pytest.fixture()
def add_item_to_cart_through_catalog(browser, auth_positive):
    """Fixture: add item to cart through catalog"""

    list_catalog_items = browser.find_elements(*IPL.INVENTORY_ITEMS)
    list_add_to_cart_btn = browser.find_elements(*IPL.ADD_TO_CART_BUTTON)

    selected_item_idx = rand_index(len(list_catalog_items))
    selected_item_name = list_catalog_items[selected_item_idx].text.split("\n")[0]

    list_add_to_cart_btn[selected_item_idx].click()
    numbers_of_items_in_shop_cart = int(browser.find_element(*IPL.SHOPPING_CART_BADGE).text)

    assert selected_item_name in page_elements_data.catalog_items_names, \
        "The selected item not present in catalog"
    assert numbers_of_items_in_shop_cart == page_elements_data.count_items_in_cart[0], \
        f"The number in shopping cart badge is different than {page_elements_data.count_items_in_cart[0]}"


@pytest.fixture()
def add_item_to_cart_through_item_card(browser, auth_positive):
    """Fixture: add item to cart through item card"""

    list_catalog_items = browser.find_elements(*IPL.INVENTORY_ITEMS)
    list_items_card_link = browser.find_elements(*IPL.INVENTORY_ITEMS_CARD_LINK_IMAGE)
    selected_item_idx = rand_index(len(list_catalog_items))
    selected_item_name_catalog = list_catalog_items[selected_item_idx].text.split("\n")[0]

    list_items_card_link[selected_item_idx].click()

    selected_item_name_product_card = browser.find_element(*ICD.ITEM_NAME).text.split("\n")[0]

    assert selected_item_name_product_card == selected_item_name_catalog, \
        "Item at the item's card details and catalog are different"

    browser.find_element(*ICD.ADD_TO_CART_BUTTON).click()

    numbers_of_items_in_shop_cart_in_badge = int(browser.find_element(*IPL.SHOPPING_CART_BADGE).text)

    assert numbers_of_items_in_shop_cart_in_badge == page_elements_data.count_items_in_cart[0], \
        f"The number in shopping cart badge is different than {page_elements_data.count_items_in_cart[0]}"


@pytest.fixture()
def check_exist_item_in_cart(browser, auth_positive):
    """Fixture: check the added item in shopping cart"""

    browser.find_element(*IPL.SHOPPING_CART_BADGE).click()

    amount_items_in_cart = len(browser.find_elements(*CPL.CART_ITEMS))

    assert amount_items_in_cart == page_elements_data.count_items_in_cart[0], \
        f"The amount is different than {page_elements_data.count_items_in_cart[0]} or cart is empty"
