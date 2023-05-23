import abc
import enum
import typing

import kurses.colors

DEFAULT_WINDOW_TITLE = "Virtual console"

T = typing.TypeVar("T", bound="VirtualConsole")


class Rendering(enum.Enum):
    HARDWARE = 0
    SOFTWARE = 1


class VirtualConsole(abc.ABC, typing.Generic[T]):
    def __init__(self, *args, **kwargs):
        """
        VirtualConsole constructor

        :keyword fps: Limit frames per second, with default value 30.
        :type fps: int
        """
        self._dt = 1.0
        self._resizable = True

        self.fps = kwargs.get("fps", 30)
        self.running = True

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
