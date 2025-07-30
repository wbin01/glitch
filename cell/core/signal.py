#!/usr/bin/env python3
from PySide6 import QtCore


class BaseSignal(QtCore.QObject):
    """Event Signals.

    Signals are connections to events. When an event such as a mouse click 
    or other event occurs, a signal is sent. The signal can be assigned a 
    function to be executed when the signal is sent.
    """
    __signal = QtCore.Signal()

    def __init__(self, value: any = None, *args, **kwargs) -> None:
        """
        :param value: Object of any type. 
            Use when you need to pass and retrieve a value.
        """
        super().__init__(*args, **kwargs)
        self._obj = self.__signal

        self.__value = value

    @property
    def value(self) -> str:
        """Value of any type passed to the class constructor."""
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        self.__value = value

    def callback(self, function, *args) -> None:
        """Function to be executed.

        :param function: Function to be executed when the signal is sent.
        """
        self.__signal.connect(function)

    def remove_callback(self, function, *args) -> None:
        """Function to be disconnected."""
        self.__signal.disconnect(function)

    def send(self) -> None:
        """Send this signal.

        This method should be executed when you need to send the signal.
        """
        self.__signal.emit()

    def __str__(self) -> str:
        return "<class 'BaseSignal'>"


class Signal(object):
    """Signal object.

    Signals an event:

        MyObj:
            obj_signal = Signal()

            def obj_call(self):
                obj_signal.emit()


        my_obj = MyObj()
        my_obj.obj_signal.connect(lamba: print('Signal has been emitted'))

    When a signal is emitted, it performs the connected function.
    """
    def __init__(self):
        self.__signal = BaseSignal()
        self.__callback = None

    def callback(self) -> callable:
        """The callback sent."""
        return self.__callback

    @property
    def value(self) -> any:
        """Signal value.

            my_signal = self.obj_signal
            signal_value = my_signal.value
            self.my_signal.connect(lambda: print(signal_value))
        """
        return self.__signal.value

    @value.setter
    def value(self, value: any) -> None:
        self.__signal.value = value

    def connect(self, callback: callable = None) -> None:
        """Function to be executed.

            my_obj.obj_signal.connect(self.my_function)

        :param callback: Function to be executed when the signal is sent.
        """
        if not callback:
            if self.__callback:
                self.__signal.callback(self.__callback)
            else:
                print('Signal ERROR: Send callback')
        else:
            self.__callback = callback
            self.__signal.callback(self.__callback)

    def disconnect(self, callback: callable = None) -> None:
        """Function to be disconnected.

            my_obj.obj_signal.disconnect(self.my_function)

        :param callback: Function to be disconnect.
        """
        if not callback:
            self.__signal.remove_callback(self.__callback)
        else:
            self.__signal.remove_callback(callback)

    def emit(self) -> None:
        """Send this signal.

        This method should be executed when you need to send the signal.
        """
        self.__signal.send()

    def __str__(self) -> str:
        return "<class 'Signal'>"
