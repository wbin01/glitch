#!/usr/bin/env python3
from PySide6 import QtCore

from ..base import Layout


qml = """
Popup {
    id: panel  // <id>
    objectName: "panel"  // <objectName>
    property string qmlType: "Panel"  // <className>
    property string baseClass: "Layout"  // <baseClass>

    ColumnLayout {
        id: column
        
        property int topMargin: 0
        property int rightMargin: 0
        property int bottomMargin: 0
        property int leftMargin: 0
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin
        
        spacing: 6

        anchors.fill: parent
        // anchors.margins: 6

// **closing_key**
    }
}
"""


class Panel(Layout):
    """Panel layout.

    Opens and closes to display content.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._qml = qml

        self.id = f'_{id(self)}'
        self._element_type = 'Panel'

        self.__show_anim = QtCore.QParallelAnimationGroup()
        # self.__hide_anim = QtCore.QParallelAnimationGroup()
        self.__is_open = False
        self.__connect_close = False

    def close(self) -> None:
        """Closes the Panel.

        Makes the Panel invisible.
        """
        self._obj.close()
        self.__is_open = False

    def open(self) -> None:
        """Open and display the Panel.

        By default, the Panel is not visible; this "open()" method is used 
        to display it.
        """
        if not self._obj: # or self._obj.property('visible'):
            return

        if not self.__connect_close:
            self._obj.closed.connect(self.close)
            self.__connect_close = True

        slide_in = QtCore.QPropertyAnimation(self._obj, b"x")
        slide_in.setDuration(300)
        slide_in.setStartValue(-250)
        slide_in.setEndValue(-5)
        slide_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        fade_in = QtCore.QPropertyAnimation(self._obj, b"opacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.__show_anim.addAnimation(slide_in)
        self.__show_anim.addAnimation(fade_in)

        # slide_out = QtCore.QPropertyAnimation(self._obj, b"x")
        # slide_out.setDuration(300)
        # slide_out.setStartValue(0)
        # slide_out.setEndValue(250)
        # slide_out.setEasingCurve(QtCore.QEasingCurve.InCubic)
        # fade_out = QtCore.QPropertyAnimation(self._obj, b"opacity")
        # fade_out.setDuration(300)
        # fade_out.setStartValue(1)
        # fade_out.setEndValue(0)
        # fade_out.setEasingCurve(QtCore.QEasingCurve.InCubic)
        # self.__hide_anim.addAnimation(slide_out)
        # self.__hide_anim.addAnimation(fade_out)

        if not self.__is_open:
            self.__is_open = True
            self._obj.open()
            self.__show_anim.start()

            # self.__hide_anim.finished.disconnect(on_done)
            # self.__hide_anim.finished.connect(on_done)
            # self.__hide_anim.start()

        # Hack
        self._obj.open()
        self.__show_anim.start()

    def __str__(self) -> str:
        return "<class 'Panel'>"
