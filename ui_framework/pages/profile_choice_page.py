from selenium.webdriver.common.by import By

from ui_framework.selenium_utils.driver_setter import DriverSetter
from ui_framework.selenium_utils.element import Element


class ProfileChoicePage(DriverSetter):
    """Profile choice page"""

    profile_label = Element(By.CSS_SELECTOR, '[data-uia="profile-choices-page"]', 'profile-choices-page')

    def check_page_opened(self):
        self.profile_label.check_presence()
