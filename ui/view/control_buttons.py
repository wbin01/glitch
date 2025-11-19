#!/usr/bin/env python3
from .view import View
from .close_button import CloseButton
from .max_button import MaxButton
from .min_button import MinButton
from ..layout.row import Row


class ControlButtons(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        self.__qml_base = 'Layout'
        self.spacing = 6
        self.__close_btn = self._QtObject__add(CloseButton())
        self.__max_btn = self._QtObject__add(MaxButton())
        self.__min_btn = self._QtObject__add(MinButton())
        self._QtObject__set_property('Layout.margins', 6)
        self._QtObject__set_property('Layout.topMargin', 5)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
