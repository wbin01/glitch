#!/usr/bin/env python3
from .layout import Layout


class Row(Layout):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
