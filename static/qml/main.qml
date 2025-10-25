import QtQuick
import QtQuick.Controls
import QtQuick.Controls.AdaptiveGlitch
import QtQuick.Layouts
import QtQuick.Shapes


MainFrame {
    id: root_app
    objectName: "root_app"

    Label {
        id: _app__label
        objectName: "_app__label"
        text: "Label xxx"
    }

    ColumnLayout {
        id: custom_col
        objectName: "custom_col"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: false
        Layout.leftMargin: 15

        Button {
            id: btn_top
            objectName: "btn_top"
            text: "TOOOp"
        }

        Label {
            id: _app__label_custom_col
            objectName: "_app__label_custom_col"
            text: "Label custom col"
        }
    }  // custom_col

    Button {
        id: _app__custom_btn
        objectName: "_app__custom_btn"
        icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
    }

    ColumnLayout {
        id: col
        objectName: "col"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: false
        Layout.leftMargin: 15

        Button {
            id: btn_click
            objectName: "btn_click"
            text: "Button 1"
        }

        Button {
            id: _app__btn2
            objectName: "_app__btn2"
            text: "Button 2"
        }

        Button {
            id: _app__btn3
            objectName: "_app__btn3"
            text: "Button 3"
        }

        Button {
            id: _app__btn4
            objectName: "_app__btn4"
            text: "Button 4"
        }

        Button {
            id: _app__btn5
            objectName: "_app__btn5"
            text: "Button 5"
        }

        Button {
            id: _app__btn6
            objectName: "_app__btn6"
            text: "Button 6"
        }

        Button {
            id: button0
            objectName: "button0"
            text: "Button range(0)"
        }

        Button {
            id: button1
            objectName: "button1"
            text: "Button range(1)"
        }
    }  // col
}  // root_app
