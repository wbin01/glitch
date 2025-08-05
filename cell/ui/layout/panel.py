#!/usr/bin/env python3
from PySide6 import QtCore

from ..base import Layout


qml = """
Popup {
    id: panel  // <id>
    objectName: "panel"  // <objectName>
    property string qmlType: "Panel"  // <className>
    property string baseClass: "Layout"  // <baseClass>

    property color backgroundColor: "#222"
    property color borderColor: "#222"
    property int borderWidth: 1

    Canvas {
        anchors.fill: parent

        property int radiusTopLeft: 10
        property int radiusTopRight: 0
        property int radiusBottomRight: 0
        property int radiusBottomLeft: 10

        onPaint: {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);

            ctx.beginPath();
            ctx.moveTo(radiusTopLeft, 0);
            ctx.lineTo(width - radiusTopRight, 0);
            ctx.arcTo(width, 0, width, radiusTopRight, radiusTopRight);
            ctx.lineTo(width, height - radiusBottomRight);
            ctx.arcTo(width, height, width - radiusBottomRight, height, radiusBottomRight);
            ctx.lineTo(radiusBottomLeft, height);
            ctx.arcTo(0, height, 0, height - radiusBottomLeft, radiusBottomLeft);
            ctx.lineTo(0, radiusTopLeft);
            ctx.arcTo(0, 0, radiusTopLeft, 0, radiusTopLeft);
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


qml = """
Popup {
    id: panel  // <id>
    objectName: "panel"  // <objectName>
    property string qmlType: "Panel"  // <className>
    property string baseClass: "Layout"  // <baseClass>

    padding: 1 // Frame border
    width: 250
    height: parent.height + 9 // Frame padding (10) - Popup padding (1) = 9
    x: 0
    y: - 4  // Half of the Frame padding - outer border
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    clip: true

    transformOrigin: Item.Left

    property color backgroundColor: "#222"
    property color borderColor: "#222"
    property int borderWidth: 1

    property int radiusTopLeft: 10
    property int radiusTopRight: 0
    property int radiusBottomRight: 0
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

        // Connections {
        //     target: panel
        //     function onBackgroundColorChanged() { canv.requestPaint() }
        //     function onBorderColorChanged() { canv.requestPaint() }
        //     function onBorderWidthChanged() { canv.requestPaint() }
        // }

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
        self.id = f'_{id(self)}'
        self._element_type = 'Panel'
        self._qml = qml.replace(
            'canvas_panel', f'canvas{self.id}').replace('panel', self.id)

        self.__show_anim = QtCore.QParallelAnimationGroup()
        # self.__hide_anim = QtCore.QParallelAnimationGroup()
        self.__is_open = False
        self.__connect_close = False

        self.__radius = 10, 0, 0, 10

    @property
    def radius(self) -> tuple:
        """Sets the Panel radius.

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
