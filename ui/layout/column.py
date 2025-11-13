#!/usr/bin/env python3
from .abstract_layout import AbstractLayout


class Column(AbstractLayout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='ColumnLayout', *args, **kwargs)

    def __repr__(self) -> str:
        return self.__class__.__name__
