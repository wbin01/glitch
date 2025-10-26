#!/usr/bin/env python3
from ..ui import UI
from ...core.signal import Signal


class View(UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return self.__class__.__name__
