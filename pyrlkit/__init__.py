import abc

import pyrlkit.character_attr
import pyrlkit.style


class Window(abc.ABC):
    @property
    @abc.abstractmethod
    def position(self):
        pass

    @position.setter
    @abc.abstractmethod
    def position(self, value):
        pass

    @property
    @abc.abstractmethod
    def size(self):
        pass

    @size.setter
    @abc.abstractmethod
    def size(self, value):
        pass

    @property
    @abc.abstractmethod
    def title(self):
        pass

    @title.setter
    @abc.abstractmethod
    def title(self, value):
        pass

    @property
    @abc.abstractmethod
    def visible(self):
        pass

    @visible.setter
    @abc.abstractmethod
    def visible(self, value):
        pass

    @abc.abstractmethod
    def set_size(self, width, height):
        pass

    @abc.abstractmethod
    def set_position(self, x, y):
        pass

    @abc.abstractmethod
    def set_title(self, title):
        pass

    @abc.abstractmethod
    def show(self):
        pass

    @abc.abstractmethod
    def hide(self):
        pass

    @abc.abstractmethod
    def minimize(self):
        pass

    @abc.abstractmethod
    def maximize(self):
        pass

    @abc.abstractmethod
    def restore(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def set_transparency(self, alpha):
        pass


import abc
import typing

MatrixCharacterAttribute = typing.List[typing.List[pyrlkit.character_attr.CharacterAttribute]]


def create_matrix(rows: int, cols: int) -> MatrixCharacterAttribute:
    return [[pyrlkit.character_attr.CharacterAttribute() for _ in range(rows)] for _ in range(cols)]


def memset_matrix(a: MatrixCharacterAttribute, b: MatrixCharacterAttribute):
    for y, row in enumerate(a):
        for x, c in enumerate(a):
            try:
                b[y][x] = a[y][x]
            except IndexError:
                pass

    return b


class VirtualMatrixBuffer(abc.ABC):
    U_CHR_MAX = 255
    DEFAULT_TITLE = ""
    DEFAULT_SIZE = 640, 480

    @property
    @abc.abstractmethod
    def queue(self) -> typing.Deque[pyrlkit.character_attr.CharacterAttribute]: ...

    @abc.abstractmethod
    def __iter__(self): ...

    @property
    @abc.abstractmethod
    def buffersize(self): ...

    @abc.abstractmethod
    def getbuffersize(self) -> typing.Tuple[int, int]: ...

    @abc.abstractmethod
    def resize(self, columns: int, rows: int) -> None: ...

    @abc.abstractmethod
    def clreol(self) -> None: ...

    @abc.abstractmethod
    def clrscr(self) -> None: ...

    @abc.abstractmethod
    def delline(self) -> None: ...

    @abc.abstractmethod
    def insline(self) -> None: ...

    @abc.abstractmethod
    def puttext(self, left: int, top: int, right: int, bottom: int, char_info) -> None: ...

    @abc.abstractmethod
    def movetext(self, left: int, top: int, right: int, bottom: int, destleft: int, desttop: int) -> None: ...

    @abc.abstractmethod
    def gotoxy(self, x: int, y: int) -> None: ...

    @abc.abstractmethod
    def print(self, _str: str): ...

    @abc.abstractmethod
    def normvideo(self) -> None: ...

    @abc.abstractmethod
    def textbackground(self, color: int) -> None: ...

    @abc.abstractmethod
    def textcolor(self, color: int) -> None: ...

    @abc.abstractmethod
    def switchbackground(self, color: int) -> None: ...

    @abc.abstractmethod
    def flashbackground(self, color: int, ms: int) -> None: ...

    @abc.abstractmethod
    def bold(self, _bool: bool): ...

    @abc.abstractmethod
    def italic(self, _bool: bool): ...

    @abc.abstractmethod
    def underline(self, _bool: bool): ...

    @abc.abstractmethod
    def cputsxy(self, x: int, y: int, _str: str) -> None: ...

    @abc.abstractmethod
    def putchxy(self, x: int, y: int, _chr: chr) -> None: ...


class MatrixBuffer(VirtualMatrixBuffer):
    pass
