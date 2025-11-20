#!/usr/bin/env python3
from PySide6.QtCore import QTimer

from .control_buttons import ControlButtons
from .expander import Expander
from .image import Image
from .label import Label
from .view import View
from ..layout import Row
from ...enum.shape import Shape


class Header(View):
    def __init__(self, text: str = 'Header text', *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        # set
        self.__qml_base = 'Layout'
        self._QtObject__set_property('spacing', 0)
        self._QtObject__set_property('Layout.fillWidth', 'true')
        self._QtObject__set_property('Layout.fillHeight', 'false')
        self.__resize = False

        # Flags
        self.__side = 'left'
        self.__rwidth = 0
        self.__lwidth = 0
        self.__margin_delta = 0
        self.__stop = False

        # Left
        self.__control_buttons = self._QtObject__add(ControlButtons())
        self.__left = self._QtObject__add(Row())
        self.__left.spacing = 6
        self.__left._QtObject__set_property('Layout.topMargin', 2)
        
        self.__left_plus = self._QtObject__add(Expander())
        self.__left_plus._QtObject__set_property('property int lw', 0)
        self.__left_plus._QtObject__set_property('Layout.preferredWidth', 'lw')

        # Text
        self.__left_span = self._QtObject__add(Expander(horizontal=True))
        self.__text = self._QtObject__add(Label(text))
        self.__right_span = self._QtObject__add(Expander(horizontal=True))

        # Right
        self.__right_plus = self._QtObject__add(Expander())
        self.__right_plus._QtObject__set_property('property int rw', 0)
        self.__right_plus._QtObject__set_property('Layout.preferredWidth','rw')

        self.__right = self._QtObject__add(Row())
        self.__right.spacing = 6
        self.__right._QtObject__set_property('Layout.topMargin', 2)

        self.__icon = self._QtObject__add(Image('glitch'))
        self.__icon._QtObject__set_property('Layout.margins', 5)

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
            return self.__right.add(item)
        return self.__left.add(item)

    def __signals_conf(self) -> None:
        self._app._render_signal.connect(self.__center_title)
        if hasattr(self._app, '_shape_signal'):
            self._app._shape_signal.connect(self.__shape_signal_thread)

    def __shape_signal_thread(self) -> None:
        QTimer.singleShot(100, self.__on_shape_signal)

    def __on_shape_signal(self) -> None:
        self.__center_title(True)

        if self._app._platform.global_menu:
            if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
                if self.__control_buttons.visible:
                    self.__control_buttons.visible = False
                    self.__icon.visible = False
            else:
                self.__control_buttons.visible = True
                self.__icon.visible = True

    def __center_title(self, shape=False) -> None:
        # Size vars
        controls = int(self.__control_buttons.width[0])
        left = int(self.__left.width[0])
        left_margin = int(self.__left_plus.width[0])
        left_span = int(self.__left_span.width[0])

        title = int(self.__text.width[0])

        right_span = int(self.__right_span.width[0])
        right_margin = int(self.__right_plus.width[0])
        right = int(self.__right.width[0])
        icon = int(self.__icon.width[0])

        window = int(self._app.width[0])
        ratio = self._app._QtObject__obj.devicePixelRatio()

        if not self.__control_buttons.visible: controls = 0
        if not self.__icon.visible: icon = 0

        # New stop point
        used_area = (controls * ratio) + left + title + right + icon
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
            QTimer.singleShot(50, self.__center_title)

        if not self.__resize:
            self._app._resize_signal.connect(self.__center_title)
            self.__resize = True

        # Equal sides +
        left_side = (controls * ratio) + (left * ratio)
        if left_side < 0: left_side = 0

        right_side = (right * ratio) + (icon * ratio)
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
        total_left = left_side + left_margin + left_span
        total_right = right_side + right_margin + right_span
        dt = (total_left + title + total_right + 20) - window

        rwidth = right_margin - dt
        if self.__side == 'right' and not right_span and rwidth > 2:
            if self.__stop: rwidth = 5
            if self.__margin_delta > right_margin - dt:
                self.__right_plus._QtObject__set_property('rw', rwidth)

        lwidth = left_margin - dt
        if self.__side == 'left' and not left_span and lwidth > 2:
            if self.__stop: lwidth = 5
            if self.__margin_delta > left_margin - dt:
                self.__left_plus._QtObject__set_property('lw', lwidth)
