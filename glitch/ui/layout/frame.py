#!/usr/bin/env python3
import logging

from PySide6 import QtCore

from ..base import Layout, RadiusMixin, SizeMixin
from ...core.signal import Signal
from ...enum import Event, FrameHint, FrameShape, Orientation
from ...platform_ import Platform


header = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

import "elements"


Window {
    id: frame  // ID
    objectName: "frame"  // Object name
    property string className: "Frame"  // Class name
    property string baseClass: "Layout"  // Base class
    property string styleClass: "Frame"  // Style class
    property string baseStyle: "Frame"  // Base style
"""

properties = """
    title: qsTr("Cell")
    color: "transparent"
    flags: Qt.FramelessWindowHint

    width: 100
    height: 30

    minimumWidth: 100
    minimumHeight: 30

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
            anchors.margins: 4
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


class Frame(RadiusMixin, SizeMixin, Layout):
    """An application frame.

    A frame where visual elements are inserted. Usually called a "Window".
    It is not the main Frame of an application, and it has no movement 
    capabilities. It is ideal as a part of the main application, such as a 
    context menu or a tool panel.
    """
    def __init__(self, resizable: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.size_signal = Signal()
        self.shape_signal = Signal()

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
        self.size = 300
        self.__style = None
        self.__hint = FrameHint.FRAME
        self.__shape = FrameShape.FRAME
        self.__platform = Platform()
        self.__style = self.__platform.style
        self.__visibility = 'Window.Windowed'
        self.__callbacks = {}
        self.__radius = 10, 10, 10, 10

        # Set
        self.radius = self.__style[f'[{self._name}]']['border_radius']

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
    def shape(self) -> FrameShape:
        """The Frame shape.

        A `FrameShape` enumeration that indicates whether the Frame shape is 
        maximized, minimized, full screen, or a normal Frame shape.
        """
        return self.__shape

    @shape.setter
    def shape(
            self, shape: FrameShape | QtCore.Qt.WindowState = FrameShape.FRAME
            ) -> None:
        # Window.AutomaticVisibility  1     system default (normally Windowed)
        if isinstance(shape, QtCore.Qt.WindowState):
            if shape == QtCore.Qt.WindowFullScreen:
                self.__shape = FrameShape.FULL
            elif shape == QtCore.Qt.WindowMaximized:
                self.__shape = FrameShape.MAX
            elif shape == QtCore.Qt.WindowNoState:
                self.__shape = FrameShape.FRAME
            else:
                self.__shape = FrameShape.MIN
            return

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
        self.shape_signal.emit()

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

    @property
    def _platform(self) -> Platform:
        """..."""
        return self.__platform

    @_platform.setter
    def _platform(self, platform) -> None:
        self.__platform = platform

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
