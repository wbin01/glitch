#!/usr/bin/env python3
from enum import Enum

from PySide6 import QtCore


class FrameHint(Enum):
    """Frame hint enumeration.

    FrameHint.BOTTOM → Always behind.
    FrameHint.FRAME → Normal behavior.
    FrameHint.POPUP → Popup Frame (does not appear in the taskbar).
    FrameHint.TOOL → Tool-like Frame (does not appear in the taskbar).
    FrameHint.TOP → Always on top.

    Use `FrameHint.TOOL` and `FrameHint.POPUP` inside a method to activate 
    them only when the window is ready; this will avoid styling issues.

    Use the `name` property to know which `FrameHint` it is.
    
    >>> self.frame_hint = FrameHint.FRAME
    >>> print(self.frame_hint.name)
    FRAME
    """
    BOTTOM = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint
    FRAME = QtCore.Qt.FramelessWindowHint
    POPUP = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup
    TOOL = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool
    TOP = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint

    # Janela tipo ferramenta (não aparece na barra de tarefas)
    # Qt.Tool
    # Controlam botões
    # Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint

    def __repr__(self) -> str:
        return self.__class__.__name__
