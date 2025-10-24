#!/usr/bin/env python3
from .frame import Frame
# from ...core.signal import Signal


class MainFrame(Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.mouse_press_signal = Signal()
