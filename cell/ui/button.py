#/usr/bin/env python3
import pathlib

from .element import Element


class Button(Element):
    """..."""
    def __init__(
            self, text: str = '', icon: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = text
        path = pathlib.Path(__file__).parent.parent
        self.__icon = path/'static'/'icons'/f'{icon}.svg'

        self.__layout_type = 'ColumnLayout'

        self.__align_key = 'Layout.alignment'
        self.__align_val = 'Qt.AlignHCenter'

        self.__align_fill_w_key = 'Layout.fillWidth'
        self.__align_fill_w_val = 'true'

        self.__align_fill_h_key = 'Layout.fillHeight'
        self.__align_fill_h_val = 'true'

        self.__top_margin_key = 'Layout.topMargin'
        self.__top_margin_val = '0'

        self.__right_margin_key = 'Layout.rightMargin'
        self.__right_margin_val = '0'

        self.__bottom_margin_key = 'Layout.bottomMargin'
        self.__bottom_margin_val = '0'

        self.__left_margin_key = 'Layout.leftMargin'
        self.__left_margin_val = '0'

        self.qml = (
            '\n'
            '\nButton {'
            f'\n    id: {self.object_id}'
            f'\n    objectName: "{self.object_id}"'
            f'\n    text: "{self.__text}"'
            f'\n    iconSource: "{self.__icon}"'
            f'\n    property string layoutType: "{self.__layout_type}"'

            f'\n    property bool fillWidth: {self.__align_fill_w_val}'
            f'\n    property bool fillHeight: {self.__align_fill_h_val}'

            f'\n    property string topMargin: "{self.__top_margin_val}"'
            f'\n    property string rightMargin: "{self.__right_margin_val}"'
            f'\n    property string bottomMargin: "{self.__bottom_margin_val}"'
            f'\n    property string leftMargin: "{self.__left_margin_val}"'

            f'\n    {self.__align_key}: {self.__align_val}'

            f'\n    {self.__align_fill_w_key}: fillWidth'
            f'\n    {self.__align_fill_h_key}: fillHeight'

            f'\n    {self.__top_margin_key}: topMargin'
            f'\n    {self.__right_margin_key}: rightMargin'
            f'\n    {self.__bottom_margin_key}: bottomMargin'
            f'\n    {self.__left_margin_key}: leftMargin'
            '\n// **closing_key**'
            f'\n}} // Button id: {self.object_id}')
