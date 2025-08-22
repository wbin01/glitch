#!/usr/bin/env python3
from xdg import IconTheme
from pathlib import Path

from ...core.application_style import style_value
from ...enum import Orientation, Size
from ...tools import color_converter


class IconMixin(object):
    """Icon mix object for implementing the icon property"""
    def __init__(
            self, icon: str = None, icon_size: int = 16,
            *args, **kwargs) -> None:
        super().__init__(icon=icon, icon_size=icon_size, *args, **kwargs)
        self.__path = Path(__file__).parent.parent.parent
        self.__icon_path = self.__path / 'static' / 'icons' / 'linux'
        self.__icon_theme = 'hicolor'

        # Args
        self.__icon_size = icon_size
        self.__icon = self.__get_icon_path(icon)

        # QML
        properties = '\n    iconSource: <icon>\n    // Property\n'
        self._qml = self._qml.replace(
            '\n    // Property', properties.replace('<icon>', self.__icon))

        # Properties
        self.icon = icon
        self.application_frame_signal.connect(self.__update_icon)

    @property
    def icon(self) -> str:
        """Icon name or path string."""
        return self.__icon

    @icon.setter
    def icon(self, icon: str) -> None:
        icon = self.__get_icon_path(icon)
        if self._obj:
            self._obj.setProperty('iconSource', icon.strip('"'))
        else:
            self._qml = self._qml.replace(
                f'iconSource: {self.__icon}', f'iconSource: {icon}')
        self.__icon = icon

    def __get_icon_path(self, icon_name: str | None) -> str | None:
        if not icon_name:
            return '""'

        elif '/' in icon_name:
            if not Path(icon_name).exists():
                return '""'
            return f'"{icon_name}"'

        else:
            icon_path = IconTheme.getIconPath(
                iconname=icon_name,
                size=self.__icon_size,
                theme=self.__icon_theme,
                extensions=['png', 'svg', 'xpm'])

            if icon_path:
                return f'"{icon_path}"'

            icon = icon_name + '.svg'
            path = self.__icon_path / icon
            return f'"{path}"' if path.exists() else '""'
                # impl callback
        """
        IconTheme.getIconPath(
            iconname=self.__icon_name,
            size=22,
            theme='breeze-dark',
            extensions=['png', 'svg', 'xpm']

        from PySide6.QtGui import QIcon
        icon = QIcon.fromTheme("document-save")
        
        ----
        Self linux impl
        
        ICON PATH
            User:
                Gtk
                /home/user/.icons/icon-theme/22x22/actions/icon-name.svg
                Qt
                /home/user/.icons/icon-theme/actions/22/icon-name.svg
            
            Gtk
            /usr/share/icons/icon-theme/22x22/actions/icon-name.svg
            Qt
            /usr/share/icons/icon-theme/actions/22/icon-name.svg
            
            Default sys
            /usr/share/icons/hicolor/22x22/actions/icon-name.png
            Default lib
            self.__icon_path / document-save.svg

        ROADMAP
            loop paths:
                check for: Gtk Qt icon-name icon-theme.png .svg
            else:
                or: Default sys
                or: Default lib
                or: callback-icon-path
        """

    def __update_icon(self) -> None:
        # Fix: DE updates dark icons without registering
        if hasattr(self._application_frame, '_platform'):
            self.__icon_theme = self._application_frame._platform.icon_theme

            is_dark = False
            if '[' + self._name + ']' in self._application_frame.style:
                is_dark = color_converter.is_dark(color_converter.hex_to_rgba(
                    style_value(
                        self._application_frame.style,
                        '[' + self._name + ']',
                        'background_color')))

            # TODO Condition for dark or light !=
            icon_theme = self._application_frame._platform.variant_icon_theme(
                self.__icon_theme, is_dark)

            icon = self.__icon.strip('"')
            icon_path = None
            for theme in [icon_theme, self.__icon_theme]:
                self._application_frame._platform.icon_theme = theme
                if theme:
                    icon_path = IconTheme.getIconPath(
                        iconname=Path(icon).stem,
                        size=self.__icon_size,
                        theme=theme,
                        extensions=['png', 'svg'])  # 'xpm'
                    if icon_path:
                        break

            self.icon = icon_path if icon_path else icon

    def __str__(self) -> str:
        return "<class 'IconMixin'>"


