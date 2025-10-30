#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add


class Frame(UI, Add):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Frame')
        self._base = 'Frame'
        self._UI__app = self

    def __repr__(self) -> str:
        return self.__class__.__name__
