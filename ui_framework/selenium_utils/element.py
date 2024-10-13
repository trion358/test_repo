import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    JavascriptException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Element:
    """Поиск элементов, драйвер подкидывается на лету в driver setter"""

    def __init__(self, how: str, locator: str, rus_name: str):

        self.how = how
        self.locator = locator
        self.rus_name = rus_name
        self.webelement = None

    def __call__(self, contains_text='', index=None, timeout=3, strict_visible=True):
        return self.find_elements(contains_text=contains_text, index=index,
                                  timeout=timeout)

    def find_elements(self, timeout=5, frequency=0.2, contains_text='',
                      index=None):

        """Обертка для поиска элементов

        :param timeout: как долго пытаемся найти элемент
        :param frequency: частота попыток поиска элемента
        :param contains_text: текст, который должен содержаться в элементе
        :param index: индекс элемента в списке найденных элементов
        """

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        try:

            elements = wait.until(EC.visibility_of_any_elements_located((self.how, self.locator)),
                                  f'Не отображается элемент')

        except TimeoutException:
            raise NoSuchElementException(f"Не найден элемент"
                                         f" '{self.locator, self.rus_name}',"
                                         f" содержащий текст {contains_text}")

        if len(elements) == 1:
            self.webelement = elements[0]
            return elements[0]
        elif len(elements) > 1 and contains_text:
            try:
                self.webelement = [element for element in elements if contains_text.lower() in element.text.lower()][0]
            except IndexError:
                raise NoSuchElementException(f'No elements that contain text {contains_text}')
            return self.webelement

        elif len(elements) > 1 and index is not None:
            try:
                self.webelement = elements[index]
            except IndexError:
                raise NoSuchElementException(f'No elements that might be took with index')
            return self.webelement

        elif len(elements) > 1:
            self.webelement = elements
            return elements

    def appear_shadow(self, color: str):
        script = f"""
                    arguments[0].style.boxShadow = 'inset 0 0 0 3px {color}';
                    setTimeout(function() {{
                        arguments[0].style.boxShadow = '';
                    }}, 800);
                """
        try:
            self.driver.execute_script(script, self.webelement)
        except JavascriptException:
            pass

    def delete_shadow(self):
        try:
            self.driver.execute_script(
                "const node = arguments[0]; setTimeout(function(){ node.style.boxShadow = ''; }"
                " , 1500)", self.webelement)
        except (TimeoutException, StaleElementReferenceException, NoSuchElementException):
            pass

    def check_presence(self, visibility=True, timeout=8):
        """Проверяем отображение элемента на странице

        :param visibility:присутствует или нет
        :param timeout: Сколько времени ждем преждем чем выдать исключение
        """

        wait = WebDriverWait(self.driver, timeout)

        if visibility:
            wait.until(EC.visibility_of_element_located((self.how, self.locator)),
                       f'Не отображается элемент {self.locator, self.rus_name}')
        else:
            wait.until(EC.invisibility_of_element_located((self.how, self.locator)),
                       f'Элемент {self.locator, self.rus_name} не должен отображаться')

    def click(self):
        """Производим клик по элементу"""

        self.find_elements()
        self.appear_shadow('red')
        self.webelement.click()
        self.delete_shadow()

    def type_in(self, text: str, clear=True):
        """Возвращает True, если webelement отображается для пользователя

        :param text: текст для ввода
        :param clear: очищать поле ввода
        """
        if clear:
            self.clear()
        self.appear_shadow('red')
        self._wait(lambda: self.find_elements().send_keys(text))
        self.delete_shadow()

    def should_be(self, contains_text='', input_field=False):

        self._wait(lambda: self.find_elements())
        if contains_text:
            if not input_field:
                element_text = self.webelement.text.lower()
            else:
                element_text = self.webelement.get_attribute('value').lower()
            assert contains_text.lower() in element_text,\
                f'No text {contains_text} in element {self.rus_name, self.locator},' \
                f' displayed text is {self.webelement.text}'

    def clear(self):
        result = self._wait(lambda: self.find_elements().clear())
        return result

    @property
    def text(self):
        """Возвращает текст, который содержит webelement"""

        result = self._wait(lambda: self.find_elements().text)
        if not result:
            result = ''
        return result

    @staticmethod
    def _wait(action, wait_time=5):
        """Метод в качестве параметра получает функцию action

        Ждет пока функция не вернет True
        Если не возвращает, то вернет в конце результат выполнения функции.

        :param action: действие которое ожиданем
        :param wait_time: время ожидания
        """

        end_time = time.time() + wait_time

        res = False
        while True:
            try:
                res = action()
                if res is not False:
                    return res
                tmp_err = None
            except Exception as error:
                tmp_err = error

            if time.time() > end_time:
                break
            time.sleep(0.1)

        if not res and tmp_err is None:
            return False
        else:
            return tmp_err
