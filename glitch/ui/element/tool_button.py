#!/usr/bin/env python3
from .button import Button


class ToolButton(Button):
    """Tool Button Element."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(icon_size=22, *args, **kwargs)
        self.size = self.size[1], self.size[1]
        self.class_id('ToolButton')
