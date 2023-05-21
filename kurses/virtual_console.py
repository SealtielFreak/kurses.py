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


class VirtualConsole(abc.ABC, typing.Generic[T]):
    def __init__(self, depth_colors: int = 8, **kwargs):
        """
        VirtualConsole constructor

        :param depth_colors: Depth colors of all characters, with default value 8.
        :type depth_colors: int
        :param kwargs: Optional arguments
        :keyword encoding: Select type encoding (ASCII, UTF-8 or UNICODE).
        :type encoding: EncodingFont
        :keyword quality_font: Select type quality textures of characters (Solid, shaded, LCD or Blended).
        :type quality_font: QualityFont
        :keyword render: Select type rendering between Hardware (only default SDL2) or Software (optional in SDL2 for old computers and only default in Pygame).
        :type render: Rendering
        :keyword auto_clean_cache: Auto cleaner textures cache, with default value True.
        :type auto_clean_cache: bool
        :keyword fps: Limit frames per second, with default value 30.
        :type fps: int
        :keyword auto_clean_buffer: Auto cleaner console buffer, with default value True.
        :type auto_clean_buffer: bool
        """
        self._dt = 1.0
        self._resizable = True

        self.running = True
        self.depth_colors = depth_colors
        self.encoding = kwargs.get("encoding", EncodingFont.ASCII)
        self.quality_font = kwargs.get("quality", QualityFont.BLENDED)
        self.render = kwargs.get("render", Rendering.SOFTWARE)
        self.auto_clean_cache = kwargs.get("auto_clean_cache", True)
        self.fps = kwargs.get("fps", 30)
        self.auto_clean_buffer = kwargs.get("auto_clean_buffer", True)

    @property
    def resizable(self) -> bool:
        """
        Get the resizable property of the console.

        :return: The resizable property of the console.
        :rtype: bool
        """
        return self._resizable

    @abc.abstractmethod
    def set_resizable(self, _bool: bool): ...

    @abc.abstractmethod
    def set_font(self, filename: str, ptsize=None): ...

    @property
    def dt(self) -> float:
        """
        Get the delta time of all loop program.

        :return: Delta time.
        :rtype: float
        """
        return self._dt

    @property
    @abc.abstractmethod
    def buffers(self) -> list[kurses.buffer.VirtualBuffer]:
        """
        Get list of virtual buffers.

        :return: list[kurses.buffer.VirtualBuffer]
        """
        ...

    @abc.abstractmethod
    def set_target(self, target: typing.Callable[[None], None]):
        """
        Set main loop function.

        :param target: Main loop function.
        :type target: typing.Callable[[None], None]
        :return: None
        """
        ...

    @property
    @abc.abstractmethod
    def background(self) -> kurses.colors.TupleColor:
        """
        Get background color of console.

        :return: kurses.colors.TupleColor
        """
        ...

    @background.setter
    @abc.abstractmethod
    def background(self, background: kurses.colors.TupleColor):
        """
        Set background color of console.

        :param background: Background color.
        :type background: kurses.colors.TupleColor
        :return: None
        """
        ...

    @abc.abstractmethod
    def main_loop(self):
        """
        Run virtual console, with all background service (SDL2 or Pygame).

        :return: None
        """
        ...

    @abc.abstractmethod
    def set_title(self, _str: str):
        """
        Set title of virtual console (Windows).

        :type _str: String of title.
        :type _str: str
        :return: None
        """
        ...

    @abc.abstractmethod
    def keyspressed(self) -> typing.List[str]:
        """
        Get all key pressed.

        :return: typing.List[str]
        """
        ...

    @property
    @abc.abstractmethod
    def window(self) -> T:
        """
        Get window instance.

        :return: T
        """
        ...

    @property
    @abc.abstractmethod
    def surface(self) -> T:
        """
        Get surface instance.

        :return: T
        """
        ...

    @property
    @abc.abstractmethod
    def font(self) -> T:
        """
        Get font instance.

        :return: T
        """
        ...

    @abc.abstractmethod
    def clear_cache(self):
        """
        Clear texture cache.

        :return: None
        """
        ...

    @abc.abstractmethod
    def push_events(self, event: T):
        """
        Push type event.

        :param event: Type event.
        :type event: T
        :return: None
        """
        ...

    @abc.abstractmethod
    def present(self):
        """
        Update surface.

        :return: None
        """
        ...

    @abc.abstractmethod
    def quit(self):
        """
        Quit virtual console.

        :return: None
        """
        ...
