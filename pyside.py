import sys
from PySide6.QtCore import QUrl, QByteArray
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent


def main_pyside():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    qml_code = """
    import QtQuick 2.15
    import QtQuick.Controls 2.15

    ApplicationWindow {
        width: 400
        height: 300
        visible: true
        title: "QML de String"
        flags: Qt.FramelessWindowHint

        Button {
            text: "Clicked"
            anchors.centerIn: parent
            onClicked: console.log("Botão clicado!")
        }
    }
    """
    component = QQmlComponent(engine)
    component.setData(QByteArray(qml_code.encode("utf-8")), QUrl())
    if component.isError():
        print("Erro:", component.errors())
        sys.exit(1)

    window = component.create()
    sys.exit(app.exec())


if __name__ == '__main__':
    main_pyside()
