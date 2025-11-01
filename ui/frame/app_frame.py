#!/usr/bin/env python3
from PySide6 import QtCore
import subprocess

from .frame import Frame
from ..ui import UI
from ...core.signal import Signal
from ...enum.frame_shape import FrameShape
from ...enum.frame_hint import FrameHint


class AppFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        UI.__init__(self, name='AppFrame')
        self.__hint_signal = Signal()
        self.__render_signal = Signal()
        self.__resize_signal = Signal()
        self.__shape_signal = Signal()
        self.__state_signal = Signal()
        # self.__platform_signal = Signal()
        
        self.__hint = FrameHint.FRAME
        self.__shape = FrameShape.FRAME
        self.__visibility = 'Window.Windowed'
        self._UI__app = self

        self.__platform = None
        self.__state_border = None

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
        self._hint_signal.emit()

    @property
    def shape(self) -> FrameShape:
        """..."""
        return self.__shape

    @shape.setter
    def shape(self, shape: FrameShape = None) -> None:
        """..."""
        if shape: self.__shape = shape

        if not self._QtObject__obj:
            self._render_signal.connect(self.__max_style_qml)
            return

        if not self.__state_border:
            self.__state_border = (
                self._QtObject__obj.property('radiusTopLeft'),
                self._QtObject__obj.property('radiusTopRight'),
                self._QtObject__obj.property('radiusBottomRight'),
                self._QtObject__obj.property('radiusBottomLeft'),
                self._QtObject__obj.property('borderColor'),
                self._QtObject__obj.property('outLineColor'),
                self._QtObject__obj.property('backgroundColor'))

        if self.__shape.value == 4 or self.__shape.value == 5:
            if self.__shape.value == 5:
                self._QtObject__obj.showFullScreen()
            elif self.__shape.value == 4:
                self._QtObject__obj.showMaximized()

            self._QtObject__obj.setProperty('radiusTopLeft', 0)
            self._QtObject__obj.setProperty('radiusTopRight', 0)
            self._QtObject__obj.setProperty('radiusBottomRight', 0)
            self._QtObject__obj.setProperty('radiusBottomLeft', 0)
            self._QtObject__obj.setProperty(
                'borderColor', self.__state_border[6])
            self._QtObject__obj.setProperty(
                'outLineColor',self.__state_border[6])
            self._QtObject__obj.setProperty('borderSpacing', 0)
        else:
            self._QtObject__obj.setProperty('borderSpacing', 1)
            if self.__shape.value == 2:
                self._QtObject__obj.showNormal()
            elif self.__shape.value == 3:
                self._QtObject__obj.showMinimized()

            # self._QtObject__obj.windowStateChanged.emit(shape.value)
            self._QtObject__obj.setProperty(
                'radiusTopLeft', self.__state_border[0])
            self._QtObject__obj.setProperty(
                'radiusTopRight', self.__state_border[1])
            self._QtObject__obj.setProperty(
                'radiusBottomRight', self.__state_border[2])
            self._QtObject__obj.setProperty(
                'radiusBottomLeft', self.__state_border[3])
            self._QtObject__obj.setProperty(
                'borderColor', self.__state_border[4])
            self._QtObject__obj.setProperty(
                'outLineColor', self.__state_border[5])

        self._shape_signal.value = self.__shape
        self._shape_signal.emit()
        self._QtObject__obj.findChild(QtCore.QObject, 'canvas').requestPaint()

    def __max_style_qml(self) -> None:
        self.shape = self.__shape

    @property
    def _hint_signal(self):
        """..."""
        return self.__hint_signal

    @property
    def _render_signal(self):
        """..."""
        return self.__render_signal

    @property
    def _resize_signal(self):
        """..."""
        return self.__resize_signal

    @property
    def _shape_signal(self):
        """..."""
        return self.__shape_signal

    @property
    def _state_signal(self):
        """..."""
        return self.__state_signal
