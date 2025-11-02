#!/usr/bin/env python3
from .view import View
from .app_close_button import AppCloseButton
from .app_max_button import AppMaxButton
from .app_min_button import AppMinButton
from ..layout.row import Row


class AppControlButtons(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        self.__qml_base = 'Layout'
        self.spacing = 6
        self.__close_btn = self._QtObject__add(AppCloseButton())
        self.__max_btn = self._QtObject__add(AppMaxButton())
        self.__min_btn = self._QtObject__add(AppMinButton())
        self._QtObject__set_property('Layout.margins', 6)
        self._QtObject__set_property('Layout.topMargin', 4)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
