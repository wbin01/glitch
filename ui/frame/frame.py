#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add
from ...enum.align import Align


class Frame(Add, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Window', *args, **kwargs)
        self.__base = 'Frame'
        self._UI__app = self

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def _base(self) -> str:
        """..."""
        return self.__base
