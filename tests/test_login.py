from ui_framework.pages.profile_choice_page import ProfileChoicePage
from ui_framework.pages.sign_in_page import SignInPage
from ui_framework.pages.welcome_page import WelcomePage


def test_authorisation(welcome_page, browser_driver, config):

    welcome_page = WelcomePage(browser_driver)
    welcome_page.go_to_sign_in()

    sign_in_page = SignInPage(browser_driver)
    sign_in_page.sign_in(config['credentials']['super_user']['login'],
                         config['credentials']['super_user']['password'])

    profile_choice_page = ProfileChoicePage(browser_driver)
    profile_choice_page.check_page_opened()
