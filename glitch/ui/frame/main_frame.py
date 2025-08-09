#!/usr/bin/env python3
from ..base import Frame


qml = """
// MainFrame
        // Drag area
        Rectangle {
            id: dragArea
            objectName: "dragArea"
            // width: parent.width
            // width: parent.width - 20
            height: 20
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
// MainFrame
"""


class MainFrame(Frame):
    """The main Frame of the application.

    The frame where the application and its visual elements are built. This is 
    commonly called the "Window". Unlike a simple Frame, this is the 
    Application Frame, and has the ability to resize at the edges, in addition 
    to being able to be moved.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(resizable=True, *args, **kwargs)
        qml_init, qml_end = self._qml.split('// MainFrame')

        self._qml = qml_init + qml + qml_end
        self._name = 'MainFrame'

    def __str__(self) -> str:
        return "<class 'MainFrame'>"
