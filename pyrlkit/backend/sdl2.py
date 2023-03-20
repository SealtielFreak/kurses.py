import collections
import ctypes
import string
import threading

import sdl2
import sdl2.sdlttf

import pyrlkit.buffer_matrix
import pyrlkit.virtual_console


def get_true_colors():
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                yield r, g, b


def get_8bit_colors():
    for r in range(0, 256, 36):
        for g in range(0, 256, 36):
            for b in range(0, 256, 85):
                yield r, g, b


def get_2bit_colors():
    for r in (0, 85, 170, 255):
        for g in (0, 85, 170, 255):
            for b in (0, 85, 170, 255):
                yield r, g, b


def get_1bit_colors():
    for r in range(0, 256, 255):
        for g in range(0, 256, 255):
            for b in range(0, 256, 255):
                yield r, g, b


class SDL2VirtualConsole(pyrlkit.virtual_console.VirtualConsole):
    def __init__(self):
        self.__buffer = pyrlkit.buffer_matrix.BufferMatrix(80, 30)
        self.__target = None
        self.__running = True

    @property
    def buffer(self) -> pyrlkit.buffer_matrix.BufferMatrix:
        return self.__buffer

    def set_target(self, target):
        self.__target = target

    def main_loop(self):
        DEFAULT_FONT = "ModernDOS8x16.ttf"
        DEFAULT_PTSIZE = 16
        DEFAULT_ALL_ASCII = string.printable
        DEFAULT_ALL_STYLES = (
            sdl2.sdlttf.TTF_STYLE_NORMAL,
            sdl2.sdlttf.TTF_STYLE_ITALIC,
            sdl2.sdlttf.TTF_STYLE_BOLD,
            sdl2.sdlttf.TTF_STYLE_UNDERLINE,
            sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH
        )

        WINDOW_DEFAULT_TITLE = "SDL2"
        WINDOW_DEFAULT_POSITION = sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED
        WINDOW_DEFAULT_SIZE = 640, 480

        DEFAULT_BIT_COLORS = get_1bit_colors

        def __main():
            try:
                self.__target()
            except Exception as e:
                self.__running = False
                raise e

        if sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING):
            return

        window = sdl2.SDL_CreateWindow(
            WINDOW_DEFAULT_TITLE.encode(),
            *WINDOW_DEFAULT_POSITION,
            *WINDOW_DEFAULT_SIZE,
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE
        )
        renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

        sdl2.sdlttf.TTF_Init()

        font = sdl2.sdlttf.TTF_OpenFont(DEFAULT_FONT.encode(), ptsize=DEFAULT_PTSIZE)
        if font is None:
            return

        ascii_texture = {}

        for _chr in DEFAULT_ALL_ASCII:
            for rgb_foreign in DEFAULT_BIT_COLORS():
                for style in DEFAULT_ALL_STYLES:
                    sdl2.sdlttf.TTF_SetFontStyle(font, style)
                    surface_c = sdl2.sdlttf.TTF_RenderText_Blended(font, _chr.encode(), sdl2.SDL_Color(*rgb_foreign))

                    chr_attr = pyrlkit.buffer_matrix.CharacterAttribute(_chr, foreign=rgb_foreign)

                    if style == sdl2.sdlttf.TTF_STYLE_UNDERLINE:
                        chr_attr = pyrlkit.buffer_matrix.CharacterAttribute(_chr, foreign=rgb_foreign, underline=True)
                    elif style == sdl2.sdlttf.TTF_STYLE_ITALIC:
                        chr_attr = pyrlkit.buffer_matrix.CharacterAttribute(_chr, foreign=rgb_foreign, italic=True)
                    elif style == sdl2.sdlttf.TTF_STYLE_BOLD:
                        chr_attr = pyrlkit.buffer_matrix.CharacterAttribute(_chr, foreign=rgb_foreign, bold=True)

                    ascii_texture[chr_attr] = sdl2.SDL_CreateTextureFromSurface(renderer, surface_c)

                    sdl2.SDL_FreeSurface(surface_c)

        w, h = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_QueryTexture(next(iter(ascii_texture.values())), None, None, ctypes.byref(w), ctypes.byref(h))
        w, h = w.value, h.value

        thread = threading.Thread(target=__main)
        thread.daemon = True
        thread.start()

        while self.__running:
            events = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(ctypes.byref(events)) != 0:
                if events.type == sdl2.SDL_QUIT:
                    self.__running = False

                elif events.type == sdl2.SDL_WINDOWEVENT:
                    if events.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                        width, height = events.window.data1, events.window.data2
                        self.__buffer.resize(width // w, height // h)

            sdl2.SDL_RenderClear(renderer)

            chr_queue = self.__buffer.queue

            while len(chr_queue) != 0:
                _chr = chr_queue.pop()
                x, y = _chr.x, _chr.y
                dest = sdl2.SDL_Rect(x * w, y * h, w, h)

                sdl2.SDL_SetRenderDrawColor(renderer, *_chr.background, 255)
                sdl2.SDL_RenderFillRect(renderer, dest)
                sdl2.SDL_RenderCopy(renderer, ascii_texture[_chr], None, dest)

            sdl2.SDL_RenderPresent(renderer)

        [sdl2.SDL_DestroyTexture(texture) for texture in ascii_texture.values()]
        ascii_texture.clear()

        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()

    def set_title(self, _str: str):
        pass
