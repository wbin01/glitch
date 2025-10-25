#!/usr/bin/env python3
from .frame import Frame
# from ...core.signal import Signal


# class MainFrame(Frame):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         # self.mouse_press_signal = Signal()


class MainFrame(Frame):
    """..."""
    def __init__(self, name: str = 'MainFrame', *args, **kwargs) -> None:
        super().__init__(name=name, *args, **kwargs)
        # self._QtObject__name = 'MainFrame'

    def __repr__(self) -> str:
        return self.__class__.__name__