class MarginsMixin(object):
    """Margins mix object for implementing the margins property"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__margins = 0, 0, 0, 0

    @property
    def margins(self) -> tuple:
        """Sets the margins.

        A tuple with the 4 margin values. The values are in clockwise
        order: top, right, bottom and left respectively.

        Get:
            (5, 10, 5, 10)

        Set:
            It is not mandatory to pass all the values, the last value will be 
            used to fill in the missing ones:

            `margins = 5` is equivalent to `margins = 5, 5, 5, 5`
            `margins = 5, 10` is equivalent to `margins = 5, 10, 10, 10`

            Use `None` for a value to be automatic. `None` indicates that the 
            value is the same as before. Example:

                # Change vertical margins (top and bottom)
                `element.margins = 10, None, 10, None`

                # Change horizontal margins (right and left)
                `element.margins = None, 5, None, 5`
        """
        return self.__margins

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if isinstance(margins, str):
            margins = margins.replace(' ', '')
            margins = int(margins) if margins.isdigit() else margins.split(',')

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 1:
            top, right, bottom, left = (
                margins[0], margins[0], margins[0], margins[0])
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = self.__margins[0] if top is None else top
        right = self.__margins[1] if right is None else right
        bottom = self.__margins[2] if bottom is None else bottom
        left = self.__margins[3] if left is None else left

        if self._obj:
            self._obj.setProperty('topMargin', top)
            self._obj.setProperty('rightMargin', right)
            self._obj.setProperty('bottomMargin', bottom)
            self._obj.setProperty('leftMargin', left)
        else:
            self._qml = self._qml.replace(
                f'property int topMargin: {self.__margins[0]}',
                f'property int topMargin: {top}')
            self._qml = self._qml.replace(
                f'property int rightMargin: {self.__margins[1]}',
                f'property int rightMargin: {right}')
            self._qml = self._qml.replace(
                f'property int bottomMargin: {self.__margins[2]}',
                f'property int bottomMargin: {bottom}')
            self._qml = self._qml.replace(
                f'property int leftMargin: {self.__margins[3]}',
                f'property int leftMargin: {left}')

        self.__margins = top, left, bottom, right
        
        header = '[' + self._name + ']'
        if header in self._application_frame.style:
            self._application_frame.style[header]['margins'] = self.__margins

    def __str__(self) -> str:
        return "<class 'MarginsMixin'>"


class RadiusMixin(object):
    """Radius mix object for implementing the radius property"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__radius = 10, 10, 10, 10

    @property
    def radius(self) -> tuple:
        """Sets the radius.

        A tuple with the 4 radius values. The values are order: top-left, 
        top-right, bottom-right and bottom-left respectively:

            (10, 10, 10, 10)

        It is not mandatory to pass all the values, the last value will be 
        used to fill in the missing ones:

        `radius = 5` is equivalent to `radius = 5, 5, 5, 5`
        `radius = 5, 10` is equivalent to `radius = 5, 10, 10, 10`

        Use `None` for a value to be automatic. `None` indicates that the 
        value is the same as before. Example:

            # Change top-left and bottom-right
            `element.radius = 10, None, 10, None`

            # Change top-right and bottom-left
            `element.radius = None, 5, None, 5`

        Note! Only works as initialization (__init__), before the window is 
        rendered.
        """
        return self.__radius

    @radius.setter
    def radius(self, radius: str | tuple) -> None:
        if isinstance(radius, str):
            radius = radius.replace(' ', '')
            radius = int(radius) if radius.isdigit() else radius.split(',')

        if isinstance(radius, int):
            top_l, top_r, bottom_r, bottom_l = radius, radius, radius, radius
        elif len(radius) == 1:
            top_l, top_r, bottom_r, bottom_l = (
                radius[0], radius[0], radius[0], radius[0])
        elif len(radius) == 2:
            top_l, top_r, bottom_r, bottom_l = radius + (radius[1], radius[1])
        elif len(radius) == 3:
            top_l, top_r, bottom_r, bottom_l = radius + (radius[2],)
        else:
            top_l, top_r, bottom_r, bottom_l = radius[:4]

        top_l = self.__radius[0] if top_l is None else top_l
        top_r = self.__radius[1] if top_r is None else top_r
        bottom_r = self.__radius[2] if bottom_r is None else bottom_r
        bottom_l = self.__radius[3] if bottom_l is None else bottom_l

        if self._obj:
            # The code works, but is not desirable and has been disabled!
            return

            self._obj.setProperty('radiusTopLeft', top_l)
            self._obj.setProperty('radiusTopRight', top_r)
            self._obj.setProperty('radiusBottomRight', bottom_r)
            self._obj.setProperty('radiusBottomLeft', bottom_l)

            # TODO: Move to Application().processEvents()  works the right way
            self._obj.findChild(QtCore.QObject, 'canvas').requestPaint()
            shape = self.shape
            self.shape = (FrameShape.MAXIMIZED
                if shape.name != 'MAXIMIZED' else FrameShape.FULL_SCREEN)
            def _shape_(shape):
                self.shape = shape
            QtCore.QTimer.singleShot(300, lambda: _shape_(shape))
            
        else:
            self._qml = self._qml.replace(
                f'property int radiusTopLeft: {self.__radius[0]}',
                f'property int radiusTopLeft: {top_l}')
            self._qml = self._qml.replace(
                f'property int radiusTopRight: {self.__radius[1]}',
                f'property int radiusTopRight: {top_r}')
            self._qml = self._qml.replace(
                f'property int radiusBottomRight: {self.__radius[2]}',
                f'property int radiusBottomRight: {bottom_r}')
            self._qml = self._qml.replace(
                f'property int radiusBottomLeft: {self.__radius[3]}',
                f'property int radiusBottomLeft: {bottom_l}')

        self.__radius = top_l, top_r, bottom_r, bottom_l

        header = '[' + self._name + ']'
        if header in self._application_frame.style:
            self._application_frame.style[header]['border_radius'] = self.__radius

    def __str__(self) -> str:
        return "<class 'RadiusMixin'>"


