from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

users = ['user1@mail.com', 'user2@mail.com', 'user3@mail.com']
passwords = ['12345gg', '123456gg', '1234567hh']


def generate_pairs():
    pairs = []
    for user in users:
        for password in passwords:
            pairs.append(pytest.param((user, password), id=f'{user}, {password}'))
    return pairs

# @pytest.mark.parametrize(
#    'creds',
#    [
#        pytest.param(('user1@mail.com', '12345gg'), id='user1@mail.com, 12345gg'),
#        pytest.param(('user2@mail.com', '123456gg'), id='user2@mail.com, 123456gg'),
#        pytest.param(('user3@mail.com', '1234567hh'), id='user3@mail.com, 1234567hh')
#    ]
# )

# @pytest.mark.skip
@pytest.mark.parametrize('creds', generate_pairs())
def test_login(creds):
    login, password = creds
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get('https://magento.softwaretestingboard.com/customer/account/login')
    driver.find_element(By.ID, 'email').send_keys(login)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.ID, 'send2').click()
    error_text = driver.find_element(By.CSS_SELECTOR, '[data-ui-id="message-error"]').text
    assert (
            'The account sign-in was incorrect or your account is disabled temporarily. '
            'Please wait and try again later.'
            == error_text
    )

@pytest.fixture()
def page(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    param = request.param
    if param == 'whats_new':
        driver.get('https://magento.softwaretestingboard.com/what-is-new.html')
    elif param == 'sale':
        driver.get('https://magento.softwaretestingboard.com/sale.html')
    return driver


@pytest.mark.parametrize('page', ['whats_new'], indirect=True)
def test_whats_new(page):
    title = page.find_element(By.CSS_SELECTOR, 'h1')
    assert title.text == 'What\'s New'


@pytest.mark.parametrize('page', ['sale'], indirect=True)
def test_sale(page):
    title = page.find_element(By.CSS_SELECTOR, 'h1')
    assert title.text == 'Sale'


