#!/usr/bin/env python3
from ..layout import Row
from .app_close_button import AppCloseButton
from .app_max_button import AppMaxButton
from .app_min_button import AppMinButton


class AppControlButtons(Row):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__close_btn = self.add(AppCloseButton())
        self.__max_btn = self.add(AppMaxButton())
        self.__min_btn = self.add(AppMinButton())
        self._QtObject__set_property('Layout.margins', 5)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
