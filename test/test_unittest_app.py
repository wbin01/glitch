#!/usr/bin/env python3
import pathlib
import sys
import unittest

sys.path.insert(0, pathlib.Path(__file__).parent.parent.parent)
from main import View
from cell.core import Application


class TestCellApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.application = Application(View)
        cls.app = cls.application.frame()
        # cls.application.exec()

    def test_button(self):
        self.assertIsNotNone(self.app.button.text)

    def test_button_text(self):
        self.assertEqual(self.app.button.text, 'Button')
        self.app.on_button()
        self.assertEqual(self.app.label.text, f'Button press: 1')
