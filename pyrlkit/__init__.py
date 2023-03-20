import abc


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


class VirtualTerminal(abc.ABC):
    @abc.abstractmethod
    def getkey(self):
        pass

    @abc.abstractmethod
    def gotoxy(self, x, y):
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
    def cprintf(self, fmt, *args):
        pass

    @abc.abstractmethod
    def putch(self, char):
        pass

    @abc.abstractmethod
    def get_console_size(self):
        pass

    @abc.abstractmethod
    def set_font_style(self, style):
        pass

    @abc.abstractmethod
    def set_font_color(self, color):
        pass

    @abc.abstractmethod
    def set_background_color(self, color):
        pass

    @abc.abstractmethod
    def enable_echo(self):
        pass

    @abc.abstractmethod
    def disable_echo(self):
        pass

    @abc.abstractmethod
    def set_cursor_visibility(self, visibility):
        pass

    @abc.abstractmethod
    def set_cursor_shape(self, shape):
        pass

    @abc.abstractmethod
    def enable_scroll(self):
        pass

    @abc.abstractmethod
    def disable_scroll(self):
        pass

    @abc.abstractmethod
    def set_title(self, title):
        pass

    @abc.abstractmethod
    def set_icon(self, icon_path):
        pass

    @abc.abstractmethod
    def set_window_size(self, width, height):
        pass

    @abc.abstractmethod
    def set_window_position(self, x, y):
        pass

    @abc.abstractmethod
    def enable_mouse_input(self):
        pass

    @abc.abstractmethod
    def disable_mouse_input(self):
        pass

    @abc.abstractmethod
    def enable_alt_buffer(self):
        pass

    @abc.abstractmethod
    def disable_alt_buffer(self):
        pass


class Terminal(VirtualTerminal):
    pass
