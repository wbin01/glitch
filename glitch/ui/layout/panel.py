#!/usr/bin/env python3
import logging

from PySide6 import QtCore

from ..base import Layout, RadiusMixin
from ...enum import Align


header = """
Popup {
    id: panel  // ID
    objectName: "panel"  // Object name
    property string className: "Panel"  // Class name
    property string baseClass: "Layout"  // Base class
    property string styleClass: "Panel"  // Style class
    property string baseStyle: "Panel"  // Base style
"""

properties = """
    padding: 1 // Frame border
    width: 250

    // Padding is 6 -> 6+6=12 -> 12-2 (2 is 1 pixel border on top and bottom) =10
    height: parent.height + 6  // 10

    x: 0

    // Half of the Frame padding - outer border
    y: - 3  // 5
    
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    clip: true

    transformOrigin: Item.Left

    property int parentHeight: parent.height + 6 // 10
    property int parentWidth: parent.width + 7 // 9  // 10 -1 detach from the right

    property color backgroundColor: "#222"
    property color borderColor: "#222"
    property int borderWidth: 1

    property int radiusTopLeft: 10
    property int radiusTopRight: 10
    property int radiusBottomRight: 10
    property int radiusBottomLeft: 10

    background: Rectangle {
        color: "#00000000"
        radius: 0
        border.color: "#00000000"
        border.width: 1
        clip: true
    }

    Canvas {
        id: canvas_panel
        objectName: "canvas_panel"
        anchors.fill: parent

        onPaint: {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);

            ctx.beginPath();
            ctx.moveTo(panel.radiusTopLeft, 0);
            ctx.lineTo(width - panel.radiusTopRight, 0);
            ctx.arcTo(width, 0, width, panel.radiusTopRight, panel.radiusTopRight);
            ctx.lineTo(width, height - panel.radiusBottomRight);
            ctx.arcTo(width, height, width - panel.radiusBottomRight, height, panel.radiusBottomRight);
            ctx.lineTo(panel.radiusBottomLeft, height);
            ctx.arcTo(0, height, 0, height - panel.radiusBottomLeft, panel.radiusBottomLeft);
            ctx.lineTo(0, panel.radiusTopLeft);
            ctx.arcTo(0, 0, panel.radiusTopLeft, 0, panel.radiusTopLeft);
            ctx.closePath();

            // Background color
            ctx.fillStyle = panel.backgroundColor;
            ctx.fill();

            // Border coloe
            ctx.strokeStyle = panel.borderColor;
            ctx.lineWidth = panel.borderWidth;
            ctx.stroke();
        }
    }

    ColumnLayout {
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

// Close
    }
"""
# } close on UI. Add // Property for inheritance


class Panel(RadiusMixin, Layout):
    """Panel layout.

    Opens and closes to display content.
    """
    def __init__(
            self, frame_side: Align = Align.LEFT, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Args
        self.__frame_side = frame_side
        self.__origin = 'Item.Left'

        # QML
        self._qml = header + self._qml.split('// Layout header')[1].replace(
            '// Close', '').replace('\n    // Property', properties).replace(
            'canvas_panel', f'canvas{self._id}').replace('panel', self._id)
        self.frame_side = frame_side
        self.class_id('Panel')

        # Properties
        self.__show_anim = QtCore.QParallelAnimationGroup()
        # self.__hide_anim = QtCore.QParallelAnimationGroup()
        self.__is_open = False
        self.__connect_close = False

        # self.__radius = 10, 0, 0, 10
        self.frame_signal.connect(self.__sinc_radius)

    @property
    def frame_side(self) -> Align:
        """The Panel Align alignment.

        Whether the panel slides in from the right or left.
        Use Align.LEFT or Align.RIGHT to set the panel's direction.
        """
        return self.__frame_side

    @frame_side.setter
    def frame_side(self, frame_side: Align) -> None:
        self.__frame_side = frame_side

        new_origin = self.__get_origin()
        self._qml = self._qml.replace(
            f'transformOrigin: {self.__origin}',
            f'transformOrigin: {new_origin}')

        self.__origin = new_origin

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

        Note! Does not work at initialization (__init__), before the window is 
        rendered. Use it in a method.
        """
        if not self._obj: # or self._obj.property('visible'):
            # TODO: Init open
            return

        if not self.__connect_close:
            self._obj.closed.connect(self.close)
            self.__connect_close = True

        parent_w = self._obj.property('parentWidth')
        parent_h = self._obj.property('parentHeight')
        size = self._obj.property('width')

        start_value = - self._obj.property('width')  # default is -250
        end_value = - 5  # Frame padding half | 10
        if self.__frame_side.name == 'RIGHT':
            start_value = parent_w
            end_value = parent_w - size - 4

        slide_in = QtCore.QPropertyAnimation(self._obj, b"x")
        slide_in.setDuration(300)
        slide_in.setStartValue(start_value)
        slide_in.setEndValue(end_value)
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

    def __get_origin(self) -> str:
        # transform_origin QML string
        if self.__frame_side.name == 'RIGHT':
            return 'Item.Right'
        # elif self.__frame_side.name.startswith('BOTTOM'):
        #     return 'Item.Bottom'
        # elif self.__frame_side.name.startswith('TOP'):
            return 'Item.Top'
        return 'Item.Left'

    def __sinc_radius(self) -> None:
        if self.frame_side.value == QtCore.Qt.AlignRight:
            self.radius = (0, self._frame.radius[1], self._frame.radius[2], 0)
        else:
            self.radius = (self._frame.radius[0], 0, 0, self._frame.radius[3])

    def __str__(self) -> str:
        return "<class 'Panel'>"
