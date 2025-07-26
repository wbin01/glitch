#/usr/bin/env python3
from cell.core import Application, Handler
from cell.enum import Event, Orientation
from cell.ui import Button, Column, Label, MainFrame, Row, Scroll


class View(MainFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.num = 0

        self.height = 400

        self.label = self.add(Label('Hello'))
        self.label.margins = None, None, None, 10

        self.button = self.add(Button('Button', 'document-save'))
        self.button.margins = 5, None, None, None
        self.button.connect(self.on_button)

        self.button_m = self.add(Button('Button 00', 'document-save'))
        self.button_m.connect(self.on_button)

        self.scroll = self.add(Scroll())
        for item in range(5):
            btn = self.scroll.add(Button(f'Button {item}', 'document-save'))
            btn.margins = 5, 5, 5, 5
            btn.connect(lambda item=item: self.on_num_button(item))
            setattr(self, f'button_{item}', btn)

        self.scroll.add(Label('Olá'))

        self.row = self.add(Row())
        self.row.add(Button('Button 1', 'document-save'))
        self.row.add(Button('Button 2', 'document-save'))

        self.column = self.add(Column())
        self.column.add(Button('Button 1', 'document-save'))
        self.column.add(Button('Button 2', 'document-save'))

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        print('H antes:', self.height)
        self.height = 500
        print('H depois:', self.height)

    def on_num_button(self, num):
        self.label.text = f'Button press: {num}'


if __name__ == '__main__':
    app = Application(View)
    app.exec()
