#!/usr/bin/env python3
import pathlib

from .abstract_button import AbstractButton
from ...core.signal import Signal


class ToolButton(AbstractButton):
    def __init__(self, icon: str = None, *args, **kwargs) -> None:
        super().__init__(name='ToolButton', icon=icon, *args, **kwargs)
        # self._QtObject__set_property('implicitHeight', 32)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
