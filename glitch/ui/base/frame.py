#!/usr/bin/env python3
import logging

from PySide6 import QtCore

from .layout import Layout
from ...enum import Event, FrameHint, FrameShape, Orientation
from ...platform_ import Style


header = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

import "elements"


Window {
    id: frame  // ID
    objectName: "frame"  // Object name
    property string qmlType: "Window"  // Class Name
    property string baseClass: "Frame"  // Base class name
"""

properties = """
    title: qsTr("Cell")
    color: "transparent"
    flags: Qt.FramelessWindowHint

    property int width_: 300
    property int height_: 300
    width: width_
    height: height_

    minimumWidth: 100
    minimumHeight: 100

    visible: true
    visibility: Window.Windowed

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.RightButton
        onPressed: logic.connections()
    }

    Rectangle {
        id: mainRect
        objectName: "mainRect"
        anchors.fill: parent
        color: "transparent"
        z: 1
        property bool isActive: true

        property color backgroundColor: "#222"
        property color borderColor: "#333"
        property color outLineColor: "#44000000"
        property int borderWidth: 1
        property int outLineWidth: 1

        property int radiusTopLeft: 10
        property int radiusTopRight: 10
        property int radiusBottomRight: 10
        property int radiusBottomLeft: 10

        Canvas {
            id: canvas
            objectName: "canvas"
            anchors.fill: parent
            property int borderSpacing: 1

            onPaint: {
                var ctx = getContext("2d");
                ctx.clearRect(0, 0, width, height);

                // Função para desenhar retângulo arredondado com raios individuais
                function roundedRect(x, y, w, h, rtl, rtr, rbr, rbl) {
                    ctx.beginPath();
                    ctx.moveTo(x + rtl, y);
                    ctx.lineTo(x + w - rtr, y);
                    ctx.arcTo(x + w, y, x + w, y + rtr, rtr);
                    ctx.lineTo(x + w, y + h - rbr);
                    ctx.arcTo(x + w, y + h, x + w - rbr, y + h, rbr);
                    ctx.lineTo(x + rbl, y + h);
                    ctx.arcTo(x, y + h, x, y + h - rbl, rbl);
                    ctx.lineTo(x, y + rtl);
                    ctx.arcTo(x, y, x + rtl, y, rtl);
                    ctx.closePath();
                }

                // --- Background ---
                roundedRect(1, 1, width - 2, height - 2,
                            mainRect.radiusTopLeft, mainRect.radiusTopRight,
                            mainRect.radiusBottomRight, mainRect.radiusBottomLeft);
                ctx.fillStyle = mainRect.backgroundColor;
                ctx.fill();

                // --- Outer border ---
                roundedRect(0, 0, width, height,
                            mainRect.radiusTopLeft + 2, mainRect.radiusTopRight + 2,
                            mainRect.radiusBottomRight + 2, mainRect.radiusBottomLeft + 2);
                ctx.strokeStyle = mainRect.outLineColor;
                ctx.lineWidth = mainRect.outLineWidth;
                ctx.stroke();

                // --- Inner border ---
                var inset = borderSpacing + mainRect.borderWidth / 2;
                roundedRect(
                    inset, inset,
                    width - inset * 2,
                    height - inset * 2,
                    Math.max(0, mainRect.radiusTopLeft - inset),
                    Math.max(0, mainRect.radiusTopRight - inset),
                    Math.max(0, mainRect.radiusBottomRight - inset),
                    Math.max(0, mainRect.radiusBottomLeft - inset)
                );
                ctx.strokeStyle = mainRect.borderColor;
                ctx.lineWidth = mainRect.borderWidth;
                ctx.stroke();
            }
        }

// MainFrame

// Resize corners

        ColumnLayout {
            id: mainColumnLayout
            objectName: "mainColumnLayout"
            anchors.fill: parent
            // anchors.top: parent.top
            anchors.margins: 6
            spacing: 6
            clip: true
            // Layout.fillHeight: false
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true

// Close

        }
    }
"""
# } close on UI

edges = """
// Resize corners
// Top left - resize NW
        MouseArea {
            id: resizeTopLeft
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.left: parent.left
            cursorShape: Qt.SizeFDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge | Qt.LeftEdge)
        }

        // Top right - resize NE
        MouseArea {
            id: resizeTopRight
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.right: parent.right
            cursorShape: Qt.SizeBDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge | Qt.RightEdge)
        }

        // Bottom left - resize SW
        MouseArea {
            id: resizeBottomLeft
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            cursorShape: Qt.SizeBDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge | Qt.LeftEdge)
        }

        // Bottom right - resize SE
        MouseArea {
            id: resizeBottomRight
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            cursorShape: Qt.SizeFDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge | Qt.RightEdge)
        }

        // Top - N
        MouseArea {
            id: resizeTop
            anchors.top: parent.top
            anchors.left: resizeTopLeft.right
            anchors.right: resizeTopRight.left
            height: 5
            cursorShape: Qt.SizeVerCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge)
        }

        // Bottom - S
        MouseArea {
            id: resizeBottom
            anchors.bottom: parent.bottom
            anchors.left: resizeBottomLeft.right
            anchors.right: resizeBottomRight.left
            height: 5
            cursorShape: Qt.SizeVerCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge)
        }

        // Left - W
        MouseArea {
            id: resizeLeft
            anchors.top: resizeTopLeft.bottom
            anchors.bottom: resizeBottomLeft.top
            anchors.left: parent.left
            width: 5
            cursorShape: Qt.SizeHorCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.LeftEdge)
        }

        // Right - E
        MouseArea {
            id: resizeRight
            anchors.top: resizeTopRight.bottom
            anchors.bottom: resizeBottomRight.top
            anchors.right: parent.right
            width: 5
            cursorShape: Qt.SizeHorCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.RightEdge)
        }
