import abc
import typing

import kurses.graphics

H = typing.TypeVar("H", bound="BitmapSurface")


class BitmapSurface(abc.ABC, typing.Generic[H]):
    def __init__(self, graphics: kurses.graphics.GraphicsBuffer):
        self.__graphics = graphics

    @property
    def graphics(self):
        return self.__graphics

    @abc.abstractmethod
    def create(self, surface: H): ...

    @abc.abstractmethod
    def destroy(self): ...

    @abc.abstractmethod
    def present(self, surface: H) -> H: ...

    @abc.abstractmethod
    def clear(self, surface: H) -> None: ...

    @property
    @abc.abstractmethod
    def current(self) -> typing.Union[H, None]: ...

    @property
    @abc.abstractmethod
    def size(self) -> typing.Tuple[int, int]: ...

    @abc.abstractmethod
    def resize(self, width: int, height: int) -> None: ...
