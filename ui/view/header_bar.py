#!/usr/bin/env python3
from ..layout import Row
from .app_control_buttons import AppControlButtons
from .app_max_button import AppMaxButton
from .app_min_button import AppMinButton


class HeaderBar(Row):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__control_buttons = self.add(AppControlButtons())
        # self._QtObject__set_property('Layout.margins', 5)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
