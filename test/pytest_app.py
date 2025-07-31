#/usr/bin/env python3
import pathlib
import sys

from PySide6.QtTest import QTest
import pytest

sys.path.insert(0, pathlib.Path(__file__).parent.parent.parent)
from main import View
from cell.core import Application
from cell.ui import MainFrame, Button, Label, Scroll


@pytest.fixture(scope="session")
def qml_app():
    application = Application(View)
    app = application.frame()
    QTest.qWaitForWindowExposed(app._obj)
    return app

def test_button(qml_app):
    assert qml_app.button.text is not None

def test_button_text(qml_app):
    assert qml_app.button.text == 'Button'
    qml_app.on_button()
    assert qml_app.button.text == 'Clicked'
