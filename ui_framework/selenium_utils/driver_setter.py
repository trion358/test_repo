from ui_framework.selenium_utils.element import Element


class DriverSetter:
    def __init__(self, browser_driver):
        self.driver = browser_driver
        self.initialize_driver()

    def initialize_driver(self):
        class_obj = self.__class__.__mro__
        for class_i in class_obj:
            for _, class_name in class_i.__dict__.items():
                if isinstance(class_name, Element):
                    setattr(class_name, 'driver', self.driver)
