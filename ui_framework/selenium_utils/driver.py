import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def start_driver(test_name, hub_address):
    video_name = f"{test_name.replace('[', '_').replace(']', '_')}" \
                 f"_{datetime.today().strftime('%Y-%m-%d_%H:%M')}"

    driver = _CommonBrowserDriver(selenium_hub_address=hub_address,
                                  video_name=video_name,
                                  test_name=test_name)

    return driver


class _CommonBrowserDriver(webdriver.Remote):
    """Class to work with browser."""

    def __init__(self, selenium_hub_address, test_name, video_name):
        self.selenium_hub_url = selenium_hub_address + "/wd/hub"

        options = Options()

        selenoid_options = {'enableVNC': True,
                            'enableVideo': True,
                            'sessionTimeout': '30m',
                            'videoName': video_name + ".mp4",
                            'name': f"{test_name}"}

        options.set_capability('selenoid:options', selenoid_options)
        options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-popup-blocking")

        super().__init__(command_executor=self.selenium_hub_url,
                         options=options)

        self.logger = logging.getLogger("TestLogger")
