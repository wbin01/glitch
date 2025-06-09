#/usr/bin/env python3
from PySide6 import QtQuick, QtCore  # QtGui, QtQml 

from .element import Element


class Label(Element):
    """..."""
    def __init__(
            self, qt_quick_item: QtQuick.QQuickItem, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__obj = qt_quick_item
        self.__text = self.__obj.property('text')

    @property
    def text(self) -> str:
        """..."""
        return self.__obj.property('text')

    @text.setter
    def text(self, text: str) -> None:
        self.__obj.setProperty('text', text)

    @property
    def margins(self) -> tuple:
        """Sets the `Label` margins.

        Get:
            (5, 10, 5, 10)

        Set:
            Missing value, only from left to right.

            self.my_label.margins = 5
            self.my_label.margins = 5, 10
            self.my_label.margins = 5, 10, 5
            self.my_label.margins = 5, 10, 5, 10
            
            If a value is missing on the left, fill it with `None`.
            `None` records the value already present in that position.

            self.my_label.margins = None, 10, None, 10
            self.my_label.margins = 5, None, None, 5
            self.my_label.margins = None, None, 5
            self.my_label.margins = None, None, None, 5
            

        """
        return (
            int(self.__obj.property('topMargin')),
            int(self.__obj.property('rightMargin')),
            int(self.__obj.property('bottomMargin')),
            int(self.__obj.property('leftMargin')))

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

        self.__obj.setProperty('topMargin', str(top))
        self.__obj.setProperty('rightMargin', str(right))
        self.__obj.setProperty('bottomMargin', str(bottom))
        self.__obj.setProperty('leftMargin', str(left))

    def connect(self, func: callable) -> None:
        self.__obj.clicked.connect(func)
