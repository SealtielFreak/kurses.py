import typing

import sdl2
import sdl2.sdlgfx as gfx

import kurses.bitmap_surface
import kurses.graphics
from kurses.graphics import CircleFigure, PolygonFigure


class SDL2BitmapSurface(kurses.bitmap_surface.BitmapSurface):
    def __init__(self, size: typing.Tuple[int, int], graphics: kurses.graphics.GraphicsBuffer):
        super().__init__(graphics)

        self.__size = size
        self.__dst_surface = None

    def create(self, surface: sdl2.SDL_Renderer):
        width, height = self.size

        self.destroy()

        self.__dst_surface = sdl2.SDL_CreateTexture(
            surface, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, width, height
        )

        sdl2.SDL_SetTextureBlendMode(self.__dst_surface, sdl2.SDL_BLENDMODE_BLEND)

    def destroy(self):
        if self.current is not None:
            sdl2.SDL_DestroyTexture(self.current)

    def present(self, surface: sdl2.SDL_Renderer) -> sdl2.SDL_Renderer:
        sdl2.SDL_SetRenderTarget(surface, self.current)

        for fig in self.graphics:
            if isinstance(fig, CircleFigure):
                x, y = fig.position

                if fig.filled:
                    gfx.aacircleRGBA(surface, x, y, fig.radius, *fig.color, 255)
                else:
                    gfx.filledCircleRGBA(surface, x, y, fig.radius, *fig.color, 255)
            elif isinstance(fig, PolygonFigure):
                pass

        sdl2.SDL_SetRenderTarget(surface, None)

        return surface

    def clear(self, surface: sdl2.SDL_Renderer) -> None:
        if self.current is not None:
            sdl2.SDL_SetRenderTarget(surface, self.current)
            sdl2.SDL_SetRenderDrawColor(surface, 0, 0, 0, 0)
            sdl2.SDL_RenderClear(surface)

    @property
    def current(self) -> typing.Union[sdl2.SDL_Renderer, None]:
        return self.__dst_surface

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self.__size
