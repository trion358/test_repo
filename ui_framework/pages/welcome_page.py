from selenium.webdriver.common.by import By

from ui_framework.selenium_utils.driver_setter import DriverSetter
from ui_framework.selenium_utils.elements.button import Button


class WelcomePage(DriverSetter):
    """Welcome page"""

    sign_in_btn = Button(By.CSS_SELECTOR, '[data-uia="header-login-link"]', 'sign in button')

    def go_to_sign_in(self):
        self.sign_in_btn.click()
