#/usr/bin/env python3
from cell.core import Application
from cell.enum import Event
from cell.ui.element import Button, Label
from cell.ui.frame import MainFrame
from cell.ui.layout import Column, Row, Scroll
from cell.ui.base import Layout, UI


class ColumnX(UI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.id = 'ustomButton'
        # self.custom_btn = self.add(Button('Custom Button', 'document-save'))
        # self.custom_lbl = self.add(Label('Custom Label'))


class View(MainFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.num = 0

        # self.height = 400

        self.label = self.add(Label('Hello'))
        self.label.margins = None, None, None, 10

        self.button = self.add(Button('Button', 'document-save'))
        self.button.margins = 5, None, None, None
        self.button.connect(self.on_button)

        self.button_m = self.add(Button('Button 00', 'document-save'))
        self.button_m.connect(self.on_button)
        self.button_m

        self.scroll = self.add(Scroll())
        for item in range(5):
            btn = self.scroll.add(Button(f'Button {item}', 'document-save'))
            btn.margins = 5, 5, 5, 5
            btn.connect(
                lambda item=item, btn=btn: self.on_num_button(item, btn),
                Event.MOUSE_HOVER)
            setattr(self, f'button_{item}', btn)

        self.scroll.add(Label('Olá'))

        self.row = self.add(Row())
        self.row.add(Button('Button 1', 'document-save'))
        self.row.add(Button('Button 2', 'document-save'))

        self.column = self.add(Column())
        self.column.add(Button('Button 1', 'document-save'))
        self.column.add(Button('Button 2', 'document-save'))

        # self.maximized = True
        self.rr = self.add(Row())
        self.cc = self.add(Column())
        self.cx = self.add(ColumnX())

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        self.height = 400

    def on_num_button(self, num, btn):
        if getattr(self, f'button_{num}').is_mouse_hover():
            self.label.text = f'Button press: {num}'
            # self.maximized = False


if __name__ == '__main__':
    app = Application(View)
    app.exec()
