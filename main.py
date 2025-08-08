#!/usr/bin/env python3
# from glitch import *
from glitch.core import Application, Signal
from glitch.enum import Align, Event, FrameShape, FrameHint, Size

# from glitch.ui import MainFrame, Frame, Column, Row, Scroll, Button, Label
from glitch.ui.element import Button, Label
from glitch.ui.frame import MainFrame, Frame
from glitch.ui.layout import Column, Panel, Row, Scroll


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
        # self.radius = 30
        # self.hint = FrameHint.TOP

        self.panel_side = 'left'
        self.panel_l = self.add(Panel())
        self.panel_l.radius = self.radius[0], 0, 0, self.radius[3]

        self.panel = self.add(Panel(Align.RIGHT))
        self.panel.radius = 0, self.radius[1], self.radius[2], 0
        
        self.panel_column = self.panel.add(Column())
        self.panel_column.margins = 10
        self.panel_button = self.panel_column.add(Button('Hello'))
        self.connect(lambda: self.panel.open(), Event.MOUSE_RIGHT_PRESS)

        # self.shape = FrameShape.MAXIMIZED  # FrameShape.FULL_SCREEN
        # self.spacing = 0
        self.size = 400
        
        # Elements
        self.label = self.add(Label('Panel slides from left'))
        self.label.margins = None, None, None, 100

        self.button = self.add(Button('Button X', 'document-save'))
        self.button.connect(self.on_button)

        self.button.size = Size.AUTO, 50
        self.button.size = 300, Size.AUTO
        self.button.size = Size.AUTO, None
        self.button.size = Size.FILL, Size.AUTO

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
        self.button.size = 300, Size.AUTO
        self.custom_num += 1

        if self.panel_side == 'right':
            self.panel_side = 'left'
            self.label.text = 'Panel slides from left'
        else:
            self.panel_side = 'right'
            self.label.text = 'Panel slides from right'

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        self.label.margins = Size.AUTO, Size.AUTO, Size.AUTO, 0
        if self.panel_side == 'right':
            self.panel.open()
        else:
            self.panel_l.open()

    def on_scroll_buttons(self, num):
        if getattr(self, f'button_{num}').is_mouse_hover():
            self.label.text = f'Button press: {num}'
            # self.shape = FrameShape.FRAME


if __name__ == '__main__':
    app = Application(View)
    app.exec()
