import abc
import typing

import kurses.buffer
import kurses.font_resources

K = typing.TypeVar("K", bound="TextureSurface")


class TextureSurface(abc.ABC, typing.Generic[K]):
    def __init__(self, surface: K, font: kurses.font_resources.FontResources, buffer: kurses.buffer.VirtualBuffer):
        self.__c_surface = surface
        self.__font = font
        self.__buffer = buffer

    @property
    def surface(self) -> K:
        return self.__c_surface

    @property
    def font(self) -> kurses.font_resources.FontResources:
        return self.__font

    @property
    def buffer(self) -> kurses.buffer.VirtualBuffer:
        return self.__buffer

    @abc.abstractmethod
    def present(self): ...
