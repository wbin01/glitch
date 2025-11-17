#!/usr/bin/env python3
from PySide6 import QtCore

from .frame import Frame
from ...core.signal import Signal
from ...enum.shape import Shape


class MainFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='MainFrame', *args, **kwargs)
        self._UI__app = self

        # Signals
        self.__shape_signal = Signal()
        
        # Properties
        self.__shape = Shape.FRAME

        # Flags
        self.__shape_border = None

    def __repr__(self) -> str:
        return self.__class__.__name__

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

        if not self.__shape_border:
            self.__shape_border = (
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
            self._QtObject__set_property('borderColor', self.__shape_border[6])
            self._QtObject__set_property('outLineColor',self.__shape_border[6])
            self._QtObject__set_property('borderSpacing', 0)
        else:
            self._QtObject__set_property('borderSpacing', 1)
            if self.__shape.value == 2:
                self._QtObject__obj.showNormal()
            elif self.__shape.value == 3:
                self._QtObject__obj.showMinimized()

            # self._QtObject__obj.windowStateChanged.emit(shape.value)
            self._QtObject__set_property(
                'radiusTopLeft', self.__shape_border[0])
            self._QtObject__set_property(
                'radiusTopRight', self.__shape_border[1])
            self._QtObject__set_property(
                'radiusBottomRight', self.__shape_border[2])
            self._QtObject__set_property(
                'radiusBottomLeft', self.__shape_border[3])
            self._QtObject__set_property(
                'borderColor', self.__shape_border[4])
            self._QtObject__set_property(
                'outLineColor', self.__shape_border[5])

        self._shape_signal.value = self.__shape
        self._shape_signal.emit()
        self._QtObject__obj.findChild(QtCore.QObject, 'canvas').requestPaint()

    @property
    def _shape_signal(self):
        """..."""
        return self.__shape_signal
