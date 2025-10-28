#!/usr/bin/env python3
from ..layout import Row
from .app_control_buttons import AppControlButtons
from .app_max_button import AppMaxButton
from .app_min_button import AppMinButton
from .label import Label
from ..ui import UI


class HeaderBar(Row):
    def __init__(self, title: str = 'Olá mundo!', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._QtObject__set_property('spacing', '0')
        self.__txt = title

        self.__control_buttons = self.add(AppControlButtons())
        self.__left = self.add(Row())

        self._left_space = self.add(UI())
        self._left_space._QtObject__set_property('property int lwidth', 0)
        self._left_space._QtObject__set_property(
            'Layout.preferredWidth', 'lwidth')

        self.__text = self.add(Label(self.__txt))

        self._right_space = self.add(UI())
        self._right_space._QtObject__set_property('property int rwidth', 0)
        self._right_space._QtObject__set_property(
            'Layout.preferredWidth', 'rwidth')

        self.__right = self.add(Row())
        self.__icon = self.add(Label('0'))
        self.__icon._QtObject__set_property('Layout.rightMargin', 5)

        self._app_signal.connect(
            lambda: self._app._render_signal.connect(self.__center_title))

    def __center_title(self) -> None:
        ratio = self._app._QtObject__obj.devicePixelRatio()
        left = (
            self.__control_buttons._QtObject__property('width') * ratio) + (
            self.__left._QtObject__property('width') * ratio)
        right = (
            self.__right._QtObject__property('width') * ratio) + (
            self.__icon._QtObject__property('width') * ratio)

        if left > right:
            self._right_space._QtObject__set_property(
                'rwidth', int(left - right))
        else:
            self._left_space._QtObject__set_property(
                'lwidth', int(right - left))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
