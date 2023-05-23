import abc
import typing

import kurses.font_resources
import kurses.stream

K = typing.TypeVar("K", bound="TextureSurface")


class TextureSurface(abc.ABC, typing.Generic[K]):
    def __init__(self, font: kurses.font_resources.FontResources, stream: kurses.stream.StreamBuffer):
        self.__font = font
        self.__stream = stream

    @property
    def font(self) -> kurses.font_resources.FontResources:
        return self.__font

    @property
    def stream(self) -> kurses.stream.StreamBuffer:
        return self.__stream

    @abc.abstractmethod
    def present(self, surface: K) -> K: ...

    @abc.abstractmethod
    def clear(self, surface: K) -> None: ...

    @property
    @abc.abstractmethod
    def current(self) -> typing.Union[K, None]: ...

    @property
    @abc.abstractmethod
    def size(self) -> typing.Tuple[int, int]: ...