class SizeMixin(object):
    """Size mix object for implementing the size property"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__fill_height = False
        self.__fill_width = True
        self.__height = 30
        self.__width = 100
        self.__size = self.__width, self.__height

    @property
    def size(self) -> tuple:
        """Frame width and height.

        Tuple like (100, 30).

        It is not mandatory to pass all the values, the last value will be 
        used to fill in the missing ones:

        `size = 100` is equivalent to `margins = 100, 100`

        Use `Size.AUTO` enum (or `None`) for a value to be automatic.
        `Size.AUTO` indicates that the value is the same as before. Example:

            # Change only the height
            `size = Size.AUTO, 50

            # Change only the width
            `size = 100, Size.AUTO

        Use `Size.FILL` to completely fill the space. Example:

            # Horizontal fill
            `size = Size.FILL, 30

            # Vertical fill
            `size = 100, Size.FILL
        """
        return self.__size

    @size.setter
    def size(self, size: str | tuple) -> None:
        if isinstance(size, str):
            size = int(size) if size.isdigit() else size.split(',')

        if isinstance(size, int):
            width, height = size, size
        elif len(size) == 1:
            width, height = size[0], size[0]
        elif len(size) >= 2:
            width, height = size[:2]

        width = Size.AUTO if width is None else width
        height = Size.AUTO if height is None else height

        enum_w = width if isinstance(width, Size) else False
        enum_h = height if isinstance(height, Size) else False
        width = self.__size[0] if not isinstance(width, int) else width
        height = self.__size[1] if not isinstance(height, int) else height

        if self._obj:
            self.__set_obj_size(enum_w, 'width', width)
            self.__set_obj_size(enum_h, 'height', height)
        else:
            self.__set_qml_size(enum_w, 'width', width)
            self.__set_qml_size(enum_h, 'height', height)

        self.__width = width
        self.__height = height
        self.__size = width, height
        self.size_signal.emit()

    def __set_obj_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        if enum:
            if enum == Size.FILL:
                self._obj.setProperty(fill, True)

            elif not self._obj.property(fill):
                self._obj.setProperty(width_height, value)
        else:
            self._obj.setProperty(fill, False)
            self._obj.setProperty(width_height, value)

    def __set_qml_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        old_value = self.__width if width_height == 'width' else self.__height

        if enum:
            if enum == Size.FILL:
                self._qml = self._qml.replace(f'{fill}: false',f'{fill}: true')

            elif f'property bool {fill}: false' in self._qml:
                self._qml = self._qml.replace(
                    f'{width_height}: {old_value}', f'{width_height}: {value}')
        else:
            self._qml = self._qml.replace(
                f'{fill}: true', f'{fill}: false').replace(
                    f'{width_height}: {old_value}', f'{width_height}: {value}')

    def __str__(self) -> str:
        return "<class 'SizeMixin'>"
