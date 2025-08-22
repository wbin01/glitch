#!/usr/bin/env python3
import pprint

# from glitch import *
from glitch.core import Application, Signal
from glitch.enum import Align, Event, FrameControl, FrameShape, FrameHint, Size
# from glitch.ui import MainFrame, Frame, Column, Panel, Row, Scroll, Button, Label
# from glitch.ui import *
from glitch.ui.element import Button, FrameCloseButton, FrameMaxButton, FrameMinButton, Label, ToolButton
from glitch.ui.layout import Column, MainFrame, Frame, Panel, Row, Scroll


class CustomElement(Row):
    # Global
    # button_clicked_signal = Signal()
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.button_clicked_signal = Signal()
        
        self.__custom_button = self.add(Button('Elves', 'document-open'))
        self.__custom_button.mouse_press_signal.connect(self.change_label)

        self.__custom_label, self.__num = self.add(Label('Label')), 0
        self.class_id('CustomElement')

        self.ola = 'Hello'

    @property
    def custom_button(self) -> Button:
        return self.__custom_button

    def change_label(self):
        self.button_clicked_signal.emit()
        self.__num += 1
        self.__custom_label.text = f'CustomElement clicked: {self.__num}'


class CustomElementX(Row):
    button_clicked_signal = Signal()
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__custom_button = self.add(Button('Button XX'))
        self.__custom_button.mouse_press_signal.connect(self.change_label)

        self.__custom_label, self.__num = self.add(Label('Label')), 0
        self.class_id('CustomElement')

        self.ola = 'Hello'

    @property
    def custom_button(self) -> Button:
        return self.__custom_button

    def change_label(self):
        self.button_clicked_signal.emit()
        self.__num += 1
        self.__custom_label.text = f'CustomElement clicked: {self.__num}'


class View(MainFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Set
        # self.radius = 6, 6, 0, 0
        # self.hint = FrameHint.TOP
        self.ola = 555

        self.header = self.add(Row())
        self.action_close = self.header.add(FrameCloseButton())
        self.action_max = self.header.add(FrameMaxButton())
        self.action_min = self.header.add(FrameMinButton())

        self.panel_side = 'left'
        self.panel_l = self.add(Panel())

        self.panel = self.add(Panel(Align.RIGHT))
        self.panel_column = self.panel.add(Column())
        self.panel_column.margins = 10
        self.panel_button = self.panel_column.add(Button('Hello'))
        self.mouse_right_press_signal.connect(lambda: self.panel.open())

        # self.shape = FrameShape.MAX  # FrameShape.FULL
        # self.spacing = 0
        self.size = 400
        
        # Elements
        self.label = self.add(Label('Panel slides from left'))
        self.label.margins = None, None, None, 100

        self.tool_button = self.add(ToolButton('document-save'))
        self.tool_button.checkable = True
        # self.tool_button.checked = True
        # self.tool_button.style_class = 'Panel'

        self.button = self.add(Button('Button check', 'document-open'))
        self.button.mouse_press_signal.connect(self.on_button)
        self.button.checkable = True
        # self.button.checked = True

        self.button.size = Size.AUTO, 50
        # self.button.size = 300, Size.AUTO
        # self.button.size = Size.AUTO, None
        # self.button.size = Size.FILL, Size.AUTO

        self.scroll = self.add(Scroll())
        self.scroll.margins = 10
        self.scroll_column = self.scroll.add(Column())
        self.scroll_column.margins = 10

        for num in range(5):
            button = self.scroll_column.add(Button(f'Button {num}'))
            button.mouse_hover_signal.connect(
                lambda num=num: self.on_scroll_buttons(num))
            setattr(self, f'button_{num}', button)

        self.custom0 = self.scroll_column.add(CustomElement())
        self.customx = self.scroll_column.add(CustomElementX())
        self.customx2 = self.scroll_column.add(CustomElementX())
        self.custom = self.scroll_column.add(CustomElement())
        self.custom.button_clicked_signal.connect(self.on_custom_clicked)

        self.row = self.add(Row())
        self.row.add(Button('Ok', 'dialog-ok-apply'))
        self.row.add(Button('Cancel', 'dialog-cancel'))

        self.column = self.add(Column())
        self.column.add(Button('Button 1'))

        self.button_2 = self.column.add(Button('Button 2', 'dialog-close'))
        self.button_2.mouse_press_signal.connect(lambda: print('button_2'))
        self.button_2.style_class = 'button_2'
        self.style['[button_2]'] = {
            'background_color': '#533', 'border_color': '#933'}

        # self.style['[ToolButton:hover]'] = {
        #     'background_color': '#533', 'border_color': '#993333'}
        # self.style['[ToolButton:checked:hover]'] = {
        #     'background_color': '#533', 'border_color': '#993333'}
        # self.style['[ToolButton:clicked]'] = {
        #     'border_color': '#FF993333', 'background_color': '#633'}
        # self.style['[ToolButton:checked]'] = {
        #     'background_color': '#533', 'border_color': '#88993333'}

        # self.button.style_class = 'ToolButton'

        # Flags
        self.num = 0
        self.custom_num = 0

        # print(self._application_frame)
        # print(self.panel._application_frame)
        # print(self.panel_column._application_frame)
        # print(self.label._application_frame)
        # print(self.label.style)
        # print(self.tool_button._application_frame)
        # print(self.button._application_frame)
        # print(self.scroll._application_frame)
        # print(self.scroll_column._application_frame)
        # print(self.custom0._application_frame)
        # print(self.customx._application_frame)
        # print(self.custom._application_frame)
        # print(self.column._application_frame)
        # print(self.button_2._application_frame)

    def on_custom_clicked(self):
        self.button.size = 300, Size.AUTO
        # self.button.margins = 100, 20
        self.custom_num += 1

        if self.panel_side == 'right':
            self.panel_side = 'left'
            self.label.text = 'Panel slides from left'
        else:
            self.panel_side = 'right'
            self.label.text = 'Panel slides from right'

    def on_button(self):
        print(self._platform.icon_theme)
        print(self._platform.accent_color)
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        # self.label.margins = Size.AUTO, Size.AUTO, Size.AUTO, 0
        # if self.panel_side == 'right':
        #     self.panel.open()
        # else:
        #     self.panel_l.open()

        # if self.shape == FrameShape.FRAME:
        #     self.shape = FrameShape.FULL
        # else:
        #     self.shape = FrameShape.FRAME

    def on_scroll_buttons(self, num):
        if getattr(self, f'button_{num}').is_mouse_hover():
            self.label.text = f'Button press: {num}'
            # self.shape = FrameShape.FRAME


if __name__ == '__main__':
    app = Application(View)
    app.exec()
