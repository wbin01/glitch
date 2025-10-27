#!/usr/bin/env python3
from .view import View
from ...core.signal import Signal


class AppCloseButton(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='AppCloseButton', *args, **kwargs)
        self.__mouse_press_signal = Signal()

        self._app_signal.connect(
            lambda: self.__mouse_press_signal.connect(  # window().close()
                lambda: self._app._QtObject__obj.close()))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _mouse_press_signal(self) -> Signal:
        """..."""
        return self.__mouse_press_signal
