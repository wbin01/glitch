#!/usr/bin/env python3
from PySide6 import QtCore

from .ui import UI
from ...enum import Event, FrameHint, FrameState, Orientation
from ...platform_ import Style


class Layout(object):
    """Layout object.

    Organizes elements in stacks like a column or side by side like a row.
    """
    def __str__(self) -> str:
        return "<class 'Layout'>"


class Element(object):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __str__(self) -> str:
        return "<class 'Element'>"


qml = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

import "elements"


Window {
    id: frame  // <id>
    objectName: "frame"  // <objectName>
    property string qmlType: "Window"  // <className>
    property string baseClass: "Frame"  // <baseClass>

    visible: true
    visibility: Window.Windowed
    
    height: _height
    property int _height: 200
    
    width: _width
    property int _width: 200

    minimumWidth: 200
    minimumHeight: 200
    title: qsTr("Cell")
    color: "transparent"
    flags: Qt.FramelessWindowHint

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
        // anchors.margins: margins
        // radius: 10
        // border.color: borderColor
        // border.width: borderWidth

        z: 1
        property bool isActive: true

        property color backgroundColor: "#99880000"
        property color borderColor: "#880000"
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

            property color fillColor: mainRect.backgroundColor
            property color innerBorderColor: mainRect.borderColor
            property color outerBorderColor: mainRect.outLineColor
            property int innerBorderWidth: mainRect.borderWidth
            property int outerBorderWidth: mainRect.outLineWidth
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
                ctx.fillStyle = fillColor;
                ctx.fill();

                // --- Outer border ---
                roundedRect(0, 0, width, height,
                            mainRect.radiusTopLeft + 2, mainRect.radiusTopRight + 2,
                            mainRect.radiusBottomRight + 2, mainRect.radiusBottomLeft + 2);
                ctx.strokeStyle = outerBorderColor;
                ctx.lineWidth = outerBorderWidth;
                ctx.stroke();

                // --- Inner border ---
                var inset = borderSpacing + innerBorderWidth / 2;
                roundedRect(
                    inset, inset,
                    width - inset * 2,
                    height - inset * 2,
                    Math.max(0, mainRect.radiusTopLeft - inset),
                    Math.max(0, mainRect.radiusTopRight - inset),
                    Math.max(0, mainRect.radiusBottomRight - inset),
                    Math.max(0, mainRect.radiusBottomLeft - inset)
                );
                ctx.strokeStyle = innerBorderColor;
                ctx.lineWidth = innerBorderWidth;
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

// **closing_key**

        }
    }
}
"""

qml_edges = """
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


