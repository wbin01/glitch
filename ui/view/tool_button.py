#!/usr/bin/env python3
import pathlib

from .abstract_button import AbstractButton
from ...core.signal import Signal


class ToolButton(AbstractButton):
    def __init__(self, icon: str = None, *args, **kwargs) -> None:
        super().__init__(name='ToolButton', icon=icon, *args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(icon_source={self.__icon!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__icon!r})'
