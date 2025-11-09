#!/usr/bin/env python3
from .frame import Frame


class AppFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._UI__app = self

    def __repr__(self) -> str:
        return self.__class__.__name__
