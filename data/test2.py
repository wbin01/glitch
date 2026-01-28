#!/usr/share/env python3
from glitch.core import Application
from glitch.enum import Hint, Shape, Align
# from glitch.ui import UI
# from glitch.ui.frame import AppFrame
# from glitch.ui.view import Button, Label
# from glitch.ui.layout import Column

# from glitch.ui import *
# from glitch.ui import layout
from glitch.ui import (
    AppFrame, Frame, MainFrame, Column, Row, Scroll, Header,
    Button, ToolButton, CloseButton, MaxButton, MinButton, ControlButtons,
    Label)


class CustomButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_text(self):
        return self.text


class CustomCol(Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.btn_top = self.add(CustomButton('TOOOp'))


class Window(AppFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.width = 300, 200, 400
        # self.height = 200, 100, 300
        # self.shape = Shape.MAX

        # self.__col_header_bar = self.add(Column())
        # self.__col_header_bar.align = Align.TOP

        # self.__header = self.__col_header_bar.add(Header())
        # self.__tb1 = self.__header.add(ToolButton('document-open'), right=False)
        # self.__tb1.checkable = True
        # self.__tb0 = self.__header.add(ToolButton('document-open'), right=True)
        # self.__tb0.checkable = True
        # self.__tb = self.__header.add(ToolButton('document-open'), right=True)
        # self.__tb.checkable = True
        # self.__tb._clicked_signal.connect(lambda: print('xxx'))

        # self.__max_btn = self.add(MaxButton())

        # self.__col = self.add(Column())
        # # self.__col.align = Align.BOTTOM_RIGHT, False
        # # self.__col.width = None, None, 500
        # self.lbl = self.__col.add(Label('Texto kkk'))

        # self.__button_custom_col = self.__col.add(Button('Button'))

        # self.__custom_btn = self.__col.add(CustomButton('Aplicar'))
        # self.__custom_btn.width = 500, 200, 600
        # self.__custom_btn._clicked_signal.connect(self.on_btn_click)
        # self.__custom_btn.checkable = True

        # self.__custom_btn2 = self.__col.add(CustomButton('Cancelar'))
        # self.__custom_btn2._clicked_signal.connect(self.close)
        # # self.__custom_btn2._hovered_signal.connect(lambda: print('HOVER'))

        # self.scroll = self.__col.add(Scroll())
        # self.scroll_row = self.scroll.add(Row())

        # self.__tool_btn = self.scroll_row.add(ToolButton('document-open'))
        # self.__tool_btn2 = self.scroll_row.add(ToolButton())
        # self.__tool_btn2.checkable = True

        # self.__btn2 = self.scroll.add(Button('Button 2', icon='document-open'))
        # self.__btn2._clicked_signal.connect(lambda: print(self.__btn3.text))

        # self.__btn3 = self.scroll.add(Button('Button 3'))
        # self.__btn3._clicked_signal.connect(lambda: print(self.__btn4.text))

        # self.__btn4 = self.scroll.add(Button('Button 4'))
        # self.__btn4._checked_signal.connect(lambda: print(self.__btn4.checkable))

        # for n in range(5):
        #     btn = self.scroll.add(Button(f'Button range({n})'))
        #     setattr(self, f'button{n}', btn)

    def on_btn_click(self):
        # print('---')
        # self.__col.align = Align.TOP_LEFT, True, True
        # self.__custom_btn.width = 100
        # # print(self.__custom_btn.width)
        # print(self.__col.align)
        # self.__btn4.checkable = True if not self.__btn4.checkable else False
        # self.__btn3.visible = True if not self.__btn3.visible else False
        # self.__btn2.enabled = True if not self.__btn2.enabled else False
        # print('checkable:', self.__btn4.checkable)
        # print('checked:', self.__btn4.checked)
        # self.lbl.enabled = True if not self.lbl.enabled else False
        # self.__tb1.enabled = True if not self.__tb1.enabled else False
        pass


if __name__ == '__main__':
    app = Application(Window)
    app.exec()
