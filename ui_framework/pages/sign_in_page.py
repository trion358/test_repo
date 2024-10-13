from selenium.webdriver.common.by import By

from ui_framework.selenium_utils.driver_setter import DriverSetter
from ui_framework.selenium_utils.elements.button import Button
from ui_framework.selenium_utils.elements.text_field import TextField


class SignInPage(DriverSetter):
    """Sign in page"""

    login_input = TextField(By.CSS_SELECTOR, '[data-uia="login-field+container"] input', 'email field')
    password_input = TextField(By.CSS_SELECTOR, '[name="password"]', 'password field')
    sign_in_btn = Button(By.CSS_SELECTOR, '[type="submit"]', 'sign in button')

    def sign_in(self, login, password):
        self.login_input.type_in(login)
        self.password_input.type_in(password)
        self.sign_in_btn.click()

    def check_page_opened(self):
        self.login_input.check_presence()
