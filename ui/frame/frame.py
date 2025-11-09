#!/usr/bin/env python3
from PySide6 import QtCore

from ..ui import UI
from ..mixin import Add
from ...core.signal import Signal
from ...enum.shape import Shape
from ...enum.hint import Hint


class Frame(Add, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        # Inheritance
        super().__init__(name='Window', base='Frame', *args, **kwargs)
        self._UI__app = self

        # Signals
        self.__hint_signal = Signal()
        self.__render_signal = Signal()
        self.__resize_signal = Signal()
        self.__shape_signal = Signal()
        self.__state_signal = Signal()
        
        # Properties
        self.__hint = Hint.FRAME
        self.__shape = Shape.FRAME
        self.__visibility = 'Window.Windowed'
        self.__platform = None

        # Flags
        self.__state_border = None

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
    def shape(self) -> Shape:
        """..."""
        return self.__shape

    @shape.setter
    def shape(self, shape: Shape = None) -> None:
        """..."""
        if shape: self.__shape = shape

        if not self._QtObject__obj:
            self._render_signal.connect(self.__max_style_qml)
            return

        if not self.__state_border:
            self.__state_border = (
                self._QtObject__property('radiusTopLeft'),
                self._QtObject__property('radiusTopRight'),
                self._QtObject__property('radiusBottomRight'),
                self._QtObject__property('radiusBottomLeft'),
                self._QtObject__property('borderColor'),
                self._QtObject__property('outLineColor'),
                self._QtObject__property('backgroundColor'))

        if self.__shape.value == 4 or self.__shape.value == 5:
            if self.__shape.value == 5:
                self._QtObject__obj.showFullScreen()
            elif self.__shape.value == 4:
                self._QtObject__obj.showMaximized()

            self._QtObject__set_property('radiusTopLeft', 0)
            self._QtObject__set_property('radiusTopRight', 0)
            self._QtObject__set_property('radiusBottomRight', 0)
            self._QtObject__set_property('radiusBottomLeft', 0)
            self._QtObject__set_property('borderColor', self.__state_border[6])
            self._QtObject__set_property('outLineColor',self.__state_border[6])
            self._QtObject__set_property('borderSpacing', 0)
        else:
            self._QtObject__set_property('borderSpacing', 1)
            if self.__shape.value == 2:
                self._QtObject__obj.showNormal()
            elif self.__shape.value == 3:
                self._QtObject__obj.showMinimized()

            # self._QtObject__obj.windowStateChanged.emit(shape.value)
            self._QtObject__set_property(
                'radiusTopLeft', self.__state_border[0])
            self._QtObject__set_property(
                'radiusTopRight', self.__state_border[1])
            self._QtObject__set_property(
                'radiusBottomRight', self.__state_border[2])
            self._QtObject__set_property(
                'radiusBottomLeft', self.__state_border[3])
            self._QtObject__set_property(
                'borderColor', self.__state_border[4])
            self._QtObject__set_property(
                'outLineColor', self.__state_border[5])

        self._shape_signal.value = self.__shape
        self._shape_signal.emit()
        self._QtObject__obj.findChild(QtCore.QObject, 'canvas').requestPaint()

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

    def close(self) -> None:
        """..."""
        if self._QtObject__obj: self._QtObject__obj.close()

    def __max_style_qml(self) -> None:
        self.shape = self.__shape
