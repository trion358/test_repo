import os
from datetime import datetime
import pytest

from configs.config import get_env_configs
from pytest_plugins.netflix_ui_plugin import NetflixUIPlugin
from ui_framework.selenium_utils.driver import start_driver


DEFAULT_ENV = "preprod"
# SELENOID_HUB_ADDRESS = 'http://172.20.0.24:4444'
SELENOID_HUB_ADDRESS = 'http://127.0.0.1:4444'  # uncomment for local run


def pytest_configure(config):
    """Auto calling function for managing plugins."""

    plugin_list = {
                   "netflix ui plugin": NetflixUIPlugin(),
                  }

    for plugin in plugin_list.values():
        config.pluginmanager.register(plugin)


@pytest.fixture(name="config", scope="session")
def get_config():
    config_dict = get_env_configs()
    return config_dict


@pytest.fixture(name="browser_driver")
def go_driver(request):

    driver = start_driver(request.node.name, SELENOID_HUB_ADDRESS)

    temp_screenshots_folder_path = os.path.join(os.path.dirname(__file__), "..", "temp", "screenshot")

    if not os.path.exists(temp_screenshots_folder_path):
        os.makedirs(temp_screenshots_folder_path, exist_ok=True)

    yield driver

    screenshot_name = os.path.basename(request.config.args[0].replace(':', '_').replace('/', '_')) + datetime.now().strftime(
        "_%d-%m_%H-%M-%S") + '.png'

    screenshot_path = os.path.join(temp_screenshots_folder_path, screenshot_name)
    driver.save_screenshot(screenshot_path)
    driver.quit()
