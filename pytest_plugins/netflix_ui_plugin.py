import pytest


class NetflixUIPlugin:
    """Class with fixtures for ui"""

    @pytest.fixture()
    def welcome_page(self, browser_driver):
        browser_driver.get('https://www.netflix.com/de/')
