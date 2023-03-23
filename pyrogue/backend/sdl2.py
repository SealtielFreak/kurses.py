import ctypes
import string
import threading
import typing

import sdl2
import sdl2.sdlttf

import pyrogue.buffer_term
import pyrogue.virtual_console
import pyrogue.colors


class SDL2VirtualConsole(pyrogue.virtual_console.VirtualConsole):
    def __init__(self):
        self.__buffer = pyrogue.buffer_term.BufferTerm(80, 30)
        self.__target = None
        self.__running = True

    @property
    def buffer(self) -> pyrogue.buffer_term.BufferTerm:
        return self.__buffer

    def set_target(self, target: typing.Callable[[None], None]):
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

        DEFAULT_BIT_COLORS = pyrogue.colors.get_1bit_colors

        def __main():
            if self.__target is None:
                return

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

                    chr_attr = pyrogue.buffer_term.CharacterAttribute(_chr, foreign=rgb_foreign)

                    if style == sdl2.sdlttf.TTF_STYLE_UNDERLINE:
                        chr_attr = pyrogue.buffer_term.CharacterAttribute(_chr, foreign=rgb_foreign, underline=True)
                    elif style == sdl2.sdlttf.TTF_STYLE_ITALIC:
                        chr_attr = pyrogue.buffer_term.CharacterAttribute(_chr, foreign=rgb_foreign, italic=True)
                    elif style == sdl2.sdlttf.TTF_STYLE_BOLD:
                        chr_attr = pyrogue.buffer_term.CharacterAttribute(_chr, foreign=rgb_foreign, bold=True)
                    elif style == sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH:
                        chr_attr = pyrogue.buffer_term.CharacterAttribute(_chr, foreign=rgb_foreign,
                                                                            strikethrough=True)

                    ascii_texture[chr_attr] = sdl2.SDL_CreateTextureFromSurface(renderer, surface_c)

                    sdl2.SDL_FreeSurface(surface_c)

        w, h = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_QueryTexture(next(iter(ascii_texture.values())), None, None, ctypes.byref(w), ctypes.byref(h))
        w, h = w.value, h.value

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

            __main()

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
