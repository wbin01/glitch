#!/usr/bin/env python3
from .view import View
from ...core.signal import Signal


class ToolButton(View):
    def __init__(self, icon_source: str = None, *args, **kwargs) -> None:
        super().__init__(name='ToolButton', *args, **kwargs)
        self.__mouse_press_signal = Signal()
        self.__icon = icon_source
        if self.__icon:
            self._QtObject__set_property('icon.source', self.__icon)
        # self._QtObject__set_property('checkable', 'true')
        # self._QtObject__set_property(
        #     'onToggled', 'console.log("Estado:", checked)')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _mouse_press_signal(self) -> Signal:
        """..."""
        return self.__mouse_press_signal
