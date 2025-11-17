#!/usr/bin/env python3
from PySide6 import QtCore

from ..ui import UI
from ..mixin import Add
from ...core.signal import Signal
from ...enum.hint import Hint


class Frame(Add, UI):
    """..."""
    def __init__(self, name='BaseFrame', *args, **kwargs) -> None:
        super().__init__(name=name, base='Frame', *args, **kwargs)
        self._UI__app = self

        # Signals
        self.__hint_signal = Signal()
        self.__platform_signal = Signal()
        self.__render_signal = Signal()
        self.__resize_signal = Signal()
        
        # Properties
        self.__hint = Hint.FRAME
        self.__visibility = 'Window.Windowed'
        self.__platform = None

        # Flags
        self.__shape_border = None

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def hint(self) -> Hint:
        """..."""
        return self.__hint

    @hint.setter
    def hint(self, hint: Hint) -> None:
        hints = {
            'BOTTOM': 'Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint',
            'FRAME': 'Qt.FramelessWindowHint',
            'POPUP': 'Qt.FramelessWindowHint | Qt.Popup',
            'TOOL': 'Qt.FramelessWindowHint | Qt.Tool',
            'TOP': 'Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint'}
        if self._QtObject__obj:
            self._QtObject__set_property('flags', int(hint.value))
        else:
            self._QtObject__set_property('flags', hints[hint.name])
        
        self.__hint = hint
        self._hint_signal.emit()

    @property
    def _hint_signal(self):
        """..."""
        return self.__hint_signal

    @property
    def _platform_signal(self):
        """..."""
        return self.__platform_signal

    @property
    def _render_signal(self):
        """..."""
        return self.__render_signal

    @property
    def _resize_signal(self):
        """..."""
        return self.__resize_signal

    @property
    def _platform(self):
        """..."""
        return self.__platform

    def close(self) -> None:
        """..."""
        if self._QtObject__obj: self._QtObject__obj.close()
