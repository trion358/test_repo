# -*- coding: utf-8 -*-
"""
Модуль реализующий работу с текстовыми полями
"""
from ..element import Element


class TextField(Element):
    """Класс реализующий работу с текстовыми полями"""

    def __str__(self):
        return 'текстовое поле'