class Frame(UI):
    """An application frame.

    A frame where visual elements are inserted. Usually called a "Window".
    It is not the main Frame of an application, and it has no movement 
    capabilities. It is ideal as a part of the main application, such as a 
    context menu or a tool panel.
    """
    def __init__(self, resizable: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._qml = qml
        if resizable:
            qml_init, qml_end = qml.split('\n// Resize corners')
            self._qml = qml_init + qml_edges + qml_end

        self._element_type = 'Frame'

        self.__height = 200
        self.__width = 200
        self.__spacing = 6

        self.__frame_hint = FrameHint.FRAME
        self.__frame_state = FrameState.FRAME
        self.__items = []
        self.__style = Style().style
        self.__visibility = 'Window.Windowed'
        self.__callbacks = {}
        self.__radius = 10, 10, 10, 10

    @property
    def frame_hint(self) -> FrameHint:
        """Frame behavior hint.

        FrameHint.BOTTOM → Always behind.
        FrameHint.FRAME → Normal behavior.
        FrameHint.POPUP → Popup Frame (does not appear in the taskbar).
        FrameHint.TOOL → Tool-like Frame (does not appear in the taskbar).
        FrameHint.TOP → Always on top.

        Use `FrameHint.TOOL` and `FrameHint.POPUP` inside a method to activate 
        them only when the window is ready; this will avoid styling issues.

        Use the `name` property to know which `FrameHint` it is.
        
        >>> self.frame_hint = FrameHint.FRAME
        >>> print(self.frame_hint.name)
        FRAME
        """
        return self.__frame_hint

    @frame_hint.setter
    def frame_hint(self, frame_hint: FrameHint) -> None:
        hints = {
            'BOTTOM': 'Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint',
            'FRAME': 'Qt.FramelessWindowHint',
            'POPUP': 'Qt.FramelessWindowHint | Qt.Popup',
            'TOOL': 'Qt.FramelessWindowHint | Qt.Tool',
            'TOP': 'Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint'}

        if self._obj:
            self._obj.setProperty('flags', int(frame_hint.value))
        else:
            self._qml = self._qml.replace(
                f'flags: {hints[self.__frame_hint.name]}',
                f'flags: {hints[frame_hint.name]}')

        self.__frame_hint = frame_hint

    @property
    def frame_state(self) -> FrameState:
        """The state of the Frame.

        A `FrameState` enum indicating whether the Frame is maximized, 
        minimized, full screen, in a normal frame or  hidden.
        """
        return self.__frame_state

    @frame_state.setter
    def frame_state(self, frame_state: FrameState = FrameState.FRAME) -> None:
        # Window.AutomaticVisibility  1     system default (normally Windowed)
        frame_state_value = {
            0: 'Window.Hidden', 1: 'Window.AutomaticVisibility',
            2: 'Window.Windowed', 3: 'Window.Minimized',
            4: 'Window.Maximized', 5: 'Window.FullScreen'}
        visibility = frame_state_value[frame_state.value]

        if self._obj:
            if frame_state.value == 2:
                self._obj.showNormal()
            elif frame_state.value == 4:
                self._obj.showMaximized()
            elif frame_state.value == 3:
                self._obj.showMinimized()
            elif frame_state.value == 5:
                self._obj.showFullScreen()
        else:
            self._qml = self._qml.replace(
                f'visibility: {self.__visibility}',
                f'visibility: {visibility}')

        self.__visibility = visibility
        self.__frame_state = frame_state

    @property
    def height(self) -> int:
        """Frame Height."""
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        if self._obj:
            self._obj.setProperty('_height', height)
        else:
            self._qml = self._qml.replace(
                f'_height: {self.__height}',
                f'_height: {height}')

        self.__height = height

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

        Warning: Only works as initialization (__init__), before the window is 
        rendered!
        """
        return self.__radius

    @radius.setter
    def radius(self, radius: tuple) -> None:
        if isinstance(radius, str):
            if not radius.isdigit():
                return
            radius = int(radius)

        if isinstance(radius, int):
            top_l, top_r, bottom_r, bottom_l = radius, radius, radius, radius
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
            frame = self.frame_state
            self.frame_state = (FrameState.MAXIMIZED
                if frame.name != 'MAXIMIZED' else FrameState.FULL_SCREEN)
            def _frame_state_(frame):
                self.frame_state = frame
            QtCore.QTimer.singleShot(300, lambda: _frame_state_(frame))
            
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
    def spacing(self) -> int:
        """Spacing Between Elements.

        The Frame contains a vertical Layout as a Column type, which manages 
        the position and spacing between Elements.
        """
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        if self._obj:
            self._obj.findChild(
                QtCore.QObject, 'mainColumnLayout').setProperty(
                    'spacing', spacing)
        else:
            self._qml = self._qml.replace(
                f'spacing: {self.__spacing}', f'spacing: {spacing}')

        self.__spacing = spacing

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
    def width(self) -> int:
        """Frame Width."""
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        if self._obj:
            self._obj.setProperty('_width', width)
        else:
            self._qml = self._qml.replace(
                f'_width: {self.__width}',
                f'_width: {width}')

        self.__width = width

    def add(self, obj: Layout | Element) -> Layout | Element:
        """Add items.

        Adds items such as Elements and Layouts to this Layout.
        
        :param obj: Element or Layout object type
        """
        if self._obj:
            obj._obj.setParentItem(self)
            # obj._obj.setParentItem(self._obj)
        else:
            setattr(self, obj.id, obj)

        self.__items.append(obj)
        return obj

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

    def items(self) -> list:
        """Items added to the Layout.

        List that includes Elements and other Layouts.
        """
        return self.__items

    def __str__(self) -> str:
        return "<class 'Frame'>"
