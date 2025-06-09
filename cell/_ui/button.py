#/usr/bin/env python3
from PySide6 import QtCore

from .element import Element


class Button(Element):
    """..."""
    def __init__(
            self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = self._obj.property('text')
        self.__icon = self._obj.findChild(QtCore.QObject, 'icon')
        # iconSource

    @property
    def text(self) -> str:
        """..."""
        return self._obj.property('text')

    @text.setter
    def text(self, text: str) -> None:
        self._obj.setProperty('text', text)

    @property
    def margins(self) -> tuple:
        """Sets the `Button` margins.

        Get:
            (5, 10, 5, 10)

        Set:
            Missing value, only from left to right.

            self.my_button.margins = 5
            self.my_button.margins = 5, 10
            self.my_button.margins = 5, 10, 5
            self.my_button.margins = 5, 10, 5, 10
            
            If a value is missing on the left, fill it with `None`.
            `None` records the value already present in that position.

            self.my_button.margins = None, 10, None, 10
            self.my_button.margins = 5, None, None, 5
            self.my_button.margins = None, None, 5
            self.my_button.margins = None, None, None, 5
        """
        return (
            int(self._obj.property('topMargin')),
            int(self._obj.property('rightMargin')),
            int(self._obj.property('bottomMargin')),
            int(self._obj.property('leftMargin')))

    @margins.setter
    def margins(self, margins: tuple) -> None:
        prev_margins = self.margins

        if isinstance(margins, int) or isinstance(margins, str):
            top, right, bottom, left = (margins,) + prev_margins[1:]
        elif len(margins) == 2:
            top, right, bottom, left = margins + prev_margins[2:]
        elif len(margins) == 3:
            top, right, bottom, left = margins + (prev_margins[-1],)
        else:
            top, right, bottom, left = margins[:4]

        top = prev_margins[0] if not top else top
        right = prev_margins[1] if not right else right
        bottom = prev_margins[2] if not bottom else bottom
        left = prev_margins[3] if not left else left

        self._obj.setProperty('topMargin', str(top))
        self._obj.setProperty('rightMargin', str(right))
        self._obj.setProperty('bottomMargin', str(bottom))
        self._obj.setProperty('leftMargin', str(left))

    def connect(self, func: callable) -> None:
        self._obj.clicked.connect(func)