// Resize corners
"""


class Frame(Layout):
    """An application frame.

    A frame where visual elements are inserted. Usually called a "Window".
    It is not the main Frame of an application, and it has no movement 
    capabilities. It is ideal as a part of the main application, such as a 
    context menu or a tool panel.
    """
    def __init__(self, resizable: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Args
        self.__resizable = resizable

        # QML
        self._qml = header + self._qml.split(
            '// Frame header')[1].replace(
            '// Close', '').replace('\n    // Property', properties)
        if self.__resizable:
            qml_init, qml_end = self._qml.split('\n// Resize corners')
            self._qml = qml_init + edges + qml_end
        self.class_id('Frame')

        # Properties
        self.__height = 300
        self.__width = 300
        self.__size = self.__width, self.__height
        # self.__spacing = 6

        self.__hint = FrameHint.FRAME
        self.__shape = FrameShape.FRAME
        # self.__items = []
        self.__style = Style().style
        self.__visibility = 'Window.Windowed'
        self.__callbacks = {}
        self.__radius = 10, 10, 10, 10

    @property
    def hint(self) -> FrameHint:
        """Frame behavior hint.

        FrameHint.BOTTOM → Always behind.
        FrameHint.FRAME → Normal behavior.
        FrameHint.POPUP → Popup Frame (does not appear in the taskbar).
        FrameHint.TOOL → Tool-like Frame (does not appear in the taskbar).
        FrameHint.TOP → Always on top.

        Use `FrameHint.TOOL` and `FrameHint.POPUP` inside a method to activate 
        them only when the window is ready; this will avoid styling issues.

        Use the `name` property to know which `FrameHint` it is.
        
        >>> self.hint = FrameHint.FRAME
        >>> print(self.hint.name)
        FRAME

        Note! On Linux it doesn't work on the Wayland display server, only on 
        the Xorg or those based on it.
        """
        return self.__hint

    @hint.setter
    def hint(self, hint: FrameHint) -> None:
        hints = {
            'BOTTOM': 'Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint',
            'FRAME': 'Qt.FramelessWindowHint',
            'POPUP': 'Qt.FramelessWindowHint | Qt.Popup',
            'TOOL': 'Qt.FramelessWindowHint | Qt.Tool',
            'TOP': 'Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint'}

        if self._obj:
            self._obj.setProperty('flags', int(hint.value))
        else:
            self._qml = self._qml.replace(
                f'flags: {hints[self.__hint.name]}',
                f'flags: {hints[hint.name]}')

        self.__hint = hint

    @property
    def radius(self) -> tuple:
        """Sets the Frame radius.

        A tuple with the 4 radius values. The values are order: top-left, 
        top-right, bottom-right and bottom-left respectively:

            (10, 10, 10, 10)

        It is not mandatory to pass all the values, the last value will be 
        used to fill in the missing ones:

        `radius = 5` is equivalent to `radius = 5, 5, 5, 5`
        `radius = 5, 10` is equivalent to `radius = 5, 10, 10, 10`

        Use `None` for a value to be automatic. `None` indicates that the 
        value is the same as before. Example:

            # Change top-left and bottom-right
            `element.radius = 10, None, 10, None`

            # Change top-right and bottom-left
            `element.radius = None, 5, None, 5`

        Note! Only works as initialization (__init__), before the window is 
        rendered.
        """
        return self.__radius

    @radius.setter
    def radius(self, radius: tuple) -> None:
        if not isinstance(radius, int) and not isinstance(radius, tuple):
            logging.error(
                f'\n  {self._name}.radius: Use a tuple of integers like '
                '(10, 10, 10, 10) or an integer like 10.')
            return

        if isinstance(radius, int):
            top_l, top_r, bottom_r, bottom_l = radius, radius, radius, radius
        elif len(radius) == 1:
            top_l, top_r, bottom_r, bottom_l = (
                radius[0], radius[0], radius[0], radius[0])
        elif len(radius) == 2:
            top_l, top_r, bottom_r, bottom_l = radius + (radius[1], radius[1])
        elif len(radius) == 3:
            top_l, top_r, bottom_r, bottom_l = radius + (radius[2],)
        else:
            top_l, top_r, bottom_r, bottom_l = radius[:4]

        top_l = self.__radius[0] if top_l is None else top_l
        top_r = self.__radius[1] if top_r is None else top_r
        bottom_r = self.__radius[2] if bottom_r is None else bottom_r
        bottom_l = self.__radius[3] if bottom_l is None else bottom_l

        if self._obj:
            # The code works, but is not desirable and has been disabled!
            return

            self._obj.setProperty('radiusTopLeft', top_l)
            self._obj.setProperty('radiusTopRight', top_r)
            self._obj.setProperty('radiusBottomRight', bottom_r)
            self._obj.setProperty('radiusBottomLeft', bottom_l)

            # TODO: Move to Application().processEvents()  works the right way
            self._obj.findChild(QtCore.QObject, 'canvas').requestPaint()
            shape = self.shape
            self.shape = (FrameShape.MAXIMIZED
                if shape.name != 'MAXIMIZED' else FrameShape.FULL_SCREEN)
            def _shape_(shape):
                self.shape = shape
            QtCore.QTimer.singleShot(300, lambda: _shape_(shape))
            
        else:
            self._qml = self._qml.replace(
                f'property int radiusTopLeft: {self.__radius[0]}',
                f'property int radiusTopLeft: {top_l}')
            self._qml = self._qml.replace(
                f'property int radiusTopRight: {self.__radius[1]}',
                f'property int radiusTopRight: {top_r}')
            self._qml = self._qml.replace(
                f'property int radiusBottomRight: {self.__radius[2]}',
                f'property int radiusBottomRight: {bottom_r}')
            self._qml = self._qml.replace(
                f'property int radiusBottomLeft: {self.__radius[3]}',
                f'property int radiusBottomLeft: {bottom_l}')

        self.__radius = top_l, top_r, bottom_r, bottom_l

    @property
    def shape(self) -> FrameShape:
        """The Frame shape.

        A `FrameShape` enumeration that indicates whether the Frame shape is 
        maximized, minimized, full screen, or a normal Frame shape.
        """
        return self.__shape

    @shape.setter
    def shape(self, shape: FrameShape = FrameShape.FRAME) -> None:
        # Window.AutomaticVisibility  1     system default (normally Windowed)
        shape_value = {
            0: 'Window.Hidden', 1: 'Window.AutomaticVisibility',
            2: 'Window.Windowed', 3: 'Window.Minimized',
            4: 'Window.Maximized', 5: 'Window.FullScreen'}
        visibility = shape_value[shape.value]

        if self._obj:
            if shape.value == 2:
                self._obj.showNormal()
            elif shape.value == 4:
                self._obj.showMaximized()
            elif shape.value == 3:
                self._obj.showMinimized()
            elif shape.value == 5:
                self._obj.showFullScreen()
        else:
            self._qml = self._qml.replace(
                f'visibility: {self.__visibility}',
                f'visibility: {visibility}')

        self.__visibility = visibility
        self.__shape = shape

    @property
    def size(self) -> tuple:
        """Frame width and height.

        Tuple like (500, 500).
        """
        return self.__size

    @size.setter
    def size(self, size: tuple) -> None:
        if not isinstance(size, int) and not isinstance(size, tuple):
            logging.error(
                f'\n  {self._name}.size: Use a tuple of integers like '
                '(600, 400) or an integer like 500.')
            return

        if isinstance(size, int):
            width, height = size, size
        elif len(size) == 1:
            width, height = size[0], size[0]
        elif len(size) >= 2:
            width, height = size[:2]

        width = self.__size[0] if width is None else width
        height = self.__size[1] if height is None else height

        if self._obj:
            self._obj.setProperty('width_', width)
            self._obj.setProperty('height_', height)
        else:
            self._qml = self._qml.replace(
                f'width_: {self.__width}', f'width_: {width}').replace(
                f'height_: {self.__height}', f'height_: {height}')

        self.__width = width
        self.__height = height
        self.__size = width, height

    @property
    def style(self) -> dict:
        """Application style.

        A dictionary with color and style information for each visual element 
        in the application.
        """
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    def callbacks(self) -> dict:
        """The functions used in the `connect` method.

        The `connect` method organizes the received functions into a 
        dictionary organized by the type of event they are associated with.
        """
        return self.__callbacks

    def connect(
            self, method: callable, event: Event = Event.MOUSE_PRESS) -> None:
        """Connect the button to a method.

        Pass a method to be executed when interacting with the button.
        Alternatively, use an event like `Event.MOUSE_HOVER` or 
        `Event.MOUSE_WHEEL` to configure when the button will use the method.

        :param method: method to be executed when interacting with the button.
        :param event: Enum like `Event.MOUSE_HOVER` or `Event.MOUSE_WHEEL`
        """
        self.__callbacks[event] = method

    def __str__(self) -> str:
        return "<class 'Frame'>"
