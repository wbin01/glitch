#!/usr/bin/env python3
from .abstract_button import AbstractButton
from ...core.signal import Signal


class Button(AbstractButton):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__text = text

        if self.__text:
            self._QtObject__set_property('text', self.__text)
        self._QtObject__set_property('Layout.fillWidth', 'true')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text={self.__text!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__text!r})'

    @property
    def text(self) -> str:
        """..."""
        return self._QtObject__property('text')

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text
        self._QtObject__set_property('text', text)
