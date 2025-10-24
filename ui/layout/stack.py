#!/usr/bin/env python3
from .layout import Layout


class Stack(Layout):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(name='StackLayout', *args, **kwargs)
