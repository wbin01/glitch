#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add


class Frame(UI, Add):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Frame')
        self._base = 'Frame'
        self._UI__frame = self
        self.__platform = None
        self.__platform_added_signal = Signal()

    def __repr__(self) -> str:
        return self.__class__.__name__
