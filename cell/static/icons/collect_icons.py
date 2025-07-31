#!/usr/bin/env python3
import pathlib


class CollectIcons(object):
	def __init__(self):
		self.__path = pathlib.Path(__file__).parent
		self.__icon_names_path = self.__path / 'icon_naming_specification.txt'
		self.__icon_names = self.__set_icon_names()

	def __set_icon_names(self) -> list:
		with open(self.__icon_names_path, 'r') as icon_names_file:
			icon_names = icon_names_file.readlines()

		names = []
		for name in icon_names:
			names.append(f'{name.strip()}')

		return names

	def collect(self) -> None:
		for name in self.__icon_names:
			print(name)


if __name__ == '__main__':
	icons = CollectIcons()
	icons.collect()
