import collections
import dataclasses
import typing

import kurses.colors

DEFAULT_PTSIZE = 16


@dataclasses.dataclass
class CharacterAttribute:
    code: str = ''
    x: int = 0
    y: int = 0
    foreign: kurses.colors.TupleColor = (255, 255, 255)
    background: kurses.colors.TupleColor = (0, 0, 0)
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    blink: int = 0

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        _hash_tuple = (
            self.code, self.foreign, self.background, self.bold, self.italic, self.underline, self.strikethrough)

        return hash(_hash_tuple)

    def __bool__(self):
        return not self.code == ' '


@dataclasses.dataclass
class RectangleAttribute:
    x: int
    y: int
    w: int
    h: int
    color: kurses.colors.TupleColor


class VirtualBuffer:
    def __init__(self, columns: int, rows: int):
        """
        Initialize a VirtualBuffer object with the specified number of columns and rows.

        :param columns: Set number of columns.
        :param rows: Set number of rows.
        """
        self.resetall()
        self.__current_position = 0, 0
        self.__shape = rows, columns
        self.__queue: typing.Deque = collections.deque()

    def __iter__(self):
        for _obj in reversed(self.__queue):
            yield _obj

    def resize(self, columns: int, rows: int) -> None:
        """
        Resize (columns and rows) virtual console.

        :param columns: Set number of columns.
        :param rows: Set number of rows.
        :return: None
        """
        self.__shape = rows, columns

    def getbuffersize(self) -> typing.Tuple[int, int]:
        """
        Get buffer size (rows and columns) of Virtual buffer.

        :return: typing.Tuple[int, int]
        """
        return self.__shape

    @property
    def buffersize(self) -> typing.Tuple[int, int]:
        """
        Get buffer size (rows and columns) of Virtual buffer.

        :return: typing.Tuple[int, int]
        """
        return self.getbuffersize()

    @buffersize.setter
    def buffersize(self, shape: typing.Tuple[int, int]):
        """
        Set buffer size (rows and columns) of virtual buffer.

        :param shape: Shape of virtual buffer (rows and columns).
        :type shape:  typing.Tuple[int, int]
        :return: None
        """
        self.resize(*shape)

    def clreol(self) -> None:
        ...

    def clrscr(self) -> None:
        """
        Clear all character from virtual buffer.

        :return: None
        """
        self.__queue.clear()

    def wherex(self):
        """
        Get cursor position in X.

        :return: int
        """
        return self.__current_position[0]

    def wherey(self):
        """
        Get cursor position in Y.

        :return: int
        """
        return self.__current_position[1]

    @property
    def current_cursor(self) -> typing.Tuple[int, int]:
        """
        Get cursor position (x and y).

        :return: typing.Tuple[int, int]
        """
        return self.__current_position

    def gotoxy(self, x: int, y: int) -> None:
        """
        Set cursor position (x and y).

        :param x: X-axis position.
        :type x: int
        :param y: Y-axis position.
        :type y: int
        :return: None
        """
        self.__current_position = x, y

    def resetall(self):
        """
        Reset all attributes of virutal buffer.

        :return: None
        """
        self.__current_position = 0, 0
        self.__bold = False
        self.__italic = False
        self.__underline = False
        self.__strikethrough = False
        self.__foreign_color = 255, 255, 255
        self.__background_color = 0, 0, 0

    def set_background_color(self, color: kurses.colors.Color) -> None:
        """
        Set background color of character.

        :param color: Background color.
        :type color: kurses.colors.Color
        :return: None
        """
        if isinstance(color, int):
            color = kurses.colors.hex_to_rgb(color)

        self.__background_color = color

    def set_foreign_color(self, color: kurses.colors.Color) -> None:
        """
        Set foreign color of character.

        :param color: Foreign color.
        :type color: kurses.colors.Color
        :return: None
        """
        if isinstance(color, int):
            color = kurses.colors.hex_to_rgb(color)

        self.__foreign_color = color

    def bold(self, _bool: bool):
        """
        Set type bold character
        :param _bool: Set it to True or False.
        :type _bool: bool
        :return: None
        """
        self.__bold = _bool

    def italic(self, _bool: bool):
        """
        Set type italic character
        :param _bool: Set it to True or False.
        :type _bool: bool
        :return: None
        """
        self.__italic = _bool

    def underline(self, _bool: bool):
        """
        Set type underline character
        :param _bool: Set it to True or False.
        :type _bool: bool
        :return: None
        """
        self.__underline = _bool

    def strikethrough(self, _bool: bool):
        """
        Set type strikethrough character
        :param _bool: Set it to True or False.
        :type _bool: bool
        :return: None
        """
        self.__strikethrough = _bool

    def __create_character_attr(self, _chr, x, y):
        return CharacterAttribute(
            _chr, x, y,
            self.__foreign_color,
            self.__background_color,
            self.__bold,
            self.__italic,
            self.__underline,
            self.__strikethrough
        )

    def cputs(self, _chr: str):
        """
        Put char value into virtual buffer.

        :param _chr: Character.
        :type _chr: str
        :return: None
        """
        x, y = self.__current_position
        self.__queue.appendleft(self.__create_character_attr(_chr, x, y))
        self.gotoxy(x + 1, y)

    def print(self, _str: str):
        """
        Put string value into virtual buffer.

        :param _str: String.
        :type _str: str
        :return: None
        """
        self.cputsxy(self.wherex(), self.wherey(), _str)

    def putchxy(self, x: int, y: int, _chr: str) -> None:
        """
        Put character value into virtual buffer, with a position.

        :param x: X-axis position.
        :type x: int
        :param y: Y-axis position.
        :type y: int
        :param _chr: Character.
        :type _chr: str
        :return: None
        """
        self.__current_position = x, y
        self.__queue.appendleft(self.__create_character_attr(_chr, x, y))

    def cputsxy(self, x: int, y: int, _str: str) -> None:
        """
        Put string value into virtual buffer, with a position.

        :param x: X-axis position.
        :type x: int
        :param y: Y-axis position.
        :type y: int
        :param _str: String.
        :type _str: str
        :return: None
        """

        for _chr in _str:
            if _chr in "\n":
                y += 1
                continue

            self.putchxy(x, y, _chr)

            x += 1

        self.gotoxy(x, y)

    def putrect(self, x: int, y: int, w: int, h: int):
        """
        Put rect into virtual buffer, with a position.

        :param x: X-axis position.
        :type x: int
        :param y: Y-axis position.
        :type y: int
        :param w: Width of rect.
        :type w: int
        :param h: Height of rect.
        :type h: int
        :return: None
        """
        self.__queue.appendleft(
            RectangleAttribute(
                x, y,
                w, h,
                self.__background_color
            )
        )
