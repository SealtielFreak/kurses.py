import abc
import enum
import typing

import pyrogue.buffer_term

T = typing.TypeVar("T", bound="VirtualConsole")


class QualityFont(enum.Enum):
    SOLID = 0
    SHADED = 1
    LCD = 2
    BLENDED = 3


class EncodingFont(enum.Enum):
    ASCII = 0
    UTF_8 = 1
    UNICODE = 2


class Rendering(enum.Enum):
    HARDWARE = 0
    SOFTWARE = 1


class VirtualConsole(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def __init__(self, depth_colors: int = 8, **kwargs):
        self.running = True
        self.depth_colors = kwargs["depth_colors"] if depth_colors in kwargs else 8
        self.encoding = kwargs["encoding"] if "encoding" in kwargs else EncodingFont.ASCII
        self.quality_font = kwargs["quality"] if "quality" in kwargs else QualityFont.SHADED
        self.render = kwargs["render"] if "render" in kwargs else Rendering.SOFTWARE
        self.automatic_cleaner = kwargs["automatic_cleaner"] if "automatic_cleaner" in kwargs else True
        self.fps = kwargs["fps"] if "fps" in kwargs else 30

        self._dt = 1.0

    @property
    def dt(self) -> float:
        return self._dt

    @property
    @abc.abstractmethod
    def buffer(self) -> pyrogue.buffer_term.BufferTerm: ...

    @abc.abstractmethod
    def set_target(self, target: typing.Callable[[None], None]): ...

    @property
    @abc.abstractmethod
    def background(self) -> typing.Tuple[int, int, int]: ...

    @background.setter
    @abc.abstractmethod
    def background(self, background: typing.Tuple[int, int, int]): ...

    @abc.abstractmethod
    def main_loop(self): ...

    @abc.abstractmethod
    def set_title(self, _str: str): ...

    @abc.abstractmethod
    def keyspressed(self) -> typing.List[chr]: ...

    @property
    @abc.abstractmethod
    def window(self) -> T: ...

    @property
    @abc.abstractmethod
    def surface(self) -> T: ...

    @property
    @abc.abstractmethod
    def font(self) -> T: ...

    @abc.abstractmethod
    def clear_cache(self): ...

    @abc.abstractmethod
    def events(self, event: T): ...

    @abc.abstractmethod
    def present(self): ...

    @abc.abstractmethod
    def quit(self): ...
