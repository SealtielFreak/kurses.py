import collections
import ctypes
import functools
import time
import typing

import sdl2
import sdl2.sdlttf

import kurses.term
import kurses.stream
import kurses.colors
import kurses.backend.sdl2.font_resources
import kurses.backend.sdl2.texture_surface

DEFAULT_WINDOW_POSITION = sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED


class SDL2VirtualTerminal(kurses.term.VirtualTerminal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if sdl2.SDL_WasInit(sdl2.SDL_INIT_EVERYTHING) == 0:
            sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        if sdl2.sdlttf.TTF_WasInit() == 0:
            sdl2.sdlttf.TTF_Init()

        width, height = self.size
        self.__c_window = sdl2.SDL_CreateWindow(
            kwargs.get("title", "Virtual terminal").encode(),
            sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED,
            width, height,
            sdl2.SDL_WINDOW_SHOWN
        )

        self.__c_renderer = sdl2.SDL_CreateRenderer(
            self.window,
            -1,
            [sdl2.SDL_RENDERER_ACCELERATED, sdl2.SDL_RENDERER_SOFTWARE][self.type_rendering.value]
        )

        self.__target = None
        self.__font = kurses.backend.FontResources(self._font_filename)
        self.__textures = kurses.backend.TextureSurface(self.__font, self.stream)

    def __del__(self):
        sdl2.SDL_DestroyRenderer(self.surface)
        sdl2.SDL_DestroyWindow(self.window)

    @property
    def title(self):
        return sdl2.SDL_GetWindowTitle(self.window)

    @title.setter
    def title(self, _str: str):
        sdl2.SDL_SetWindowTitle(self.window, _str.encode())

    def set_target(self, target: typing.Callable[[None], None]):
        self.__target = target

    def main_loop(self):
        while self.running:
            event = sdl2.SDL_Event()

            while sdl2.SDL_PollEvent(ctypes.byref(event)):
                if event.type == sdl2.SDL_QUIT:
                    self.quit()

                self.push_events(event)

            if self.__target:
                self.__target()

            self.__textures.present(self.surface)

            sdl2.SDL_RenderClear(self.surface)
            sdl2.SDL_RenderCopy(self.surface, self.__textures.current, None, None)
            sdl2.SDL_RenderPresent(self.surface)

    def keyspressed(self) -> typing.List[str]:
        pass

    @property
    def window(self) -> sdl2.SDL_Window:
        return self.__c_window

    @property
    def surface(self) -> sdl2.SDL_Renderer:
        return self.__c_renderer

    def push_events(self, event: sdl2.SDL_Event):
        pass

    def present(self):
        pass

    def quit(self):
        self.running = False
