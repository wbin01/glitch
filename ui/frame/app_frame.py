#!/usr/bin/env python3
from .frame import Frame
from ..ui import UI
from ...core.signal import Signal
from ...enum.frame_shape import FrameShape
from ...enum.frame_hint import FrameHint


class AppFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        UI.__init__(self, name='AppFrame')
        self.__render_signal = Signal()
        self.__resize_signal = Signal()
        self.__state_signal = Signal()
        self._UI__app = self
        self.__hint = FrameHint.FRAME
        self.__shape = FrameShape.FRAME
        self.__visibility = 'Window.Windowed'
        self.__platform = None

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def hint(self) -> FrameHint:
        """..."""
        return self.__hint

    @hint.setter
    def hint(self, hint: FrameHint) -> None:
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

    @property
    def shape(self) -> FrameShape:
        """..."""
        return self.__shape

    @shape.setter
    def shape(self, shape: FrameShape) -> None:
        shape_values = {  # 1 default (normally Windowed)
            0: 'Window.Hidden', 1: 'Window.AutomaticVisibility',
            2: 'Window.Windowed', 3: 'Window.Minimized',
            4: 'Window.Maximized', 5: 'Window.FullScreen'}
        visibility = shape_values[shape.value]

        if self._QtObject__obj:
            if shape.value == 2:
                self._QtObject__obj.showNormal()
            elif shape.value == 4:
                self._QtObject__obj.showMaximized()
            elif shape.value == 3:
                self._QtObject__obj.showMinimized()
            elif shape.value == 5:
                self._QtObject__obj.showFullScreen()
        else:
            self._QtObject__set_property('visibility', visibility)

        self.__visibility = visibility
        self.__shape = shape
        # self.shape_signal.emit()

    @property
    def _render_signal(self):
        """..."""
        return self.__render_signal

    @property
    def _resize_signal(self):
        """..."""
        return self.__resize_signal

    @property
    def _state_signal(self):
        """..."""
        return self.__state_signal
