import abc

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


class VirtualMatrixBuffer(abc.ABC):
    @abc.abstractmethod
    def getkey(self):
        pass

    @property
    @abc.abstractmethod
    def keys_pressed(self):
        pass

    @property
    @abc.abstractmethod
    def keys_released(self):
        pass

    @abc.abstractmethod
    def resize(self, shape):
        pass

    @abc.abstractmethod
    def gotoxy(self, x: int, y: int):
        pass

    @abc.abstractmethod
    def clrscr(self):
        pass

    @abc.abstractmethod
    def textcolor(self, color):
        pass

    @abc.abstractmethod
    def textbackground(self, color):
        pass

    @abc.abstractmethod
    def cprintf(self, fmt: str, *args):
        pass

    @abc.abstractmethod
    def putch(self, _chr: chr):
        pass

    @abc.abstractmethod
    def cputsxy(self, x: int, y: int, _chr: chr):
        pass

    @abc.abstractmethod
    def cputsxy(self, x: int, y: int, _str: str):
        pass

    @abc.abstractmethod
    def get_console_size(self):
        pass

    @abc.abstractmethod
    def set_font_style(self, style: pyrlkit.style.FontStyle):
        pass

    @abc.abstractmethod
    def set_font_color(self, color):
        pass

    @abc.abstractmethod
    def set_background_color(self, color):
        pass


class MatrixBuffer(VirtualMatrixBuffer):
    pass
