#!/usr/bin/env python3
import pathlib

from PySide6.QtCore import QTimer

from .app_control_buttons import AppControlButtons
from .label import Label
from .tool_button import ToolButton
from ..ui import UI
from ..layout import Row


class HeaderBar(Row):
    def __init__(self, title: str = 'Olá mundo!', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._QtObject__set_property('spacing', '0')
        self._QtObject__set_property('Layout.fillWidth', 'true')
        self.__resize = False
        self.__side = 'left'
        self.__margin_delta = 0

        self.__total_left = 0
        self.__total_right = 0
        self.__total = 0

        self.__control_buttons = self._QtObject__add(AppControlButtons())
        self.__left = self._QtObject__add(Row())
        self.__left._QtObject__set_property('Layout.fillWidth', 'true')
        self.__left._QtObject__set_property('Layout.topMargin', 2)
        
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
        self.__right._QtObject__set_property('Layout.fillWidth', 'true')
        self.__right._QtObject__set_property('Layout.topMargin', 2)

        self.__icon = self._QtObject__add(UI('Image'))
        self.__icon._QtObject__set_property('source', pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'glitch.svg')
        self.__icon._QtObject__set_property('Layout.margins', 5)

        self._app_signal.connect(
            lambda: self._app._render_signal.connect(self.__center_title))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def add(self, item: ToolButton, right: bool = False) -> ToolButton:
        """..."""
        if right:
            return self.__right.add(item)
        return self.__left.add(item)

    def __center_title_shot(self) -> None:
        print('SHOOOT')
        self.__center_title()

    def __center_title(self) -> None:
        self._app._state_signal.connect(
            lambda: QTimer.singleShot(2000, self.__center_title_shot))

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

        left_side = (self.__control_buttons._QtObject__property('width'
            ) * ratio) + (left * ratio)
        if left_side < 0: left_side = 0

        right_side = (right * ratio) + (icon * ratio)
        if right_side < 0: right_side = 0

        # print(left, left_margin, left_span, 'text',
        #     right_span, right_margin, right)

        if not self.__resize:
            self._app._AppFrame__resize_signal.connect(self.__center_title)
            self.__resize = True

        if left_side > right_side:
            self.__rwidth = int(left_side - right_side)
            self.__right_margin._QtObject__set_property('rwidth',self.__rwidth)
            self.__side = 'right'
            self.__margin_delta = self.__rwidth
        else:
            self.__lwidth = int(right_side - left_side)
            self.__left_margin._QtObject__set_property('lwidth', self.__lwidth)
            self.__side = 'left'
            self.__margin_delta = self.__lwidth

        total_left = left_side + left_margin + left_span
        total_right = right_side + right_margin + right_span
        total = total_left + title + total_right + 20
        dt = total - window
        
        if self.__side == 'right' and not right_span and right_margin - dt > 2:
            if left_margin == 0 and right_margin > 10:
                # print('R STOP')
                pass
            if self.__margin_delta > right_margin - dt:
                self.__right_margin._QtObject__set_property(
                    'rwidth', right_margin - dt)

        if self.__side == 'left' and not left_span and left_margin - dt > 2:
            if right_margin == 0 and left_margin > 10:
                # print('L STOP')
                pass

            if self.__margin_delta > left_margin - dt:
                self.__left_margin._QtObject__set_property(
                    'lwidth', left_margin - dt)
