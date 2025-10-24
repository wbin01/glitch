#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add


class Frame(Add, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Window', *args, **kwargs)
        self._UI__frame = self

    def __repr__(self) -> str:
        return self.__class__.__name__
