#!/usr/bin/env python3
from .close_button import CloseButton
from .image import Image
from .max_button import MaxButton
from .min_button import MinButton
from .view import View
from ...tools import DesktopFile


class ControlButtons(View):
    def __init__(self, platform, side=0, *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        self.__qml_base = 'Layout'
        self.__platform = platform

        # Set
        self.__buttons = {'close': CloseButton(), 'max': MaxButton(),
            'min': MinButton(), 'icon': Image('glitch')}

        control_buttons_side = self.__platform.control_buttons_order[side]
        self.__count = len(control_buttons_side)

        if control_buttons_side == ('',):
            self.__empty = self._QtObject__add(View())
            self.__empty.width = 2
            self.__empty.margin = 0
            return

        if self.__platform.de == 'cinnamon':
            self._QtObject__set_property('spacing', 12)
            self.margin = 6
        elif 'windows' in self.__platform.de:
            self._QtObject__set_property('spacing', 0)
            if side == 0:
                self.margin = 0, 0, 0, 6
            else:
                self.margin = 0
        elif self.__platform.de == 'glitch':
            self._QtObject__set_property('spacing', 0)
            self.margin = 0
        else:
            self._QtObject__set_property('spacing', 6)
            self.margin = 5, 6, 6, 6

        for button in control_buttons_side:
            setattr(self, button, self._QtObject__add(self.__buttons[button]))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _count(self) -> bool:
        """..."""
        return self.__count
