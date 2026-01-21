#!/usr/bin/env python3
import os
import subprocess
import platform

from .close_button import CloseButton
from .image import Image
from .max_button import MaxButton
from .min_button import MinButton
from .view import View
from ...tools import DesktopFile


class ControlButtons(View):
    def __init__(self, side=0, *args, **kwargs) -> None:
        super().__init__(name='RowLayout', *args, **kwargs)
        self.__qml_base = 'Layout'

        self.__control_buttons_order = self.__get_control_buttons_order()
        self.__buttons = {'close': CloseButton(), 'max': MaxButton(),
            'min': MinButton(), 'icon': Image('glitch')}

        control_buttons_side = self.__control_buttons_order[side]
        self.__count = len(control_buttons_side)

        if control_buttons_side == ('',):
            self.__empty = self._QtObject__add(View())
            self.__empty.width = 2
            self.__empty.margin = 0
            return

        self.spacing = 6
        self.margin = 5, 6, 6, 6
        for button in control_buttons_side:
            setattr(self, button, self._QtObject__add(self.__buttons[button]))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _count(self) -> bool:
        """..."""
        return self.__count
    
    def __get_control_buttons_order(self) -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        if platform.system() == 'Linux':
            if os.environ['DESKTOP_SESSION'] == 'cinnamon':
                self.__platform = 'cinnamon'

                cmd = subprocess.run(
                    'gsettings get org.cinnamon.desktop.wm.preferences '
                    'button-layout', shell=True, capture_output=True, text=True)
                button_layout = cmd.stdout.strip().strip("'").strip('"')

                buttons_l, buttons_r = button_layout.replace(
                    'minimize', 'min').replace(
                    'maximize', 'max').split(':')
                
                return tuple(buttons_l.split(',')), tuple(buttons_r.split(','))

            elif os.environ['DESKTOP_SESSION'] == 'plasma':
                filerc = os.path.join(os.environ['HOME'], '.config', 'kwinrc')
                if not os.path.isfile(filerc):
                    return ('close', 'max', 'min'), ('icon',)
                kwinrc = DesktopFile(url=filerc).content

                left_buttons = 'M'  # M = icon, F = above all
                right_buttons = 'IAX'  # X = close, A = max, I = min

                kdecoration = '[org.kde.kdecoration2]'
                buttons_on_left = 'ButtonsOnLeft'
                buttons_on_right = 'ButtonsOnRight'
                if kdecoration in kwinrc:
                    if buttons_on_left in kwinrc[kdecoration]:
                        left_buttons = kwinrc[kdecoration][buttons_on_left]

                    if buttons_on_right in kwinrc[kdecoration]:
                        right_buttons = kwinrc[kdecoration][buttons_on_right]

                d = {'X': 'close', 'A': 'max', 'I': 'min', 'M': 'icon'}
                return tuple(
                    d[x] for x in left_buttons
                    if x == 'X' or x == 'A' or x == 'I' or x == 'M'), tuple(
                    d[x] for x in right_buttons
                    if x == 'X' or x == 'A' or x == 'I' or x == 'M')

        return ('close', 'max', 'min'), ('icon',)
