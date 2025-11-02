#!/usr/bin/env python3
import pathlib

from PySide6.QtCore import QTimer

from .app_control_buttons import AppControlButtons
from .label import Label
from .tool_button import ToolButton
from .view import View
from ..ui import UI
from ..layout import Row


class HeaderBar(View):
    def __init__(self, title: str = 'Olá mundo!', *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        self.__qml_base = 'Layout'
        self._QtObject__set_property('spacing', 0)
        self._QtObject__set_property('Layout.fillWidth', 'true')
        self.__resize = False

        self.__side = 'left'
        self.__rwidth = 0
        self.__lwidth = 0
        self.__margin_delta = 0
        self.__stop = False

        self.__control_buttons = self._QtObject__add(AppControlButtons())
        self.__left = self._QtObject__add(Row())
        self.__left.spacing = 6
        self.__left._QtObject__set_property('Layout.fillWidth', 'true')
        self.__left._QtObject__set_property('Layout.topMargin', 3)
        
        self.__left_margin = self._QtObject__add(UI())
        self.__left_margin._QtObject__set_property('property int lwidth', 0)
        self.__left_margin._QtObject__set_property(
            'Layout.preferredWidth', 'lwidth')

        self.__left_span = self._QtObject__add(UI())
        self.__left_span._QtObject__set_property('Layout.fillWidth', 'true')
        self.__title = self._QtObject__add(Label(title))
        self.__right_span = self._QtObject__add(UI())
        self.__right_span._QtObject__set_property('Layout.fillWidth', 'true')

        self.__right_margin = self._QtObject__add(UI())
        self.__right_margin._QtObject__set_property('property int rwidth', 0)
        self.__right_margin._QtObject__set_property(
            'Layout.preferredWidth', 'rwidth')

        self.__right = self._QtObject__add(Row())
        self.__right.spacing = 6
        self.__right._QtObject__set_property('Layout.fillWidth', 'true')
        self.__right._QtObject__set_property('Layout.topMargin', 3)

        self.__icon = self._QtObject__add(UI('Image'))
        self.__icon._QtObject__set_property('source', pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'glitch.svg')
        self.__icon._QtObject__set_property('Layout.margins', 5)

        self._app_signal.connect(self.__signals_conf)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def spacing(self) -> int:
        """..."""
        return self._QtObject__property('spacing')

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        if hasattr(self, '_HeaderBar__left'):
            getattr(self, '_HeaderBar__left').spacing = spacing

        if hasattr(self, '_HeaderBar__left'):
            getattr(self, '_HeaderBar__left').spacing = spacing

        if hasattr(self, '_HeaderBar__right'):
            getattr(self, '_HeaderBar__right').spacing = spacing
    
    @property
    def text(self) -> str:
        return self.__title.text

    @text.setter
    def text(self, text: str) -> None:
        self.__title.text = text

    def add(self, item: ToolButton, right: bool = False) -> ToolButton:
        """..."""
        if right:
            return self.__right.add(item)
        return self.__left.add(item)

    def __signals_conf(self) -> None:
        self._app._render_signal.connect(self.__center_title)
        self._app._state_signal.connect(self.__state_signal_thread)

    def __state_signal_thread(self) -> None:
        QTimer.singleShot(100, self.__on_state_signal)

    def __on_state_signal(self) -> None:
        self.__center_title(True)

    def __center_title(self, state=False) -> None:
        # Size vars
        left = int(self.__left._QtObject__property('width'))
        left_margin = int(self.__left_margin._QtObject__property('width'))
        left_span = int(self.__left_span._QtObject__property('width'))

        title = int(self.__title._QtObject__property('width'))

        right = int(self.__right._QtObject__property('width'))
        right_margin = int(self.__right_margin._QtObject__property('width'))
        right_span = int(self.__right_span._QtObject__property('width'))
        
        icon = int(self.__icon._QtObject__property('width'))
        window = int(self._app._QtObject__obj.width())
        ratio = self._app._QtObject__obj.devicePixelRatio()

        left_side = (self.__control_buttons._QtObject__property(
            'width') * ratio) + (left * ratio)
        if left_side < 0: left_side = 0

        right_side = (right * ratio) + (icon * ratio)
        if right_side < 0: right_side = 0

        # Signals
        if state:
            self.__right_margin._QtObject__set_property('rwidth', 0)
            self.__left_margin._QtObject__set_property('lwidth', 0)
            self.__stop = False
            QTimer.singleShot(50, self.__center_title)

        if not self.__resize:
            self._app._resize_signal.connect(self.__center_title)
            self.__resize = True

        # Equal sides +
        if left_side > right_side:
            self.__rwidth = int(left_side - right_side)
            self.__side = 'right'
            self.__margin_delta = self.__rwidth
            rwidth = 0 if self.__stop else self.__rwidth
            self.__right_margin._QtObject__set_property('rwidth', rwidth)
        else:
            self.__lwidth = int(right_side - left_side)
            self.__side = 'left'
            self.__margin_delta = self.__lwidth
            lwidth = 0 if self.__stop else self.__lwidth
            self.__left_margin._QtObject__set_property('lwidth', lwidth)

        # Equal sides -
        total_left = left_side + left_margin + left_span
        total_right = right_side + right_margin + right_span
        dt = (total_left + title + total_right + 20) - window

        rwidth = right_margin - dt
        if self.__side == 'right' and not right_span and rwidth > 2:
            self.__stop = True if left_margin < 10 and rwidth < 10 else False
            if self.__stop: rwidth = 5
            if self.__margin_delta > right_margin - dt:
                self.__right_margin._QtObject__set_property('rwidth', rwidth)

        lwidth = left_margin - dt
        if self.__side == 'left' and not left_span and lwidth > 2:
            self.__stop = True if right_margin < 10 and lwidth < 10 else False
            if self.__stop: lwidth = 5
            if self.__margin_delta > left_margin - dt:
                self.__left_margin._QtObject__set_property('lwidth', lwidth)
