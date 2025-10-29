#!/usr/bin/env python3
import pathlib

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

        self.__control_buttons = self._QtObject__add(AppControlButtons())
        self.__left = self._QtObject__add(Row())
        self.__left._QtObject__set_property('Layout.fillWidth', 'true')
        self.__left._QtObject__set_property('Layout.topMargin', 2)
        
        self._left_space = self._QtObject__add(UI())
        self._left_space._QtObject__set_property('property int lwidth', 0)
        self._left_space._QtObject__set_property(
            'Layout.preferredWidth', 'lwidth')

        left_span = self._QtObject__add(UI())
        left_span._QtObject__set_property('Layout.fillWidth', 'true')
        self.__title = self._QtObject__add(Label(title))
        right_span = self._QtObject__add(UI())
        right_span._QtObject__set_property('Layout.fillWidth', 'true')

        self._right_space = self._QtObject__add(UI())
        self._right_space._QtObject__set_property('property int rwidth', 0)
        self._right_space._QtObject__set_property(
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

    def __center_title(self) -> None:
        if not self.__resize:
            self._app._AppFrame__resize_signal.connect(self.__center_title)
            self.__resize = True

        ratio = self._app._QtObject__obj.devicePixelRatio()
        left = (
            self.__control_buttons._QtObject__property('width') * ratio) + (
            self.__left._QtObject__property('width') * ratio)
        if left < 0: left = 0
        right = (
            self.__right._QtObject__property('width') * ratio) + (
            self.__icon._QtObject__property('width') * ratio)
        if right < 0: right = 0
        
        if left > right:
            self._right_space._QtObject__set_property(
                'rwidth', int(left - right))
        else:
            self._left_space._QtObject__set_property(
                'lwidth', int(right - left))
