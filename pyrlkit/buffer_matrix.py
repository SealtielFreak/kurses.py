import abc
import collections
import dataclasses
import typing

TupleColor = typing.Tuple[int, int, int]
Color = typing.Union[TupleColor, int]


def rgb_to_hex(rgb: TupleColor) -> int:
    return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]


def hex_to_rgb(hex_color: int) -> TupleColor:
    hex_str = hex(hex_color)[2:]

    hex_str = hex_str.rjust(6, '0')

    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)

    return r, g, b


@dataclasses.dataclass
class CharacterAttribute:
    code: chr = ''
    x: int = 0
    y: int = 0
    foreign: TupleColor = (255, 255, 255)
    background: TupleColor = (0, 0, 0)
    bold: bool = False
    italic: bool = False
    underline: bool = False

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash((self.code, self.foreign, self.background, self.bold, self.italic, self.underline))

    def __bool__(self):
        return self.code != ''


ArrayCharacterAttribute = typing.List[CharacterAttribute]
MatrixCharacterAttribute = typing.List[ArrayCharacterAttribute]
DequeCharacterAttribute = typing.Deque[CharacterAttribute]


def create_matrix(rows: int, cols: int) -> MatrixCharacterAttribute:
    return [[CharacterAttribute() for _ in range(rows)] for _ in range(cols)]


def copy_memset(a: MatrixCharacterAttribute, b: MatrixCharacterAttribute) -> MatrixCharacterAttribute:
    for y, row in enumerate(a):
        for x, c in enumerate(a):
            try:
                b[y][x] = a[y][x]
            except IndexError:
                pass

    return b


class BufferMatrix:
    def __init__(self, columns: int, rows: int):
        self.__current_character = CharacterAttribute()
        self.__shape = rows, columns
        self.__matrix = create_matrix(rows, columns)

    def __iter__(self):
        return iter([k[:] for k in self.__matrix])

    @property
    def queue(self) -> DequeCharacterAttribute:
        return collections.deque(iter(self))

    def resize(self, columns: int, rows: int) -> None:
        self.__shape = rows, columns
        self.__matrix = copy_memset(self.__matrix, create_matrix(rows, columns))

    @abc.abstractmethod
    def getbuffersize(self) -> typing.Tuple[int, int]:
        return self.__shape

    @property
    def buffersize(self) -> typing.Tuple[int, int]:
        return self.getbuffersize()

    @buffersize.setter
    def buffersize(self, shape: typing.Tuple[int, int]):
        self.resize(*shape)

    def clreol(self) -> None:
        ...

    def clrscr(self) -> None:
        self.__matrix = create_matrix(*self.buffersize)

    def wherex(self):
        return self.__current_character.x

    def wherey(self):
        return self.__current_character.y

    def gotoxy(self, x: int, y: int) -> None:
        self.__current_character.x = x
        self.__current_character.y = y

    def set_background_color(self, color: Color) -> None:
        if isinstance(color, int):
            color = hex_to_rgb(color)

        self.__current_character.background = color

    def set_foreign_color(self, color: Color) -> None:
        if isinstance(color, int):
            color = hex_to_rgb(color)

        self.__current_character.foreign = color

    def bold(self, _bool: bool):
        self.__current_character.bold = _bool

    def italic(self, _bool: bool):
        self.__current_character.italic = _bool

    def underline(self, _bool: bool):
        self.__current_character.underline = _bool

    def cputs(self, _chr: chr):
        self.__current_character.code = _chr
        x, y = self.__current_character.x, self.__current_character.y
        self.__matrix[y][x] = dataclasses.replace(self.__current_character)

    def print(self, _str: str):
        x, y = self.wherex(), self.wherey()
        for _chr in _str:
            self.gotoxy(x, y)
            self.cputs(_chr)
            x += 1

    def putchxy(self, x: int, y: int, _chr: chr) -> None:
        self.__current_character.code = _chr
        self.__matrix[y][x] = dataclasses.replace(self.__current_character)

    def cputsxy(self, x: int, y: int, _str: str) -> None:
        for _chr in _str:
            self.putchxy(x, y, _chr)
            x += 1
