import abc
import enum
import typing

import kurses.buffer
import kurses.colors

DEFAULT_WINDOW_TITLE = "Virtual console"

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


class TypeCursor(enum.Enum):
    LINE = 0
    RECT = 1
    SOLID_RECT = 2
    VERTICAL = 3
    UNDERSCORE = 4


class VirtualConsole(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def __init__(self, depth_colors: int = 8, **kwargs):
        self._dt = 1.0
        self._resizable = True

        self.running = True
        self.depth_colors = kwargs["depth_colors"] if depth_colors in kwargs else 8
        self.encoding = kwargs["encoding"] if "encoding" in kwargs else EncodingFont.ASCII
        self.quality_font = kwargs["quality"] if "quality" in kwargs else QualityFont.BLENDED
        self.render = kwargs["render"] if "render" in kwargs else Rendering.SOFTWARE
        self.auto_clean_cache = kwargs["auto_clean_cache"] if "auto_clean_cache" in kwargs else True
        self.fps = kwargs["fps"] if "fps" in kwargs else 30
        self.auto_clean_buffer = kwargs["auto_clean_buffer"] if "auto_clean_buffer" in kwargs else True
        self.time_blink_cursor = kwargs["time_blink_cursor"] if "time_blink_cursor" in kwargs else 1
        self.time_wait_blink_cursor = kwargs["time_wait_blink_cursor"] if "time_wait_blink_cursor" in kwargs else 25
        self.type_cursor = kwargs["type_cursor"] if "type_cursor" in kwargs else TypeCursor.LINE
        self.cursor_color: kurses.colors.TupleColor = kwargs["cursor_color"] if "cursor_color" in kwargs else (128, 128, 128)

    @property
    def resizable(self) -> bool:
        return self._resizable

    @abc.abstractmethod
    def set_resizable(self, _bool: bool): ...

    @abc.abstractmethod
    def set_font(self, filename: str, ptsize=None): ...

    @property
    def dt(self) -> float:
        return self._dt

    @property
    @abc.abstractmethod
    def buffer(self) -> kurses.buffer.VirtualBuffer: ...

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
    def keyspressed(self) -> typing.List[str]: ...

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
    def push_events(self, event: T): ...

    @abc.abstractmethod
    def present(self): ...

    @abc.abstractmethod
    def quit(self): ...
