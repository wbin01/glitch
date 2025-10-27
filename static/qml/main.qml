import QtQuick
import QtQuick.Controls
import QtQuick.Controls.AdaptiveGlitch
import QtQuick.Layouts
import QtQuick.Shapes


AppFrame {
    id: root_app
    objectName: "root_app"

    RowLayout {
        id: _app__control_btn
        objectName: "_app__control_btn"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true
        Layout.margins: 5

        FrameCloseButton {
            id: _framecontrolbuttons__close_btn
            objectName: "_framecontrolbuttons__close_btn"
        }

        FrameMaxButton {
            id: _framecontrolbuttons__max_btn
            objectName: "_framecontrolbuttons__max_btn"
        }

        FrameMinButton {
            id: _framecontrolbuttons__min_btn
            objectName: "_framecontrolbuttons__min_btn"
        }
    }  // _app__control_btn

    RowLayout {
        id: _app__row
        objectName: "_app__row"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true
        Layout.margins: 5

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

        ToolButton {
            id: _app__tool
            objectName: "_app__tool"
            icon.source: "/usr/share/icons/breeze-dark/actions/16/edit-image-face-recognize.svg"
            checkable: true
        }

        ToolButton {
            id: _app__tool2
            objectName: "_app__tool2"
            icon.source: "/usr/share/icons/breeze-dark/actions/16/edit-image-face-recognize.svg"
            checkable: true
        }

        ToolButton {
            id: _app__tool3
            objectName: "_app__tool3"
            icon.source: "/usr/share/icons/breeze-dark/actions/16/edit-image-face-recognize.svg"
            checkable: true
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

    Scroll {
        id: scroll
        objectName: "scroll"
        spacing: 6
        clip: true
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true

        RowLayout {
            id: scroll_row
            objectName: "scroll_row"
            spacing: 6
            clip: true
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true

            ToolButton {
                id: _app__tool_btn
                objectName: "_app__tool_btn"
                icon.source: "/usr/share/icons/breeze-dark/actions/16/edit-image-face-recognize.svg"
            }

            ToolButton {
                id: _app__tool_btn2
                objectName: "_app__tool_btn2"
                icon.source: "/usr/share/icons/breeze-dark/actions/16/edit-image-face-recognize.svg"
                checkable: true
            }
        }  // scroll_row

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

        Button {
            id: button2
            objectName: "button2"
            text: "Button range(2)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button3
            objectName: "button3"
            text: "Button range(3)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button4
            objectName: "button4"
            text: "Button range(4)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button5
            objectName: "button5"
            text: "Button range(5)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button6
            objectName: "button6"
            text: "Button range(6)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button7
            objectName: "button7"
            text: "Button range(7)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button8
            objectName: "button8"
            text: "Button range(8)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }

        Button {
            id: button9
            objectName: "button9"
            text: "Button range(9)"
            Layout.fillWidth: true
            Layout.minimumHeight: 32
        }
    }  // scroll
}  // root_app
