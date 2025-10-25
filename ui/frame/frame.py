#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add


class Frame(Add, UI):
    """..."""
    def __init__(self, name: str = 'Window', *args, **kwargs) -> None:
        super().__init__(name=name, *args, **kwargs)
        self._UI__frame = self

    def __repr__(self) -> str:
        return self.__class__.__name__
