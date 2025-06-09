#/usr/bin/env python3


class Element(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """
        self.qml is instance: static/elements/<element>.qml
        """
        self.__class_name = 'Element'
        self.__id = '_' + str(id(self))
        self.__qml = self.__id

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

        self.qml_end = (
            '\n// **closing_key**'
            f'\n}} // {self.__class_name} id: {self.object_id}')

        self.qml = (
            '\n'
            f'\n{self.__class_name} {{'
            f'\n    id: {self.object_id}'
            f'\n    objectName: "{self.object_id}"'

            f'\n    property string layoutType: "{self.__layout_type}"'

            f'\n    property int alignment: {self.__align_val}'
            f'\n    {self.__align_key}: alignment'
            
            f'\n    property bool fillWidth: {self.__align_fill_w_val}'
            f'\n    property bool fillHeight: {self.__align_fill_h_val}'
            f'\n    {self.__align_fill_w_key}: fillWidth'
            f'\n    {self.__align_fill_h_key}: fillHeight'

            f'\n    property string topMargin: "{self.__top_margin_val}"'
            f'\n    property string rightMargin: "{self.__right_margin_val}"'
            f'\n    property string bottomMargin: "{self.__bottom_margin_val}"'
            f'\n    property string leftMargin: "{self.__left_margin_val}"'
            f'\n    {self.__top_margin_key}: topMargin'
            f'\n    {self.__right_margin_key}: rightMargin'
            f'\n    {self.__bottom_margin_key}: bottomMargin'
            f'\n    {self.__left_margin_key}: leftMargin'

            '\n// <property>'
            ) + self.qml_end

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self.__qml = self.__qml.replace(
            f'id: {self.__id}', f'id: {object_id}').replace(
            f'objectName: "{self.__id}"', f'objectName: "{object_id}"')
        self.__id = object_id

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml

    @property
    def class_name(self) -> str:
        """..."""
        return self.__class_name

    @class_name.setter
    def class_name(self, class_name: str) -> None:
        self.qml = self.qml.replace(
            f'\n{self.__class_name} {{', f'\n{class_name} {{')

        self.__class_name = class_name
