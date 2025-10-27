import QtQuick
import QtQuick.Controls
import QtQuick.Controls.AdaptiveGlitch
import QtQuick.Layouts
import QtQuick.Shapes


MainFrame {
    id: root_app
    objectName: "root_app"

    RowLayout {
        id: _app__row
        objectName: "_app__row"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true

        FrameCloseButton {
            id: _app__close_btn
            objectName: "_app__close_btn"
        }

        FrameMaxButton {
            id: _app__max_btn
            objectName: "_app__max_btn"
        }

        FrameMinButton {
            id: _app__min_btn
            objectName: "_app__min_btn"
        }
    }  // _app__row

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
        Layout.fillWidth: true

        Button {
            id: btn_top
            objectName: "btn_top"
            text: "TOOOp"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
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
        text: "Aplicar"
        Layout.fillWidth: true
        Layout.minimumHeight: 32
        checkable: true
    }

    Button {
        id: _app__custom_btn2
        objectName: "_app__custom_btn2"
        text: "Cancelar"
        Layout.fillWidth: true
        Layout.minimumHeight: 32
    }

    ToolButton {
        id: _app__tool_btn
        objectName: "_app__tool_btn"
        icon.source: "/usr/share/icons/breeze-dark/actions/16/edit-image-face-recognize.svg"
    }

    ToolButton {
        id: _app__tool_btn2
        objectName: "_app__tool_btn2"
        icon.source: "/home/user/Dev/github/glitch/static/icons/empty.svg"
        checkable: true
    }

    ColumnLayout {
        id: col
        objectName: "col"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true

        Button {
            id: _app__btn2
            objectName: "_app__btn2"
            text: "Button 2"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: _app__btn3
            objectName: "_app__btn3"
            text: "Button 3"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: _app__btn4
            objectName: "_app__btn4"
            text: "Button 4"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button0
            objectName: "button0"
            text: "Button range(0)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button1
            objectName: "button1"
            text: "Button range(1)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }
    }  // col
}  // root_app
