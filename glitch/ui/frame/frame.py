#!/usr/bin/env python3
from ..base import Frame


class Frame(Frame):
    """An application frame.

    A frame where visual elements are inserted. Usually called a "Window".
    It is not the main Frame of an application, and it has no movement 
    capabilities. It is ideal as a part of the main application, such as a 
    context menu or a tool panel.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.class_id('Frame')
