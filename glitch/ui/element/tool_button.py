#!/usr/bin/env python3
from .button import Button


class ToolButton(Button):
    """Tool Button Element."""
    def __init__(self, icon: str, icon_size: int =22, *args, **kwargs) -> None:
        super().__init__(text='', icon=icon, icon_size=icon_size, *args, **kwargs)
        self.size = self.size[1], self.size[1]
        self.class_id('ToolButton')
