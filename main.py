#/usr/bin/env python3
from cell.core import Application
from cell.enum import Event, FrameState
from cell.ui.element import Button, Label
from cell.ui.frame import MainFrame
from cell.ui.layout import Column, Row, Scroll


class CustomElement(Row):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.custom_btn = self.add(Button('Button', 'document-save'))
        # self.custom_btn.margins = 5, 5, 5, 5
        self.custom_btn.connect(self.change_label)

        self.custom_lbl, self.num = self.add(Label('Label')), 0
        # self.custom_lbl.margins = 5, 5, 5, 5

    def change_label(self):
        self.num += 1
        self.custom_lbl.text = f'New Label {self.num}'


class View(MainFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Set
        # self.frame_state = FrameState.FULL_SCREEN
        self.height = 400
        self.width = 400

        # Elements
        self.label = self.add(Label('Hello'))
        self.label.margins = None, None, None, 100

        self.button = self.add(Button('Button', 'document-save'))
        # self.button.margins = 5, None, None, None
        self.button.connect(self.on_button)

        self.button_m = self.add(Button('Button 00', 'document-save'))
        self.button_m.connect(self.on_button)
        self.button_m

        self.scroll = self.add(Scroll())
        for item in range(5):
            btn = self.scroll.add(Button(f'Button {item}', 'document-save'))
            btn.connect(
                lambda item=item, btn=btn: self.on_num_button(item, btn),
                Event.MOUSE_HOVER)
            setattr(self, f'button_{item}', btn)

        self.ce = self.scroll.add(CustomElement())

        self.row = self.add(Row())
        self.row.add(Button('Button 1', 'document-save'))
        self.row.add(Button('Button 2', 'document-save'))

        self.column = self.add(Column())
        self.column.add(Button('Button 1', 'document-save'))
        self.column.add(Button('Button 2', 'document-save'))

        # Flags
        self.num = 0

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        self.scroll.spacing = 20
        self.label.margins = None, None, None, 0

    def on_num_button(self, num, btn):
        if getattr(self, f'button_{num}').is_mouse_hover():
            self.label.text = f'Button press: {num}'
            self.frame_state = FrameState.FRAME


if __name__ == '__main__':
    app = Application(View)
    app.exec()
