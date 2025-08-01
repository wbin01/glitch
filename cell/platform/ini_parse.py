#!/usr/bin/env python3
import os


class IniParse(object):
    """INI files object.

    Converts INI files into a dictionary to provide easy access.
    """
    def __init__(self, url: str) -> None:
        """Class constructor

        Initialize class properties.

        :param url: String from a desktop file like: "/path/inifile"
        """
        self.__url = os.path.abspath(url)
        self.__content_full = False
        self.__content = {
        '[Frame-Border]': {
            'background': 'rgba(0, 0, 0, 0.00)',
            'border': '1px rgba(50, 50, 50, 0.80)',
            'border_radius': '10px',
            'padding': '0px',
            'margin': '0px'},
        '[Frame-Shadow]': {
            'background': 'rgba(0, 0, 0, 0.00)',
            'border': '1px rgba(0, 0, 0, 0.20)',
            'border_radius': '10px',
            'padding': '0px'},
        '[MainFrame-Border]': {
            'background': 'rgba(0, 0, 0, 0.00)',
            'border': '1px rgba(50, 50, 50, 0.80)',
            'border_radius': '10px',
            'padding': '0px'},
        '[MainFrame-Shadow]': {
            'background': 'rgba(0, 0, 0, 0.00)',
            'border': '1px rgba(0, 0, 0, 0.20)',
            'border_radius': '10px',
            'padding': '0px',
            'margin': '0px'}
        }

    @property
    def content(self) -> dict:
        """Contents of a INI file as a dictionary

        Example:
        >>> ini_file = IniParse(
        ... url='/usr/share/applications/firefox.desktop')
        >>> ini_file.content['[Desktop Entry]']['Name']
        'Firefox Web Browser'
        >>> ini_file.content['[Desktop Entry]']['Type']
        'Application'
        >>> for key in ini_file.content.keys():
        ... print(key)
        ...
        [Desktop Entry]
        [Desktop Action new-window]
        [Desktop Action new-private-window]
        >>>
        >>> ini_file.content['[Desktop Action new-window]']['Name']
        'Open a New Window'
        """
        if not self.__content_full:
            self.__parse_file_to_dict()
            self.__content_full = True
        return self.__content

    @property
    def url(self) -> str:
        """URL of the INI file

        The URL used to construct this object, like: "/path/inifile".
        """
        return self.__url

    def __parse_file_to_dict(self) -> None:
        with open(self.__url, 'r') as ini_file:
            ini_text = ini_file.read()

        for scope in ini_text.split('['):
            if not scope.strip().startswith('#'):
                scope = f'[{scope.strip()}'

            header, key, value = '', '', ''
            for line in scope.split('\n'):
                if line and not line.strip().startswith('#'):
                    line = line.strip()

                    if line.startswith('['):
                        header = line
                        self.__content[header] = {}

                    elif '=' in line:
                        key, value = line.split('=')
                        self.__content[header][key] = value

                    else:
                        value = self.__content[header][key] + ' ' + line
                        self.__content[header][key] = value

        if '[MainFrame]' in self.__content:
            border_radius = self.__border_radius_str_to_list(
                self.__content['[MainFrame]']['border_radius'])

            border = int(self.__content['[MainFrame]']['border'
                ].split()[0].replace('px', '').strip())
            bd_radius = '{}px {}px {}px {}px'.format(
                int(border_radius[0]) + border, int(border_radius[1]) + border,
                int(border_radius[2]) + border, int(border_radius[3]) + border)


            self.__content['[MainFrame-Shadow]']['border_radius'] = bd_radius
            self.__content['[MainFrame-Border]']['border_radius'] = bd_radius
            self.__content['[MainFrame-Border]']['border'] = self.__content['[MainFrame]']['border']
            self.__content['[MainFrame]']['border'] = '0px'

        if '[Frame]' in self.__content:
            border_radius = self.__border_radius_str_to_list(
                self.__content['[Frame]']['border_radius'])
            bd_radius = '{}px {}px {}px {}px'.format(
                int(border_radius[0]) + 1, int(border_radius[1]) + 1,
                int(border_radius[2]) + 1, int(border_radius[3]) + 1)
            self.__content['[Frame-Shadow]']['border_radius'] = bd_radius
            self.__content['[Frame-Border]']['border_radius'] = bd_radius
            self.__content['[Frame-Border]']['border'] = self.__content['[Frame]']['border']
            self.__content['[Frame]']['border'] = '0px'

    @staticmethod
    def __border_radius_str_to_list(border: str) -> list:
        bd = border.strip().replace('  ', ' ').split('px')
        if len(bd) == 2:
            n1, n2, n3, n4 = bd[0], bd[0], bd[0], bd[0]
        else:
            n1, n2, n3, n4, _ = bd

        return [n1, n2, n3, n4]

    def __str__(self) -> str:
        return f'<IniParse: {self.__url_basename}>'
