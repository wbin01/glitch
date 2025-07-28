#/usr/bin/env python3

qml = """
Item {
    id: rowLayout
    objectName: "rowLayout"
            
// **closing_key**
}
"""


class UI(object):
    """Base UI object."""
    def __init__(self, *args, **kwargs) -> None:
        self.__id = '_' + str(id(self))
        self.__qml = qml
        self.__obj = None

    @property
    def id(self) -> str:
        """Layout identifier."""
        if self._obj:
            return self._obj.property('id')
        return self.__id

    @id.setter
    def id(self, id: str) -> None:
        if self._obj:
            self._obj.setProperty('id', id)
            self._obj.setProperty('objectName', id)
        else:
            self.__qml = self.__qml.replace(
                f'id: {self.__id}', f'id: {id}').replace(
                f'objectName: "{self.__id}"', f'objectName: "{id}"')

        self.__id = id

    @property
    def _obj(self):
        """Qt Object.

        Internal object manipulated by the wrapper class.
        """
        return self.__obj

    @_obj.setter
    def _obj(self, obj) -> None:
        self.__obj = obj

    @property
    def _qml(self) -> str:
        """Qml code.

        Internal Qml handled by the wrapper class.
        """
        return self.__qml

    @_qml.setter
    def _qml(self, qml: str) -> None:
        self.__qml = qml
