import typing

import sdl2
import sdl2.sdlgfx as gfx

import kurses.graphics
import kurses.surface.bitmap
from kurses.graphics import CircleFigure, PolygonFigure
from kurses.graphics.primitive import LineFigure, RectangleFigure


class SDL2BitmapSurface(kurses.surface.bitmap.BitmapSurface):
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

        def _draw_line(line):
            x1, y1 = line.start
            x2, y2 = line.end

            gfx.thickLineRGBA(surface, x1, y1, x2, y2, line.thickness, *line.color, 255)

        def _draw_rectangle(rect):
            x, y = rect.position
            w, h = rect.size

            if rect.filled:
                gfx.boxRGBA(surface, x, y, x + w, y + h, *rect.color, 255)
            else:
                gfx.rectangleRGBA(surface, x, y, x + w, y + h, *rect.color, 255)

        def _draw_circle(circle):
            x, y = circle.position

            if circle.filled:
                gfx.filledCircleRGBA(surface, x, y, circle.radius, *circle.color, 255)
            else:
                gfx.aacircleRGBA(surface, x, y, circle.radius, *circle.color, 255)

        def _draw_polygon(poly):
            vx, vy = poly.points
            length = poly.length

            vx = (sdl2.Sint16 * length)(*vx)
            vy = (sdl2.Sint16 * length)(*vy)

            if poly.filled:
                gfx.filledPolygonRGBA(surface, vx, vy, length, *poly.color, 255)
            else:
                gfx.aapolygonRGBA(surface, vx, vy, length, *poly.color, 255)

        all_draw_method = {
            LineFigure: _draw_line,
            RectangleFigure: _draw_rectangle,
            CircleFigure: _draw_circle,
            PolygonFigure: _draw_polygon,
        }

        for fig in self.graphics:
            draw = all_draw_method.get(type(fig), None)

            if draw is not None:
                draw(fig)

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

    def resize(self, width: int, height: int):
        self.__size = width, height
