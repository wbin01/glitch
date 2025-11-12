#!/usr/bin/env python3
from .view import View
from ...core.signal import Signal


class MinButton(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='MinButton', *args, **kwargs)
        self.__clicked_signal = Signal()

        self._app_signal.connect(
            lambda: self.__clicked_signal.connect(
                lambda: self._app._QtObject__obj.showMinimized()))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _clicked_signal(self) -> Signal:
        """..."""
        return self.__clicked_signal
