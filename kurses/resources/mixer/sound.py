import abc
import typing


class Sound(abc.ABC):
    def __init__(self, filename: str):
        self.__filename = filename

    @property
    def filename(self):
        return self.__filename

    @abc.abstractmethod
    def play(self, loops: typing.Optional[int]):
        ...

    @abc.abstractmethod
    def stop(self):
        ...

    @abc.abstractmethod
    def volume(self, value: typing.Optional[int]) -> typing.Optional[int]:
        ...
