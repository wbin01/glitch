#!/usr/bin/env python3
import pathlib

from .abstract_button import AbstractButton
from ...core.signal import Signal


class ToolButton(AbstractButton):
    def __init__(self, icon_source: str = None, *args, **kwargs) -> None:
        super().__init__(name='ToolButton', *args, **kwargs)

        self.__icon = icon_source if icon_source else pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'empty.svg'
        if self.__icon:
            self._QtObject__set_property('icon.source', self.__icon)
        # self._QtObject__set_property('checkable', 'true')
        # self._QtObject__set_property(
        #     'onToggled', 'console.log("Estado:", checked)')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(icon_source={self.__icon!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__icon!r})'
