import sdl2

import pyrlkit.virtual_console
import pyrlkit.buffer_matrix


class SDL2VirtualConsole(pyrlkit.virtual_console.VirtualConsole):
    def __init__(self):
        self.__buffer = pyrlkit.buffer_matrix.BufferMatrix(80, 30)

    @property
    def buffer(self) -> pyrlkit.buffer_matrix.BufferMatrix:
        return self.__buffer

    def set_target(self, target):
        pass

    def main_loop(self):
        sdl2.SDL_Init(0)

    def set_title(self, _str: str):
        pass
