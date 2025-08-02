#!/usr/bin/env python3
from ..base import Frame


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


qml_popup = """
// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Layouts 1.15

// import QtQuick
// import QtQuick.Controls
// import QtQuick.Layouts

// import "elements"

Popup {
    id: painel
    width: 250
    height: parent.height - 40
    x: parent.width - width - 20
    y: 20
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Rectangle {
        color: "#2c2c2c"
        radius: 12
        border.color: "#555"
        border.width: 2
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 10

        Label { text: "Configurações"; font.pixelSize: 18; color: "white" }
        Button { text: "Salvar" }
        Button { text: "Cancelar"; onClicked: painel.close() }

// **closing_key**
    }
}
"""

qml_drawer = """
// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Layouts 1.15

// import QtQuick
// import QtQuick.Controls
// import QtQuick.Layouts

// import "elements"

Drawer {
    id: menuLateral
    edge: Qt.LeftEdge
    width: parent.width * 0.6
    height: parent.height

    background: Rectangle {
        color: "#1e1e1e"
        radius: 0
        border.color: "#666"
        border.width: 1
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        Label { text: "Menu"; font.pixelSize: 20; color: "white" }
        Button { text: "Item 1" }
        Button { text: "Item 2" }
        Button { text: "Fechar"; onClicked: menuLateral.close() }

// **closing_key**
    }
}
"""


class Context(Frame):
    """..."""
    def __init__(self, frame='popup', *args, **kwargs) -> None:
        super().__init__(resizable=True, *args, **kwargs)
        self.__qml_drawer = qml_drawer
        self.__qml_popup = qml_popup
        self._qml = self.__qml_popup if frame == 'popup' else self.__qml_drawer

        self._qml = qml_init + qml + qml_end
        self._element_type = 'Context'

    def __str__(self) -> str:
        return "<class 'Context'>"
