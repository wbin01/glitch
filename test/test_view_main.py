#/usr/bin/env python3
import os
import sys
import unittest

from PySide6.QtWidgets import QApplication
# from PySide6.QtQml import QQmlApplicationEngine
# from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cell.core import Application, Handler
from cell.ui import AppFrame, Button, Label, ScrollBox


class App(AppFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.button = self.add(Button('Button', 'document-save'))
        self.button.connect(self.on_button)

    def on_button(self):
        self.button.text = 'Clicked'


class TestQMLButton(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = Application(App)
        cls.app = cls.application.app_frame()

    def test_button(self):
        self.assertIsNotNone(self.app.button.text)

    def test_button_text(self):
        self.assertEqual(self.app.button.text, 'Button')
        # QTest.mouseClick(self.app.button._obj, Qt.LeftButton)
        self.app.on_button()
        self.assertEqual(self.app.button.text, 'Clicked')
