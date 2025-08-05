#!/usr/bin/env python3
# from cell import *
from cell.core import Application, Signal
from cell.enum import Event, FrameState, FrameHint

# from cell.ui import MainFrame, Frame, Column, Row, Scroll, Button, Label
from cell.ui.element import Button, Label
from cell.ui.frame import MainFrame, Frame
from cell.ui.layout import Column, Panel, Row, Scroll


class CustomElement(Row):
    button_clicked_signal = Signal()
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.custom_button = self.add(Button('Button'))
        self.custom_button.connect(self.change_label)
        self.custom_label, self.num = self.add(Label('Label')), 0

    def change_label(self):
        self.button_clicked_signal.emit()
        self.num += 1
        self.custom_label.text = f'CustomElement clicked: {self.num}'


class View(MainFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Set
        self.context = self.add(Panel())
        self.context_column = self.context.add(Column())
        self.context_column.margins = 10
        self.context_button = self.context_column.add(Button('Hello'))
        self.connect(lambda: self.context.open(), Event.MOUSE_RIGHT_PRESS)

        self.frame_state = FrameState.MAXIMIZED  # FrameState.FULL_SCREEN
        # self.spacing = 0
        self.height = 400
        self.width = 400
        self.radius = 10, 10, 0, 0

        # Elements
        self.label = self.add(Label('Hello'))
        self.label.margins = None, None, None, 100

        self.button = self.add(Button('Button', 'document-save'))
        self.button.connect(self.on_button)

        self.scroll = self.add(Scroll())
        self.scroll_column = self.scroll.add(Column())
        self.scroll_column.margins = 10

        for num in range(5):
            button = self.scroll_column.add(Button(f'Button {num}'))
            button.connect(
                lambda num=num: self.on_scroll_buttons(num), Event.MOUSE_HOVER)
            setattr(self, f'button_{num}', button)

        self.custom = self.scroll_column.add(CustomElement())
        self.custom.button_clicked_signal.connect(self.on_custom_clicked)

        self.row = self.add(Row())
        self.row.add(Button('Button 1'))
        self.row.add(Button('Button 2'))

        self.column = self.add(Column())
        self.column.add(Button('Button 1'))
        self.column.add(Button('Button 2'))

        # Flags
        self.num = 0
        self.custom_num = 0

    def on_custom_clicked(self):
        self.custom_num += 1
        self.label.text = f'Custom Element Button clicked {self.custom_num}'

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        self.label.margins = None, None, None, 0
        self.context.open()

    def on_scroll_buttons(self, num):
        if getattr(self, f'button_{num}').is_mouse_hover():
            self.label.text = f'Button press: {num}'
            # self.frame_state = FrameState.FRAME


if __name__ == '__main__':
    app = Application(View)
    app.exec()
