import enum
import abc
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
    def __init__(self, depth_colors: int = 8, encoding: EncodingFont = EncodingFont.ASCII, quality: QualityFont = QualityFont.SOLID, render: Rendering = Rendering.SOFTWARE):
        self.running = True
        self.depth_colors = depth_colors
        self.encoding = encoding
        self.quality_font = quality
        self.render = render

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
