#!/usr/bin/env python3
from PySide6 import QtCore

from .control_buttons import ControlButtons
from .expander import Expander
from .image import Image
from .label import Label
from .view import View
from ..layout import Row
from ...enum.shape import Shape


class Header(View):
    def __init__(self, text: str = '', *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        # set
        self.__qml_base = 'Layout'
        self._QtObject__set_property('spacing', 0)
        self._QtObject__set_property('Layout.fillWidth', 'true')
        self._QtObject__set_property('Layout.fillHeight', 'false')
        self.__resize = False
        self.__active_color = None
        self.__active_color_bd = None
        self.__inactive_color = None
        self.__inactive_color_bd = None

        # Flags
        self.__side = 'left'
        self.__rwidth = 0
        self.__lwidth = 0
        self.__margin_delta = 0
        self.__stop = False
        self.__left_count = 0
        self.__right_count = 0

        # Left
        self.__control_l = self._QtObject__add(ControlButtons(0))
        self.__left = self._QtObject__add(Row())
        self.__left.spacing = 6
        self.__left.margin = 2, 0, 0, 2 if self.__control_l._count else 0
        
        self.__left_plus = self._QtObject__add(Expander())
        self.__left_plus._QtObject__set_property('property int lw', 0)
        self.__left_plus._QtObject__set_property('Layout.preferredWidth', 'lw')
        self.__left_plus.margin = 0

        # Text
        self.__left_span = self._QtObject__add(Expander(horizontal=True))
        self.__text = self._QtObject__add(Label(text))
        self.__right_span = self._QtObject__add(Expander(horizontal=True))

        # Right
        self.__right_plus = self._QtObject__add(Expander())
        self.__right_plus._QtObject__set_property('property int rw', 0)
        self.__right_plus._QtObject__set_property('Layout.preferredWidth','rw')
        self.__right_plus.margin = 0

        self.__right = self._QtObject__add(Row())
        self.__right.spacing = 6
        self.__control_r = self._QtObject__add(ControlButtons(1))
        self.__right.margin = 2, 0, 0, 2 if self.__control_r._count else 0

        self._app_signal.connect(self.__signals_conf)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def spacing(self) -> int:
        """..."""
        return self.__left.spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self.__left.spacing = spacing
        self.__right.spacing = spacing
    
    @property
    def text(self) -> str:
        return self.__text.text

    @text.setter
    def text(self, text: str) -> None:
        self.__text.text = text

    def add(self, item: View, right: bool = False) -> View:
        """..."""
        if right:
            self.__right_count += 1
            return self.__right.add(item)

        self.__left_count += 1
        return self.__left.add(item)

    def __center_title(self, shape=False) -> None:
        # Size vars
        ratio = self._app._QtObject__obj.devicePixelRatio()

        control_l = self.__control_l.width[0]
        left = self.__left.width[0]
        left_plus = self.__left_plus.width[0]
        left_span = self.__left_span.width[0]

        title = self.__text.width[0]

        right_span = self.__right_span.width[0]
        right_plus = self.__right_plus.width[0]
        right = self.__right.width[0]
        control_r = self.__control_r.width[0]

        window = self._app.width[0]
        
        if not self.__control_l.visible: control_l = 0
        if not self.__control_r.visible: control_r = 0

        if not self.__left_count and left != 32: self.__left.width = 32
        if not self.__right_count and right != 32: self.__right.width = 32

        # New stop point
        used_area = control_l + left + title + right + control_r
        self.__stop = True if window < used_area + 20 else False
        if self.__stop:
            self.__right_plus._QtObject__set_property('rw', 5)
            self.__left_plus._QtObject__set_property('lw', 5)
            return

        # Signals
        if shape:
            self.__right_plus._QtObject__set_property('rw', 0)
            self.__left_plus._QtObject__set_property('lw', 0)
            self.__stop = False
            QtCore.QTimer.singleShot(50, self.__center_title)

        if not self.__resize:
            self._app._resize_signal.connect(self.__center_title)
            self.__resize = True

        # Equal sides +
        left_side = control_l + left
        if left_side < 0: left_side = 0

        right_side = right + control_r
        if right_side < 0: right_side = 0
        
        if left_side > right_side:
            self.__rwidth = int(left_side - right_side)
            self.__side = 'right'
            self.__margin_delta = self.__rwidth
            rwidth = 0 if self.__stop else self.__rwidth
            self.__right_plus._QtObject__set_property('rw', rwidth)
        else:
            self.__lwidth = int(right_side - left_side)
            self.__side = 'left'
            self.__margin_delta = self.__lwidth
            lwidth = 0 if self.__stop else self.__lwidth
            self.__left_plus._QtObject__set_property('lw', lwidth)

        # Equal sides -
        total_left = left_side + left_plus + left_span
        total_right = right_side + right_plus + right_span
        dt = (total_left + title + total_right + 20) - window

        rwidth = right_plus - dt
        if self.__side == 'right' and not right_span and rwidth > 2:
            if self.__stop: rwidth = 5
            if self.__margin_delta > right_plus - dt:
                self.__right_plus._QtObject__set_property('rw', rwidth)

        lwidth = left_plus - dt
        if self.__side == 'left' and not left_span and lwidth > 2:
            if self.__stop: lwidth = 5
            if self.__margin_delta > left_plus - dt:
                self.__left_plus._QtObject__set_property('lw', lwidth)

    def __on_active_signal(self) -> None:
        if not self.__active_color:
            self.__active_color = self._app._platform.style[
                '[MainFrame]']['background_color']

        if not self.__active_color_bd:
            self.__active_color_bd = self._app._platform.style[
                '[MainFrame]']['border_color']
        
        self._app._QtObject__set_property(
            'backgroundColor', self.__active_color)

        self._app._QtObject__set_property(
            'borderColor', self.__active_color_bd)
        
        self._app._QtObject__obj.findChild(
            QtCore.QObject, 'canvas').requestPaint()

    def __on_inactive_signal(self) -> None:
        if not self.__inactive_color:
            self.__inactive_color = self._app._platform.style[
                '[MainFrame:inactive]']['background_color']

        if not self.__inactive_color_bd:
            self.__inactive_color_bd = self._app._platform.style[
                '[MainFrame:inactive]']['border_color']

        self._app._QtObject__set_property(
            'backgroundColor', self.__inactive_color)

        self._app._QtObject__set_property(
            'borderColor', self.__inactive_color_bd)
        
        self._app._QtObject__obj.findChild(
            QtCore.QObject, 'canvas').requestPaint()

    def __on_shape_signal(self) -> None:
        if self._app._platform.global_menu:
            if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
                if self.__control_l.visible:
                    self.__control_l.visible = False
                    self.__control_r.visible = False
            else:
                self.__control_l.visible = True
                self.__control_r.visible = True

        self.__center_title(True)

    def __set_active_inactive_signal(self) -> None:
        if self._app._platform.de == 'lxqt':
            self._app._QtObject__set_property('borderWidth', 2)
        
        self._app._active_signal.connect(self.__on_active_signal)
        self._app._inactive_signal.connect(self.__on_inactive_signal)

    def __shape_signal_thread(self) -> None:
        QtCore.QTimer.singleShot(100, self.__on_shape_signal)

    def __signals_conf(self) -> None:
        self._app._render_signal.connect(self.__center_title)
        self._app._render_signal.connect(self.__set_active_inactive_signal)
        
        if hasattr(self._app, '_shape_signal'):
            self._app._shape_signal.connect(self.__shape_signal_thread)
