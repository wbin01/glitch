#/usr/bin/env python3
from ..base import Frame
from ...enum import FrameState


qml = """
// MainFrame
        // Drag area
        Rectangle {
            id: dragArea
            objectName: "dragArea"
            // width: parent.width
            // width: parent.width - 20
            height: 40
            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
                margins: 5  // margem de 10px nas laterais
            }
            color: "transparent"
            z: 2

            MouseArea {
                anchors.fill: parent
                drag.target: mainRect
                onPressed: logic.start_move()
            }
        }

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
// MainFrame
"""

class MainFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        qml_init, qml_end = self._qml.split('// MainFrame')
        self._qml = qml_init + qml + qml_end
        self._element_type = 'MainFrame'

        self.__frame_state = FrameState.FRAME
        self.__visibility = 'Window.Windowed'

    @property
    def frame_state(self) -> FrameState:
        """..."""
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
