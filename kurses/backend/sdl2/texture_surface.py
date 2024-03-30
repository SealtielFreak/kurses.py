import typing

import sdl2

import kurses.font_resources
import kurses.texture_surface
import kurses.stream


class SDL2TextureSurface(kurses.texture_surface.TextureSurface):
    def __init__(self, font: kurses.font_resources.FontResources, streams: list[kurses.stream.StreamBuffer]):
        super().__init__(font, streams)

        self.__dst_texture = None

    def __del__(self):
        if self.current is not None:
            sdl2.SDL_DestroyTexture(self.current)

    def present(self, surface: sdl2.SDL_Renderer) -> sdl2.SDL_Texture:
        w, h = self.font.size
        cols, rows = self.stream.shape

        if self.current is None:
            self.__dst_texture = sdl2.SDL_CreateTexture(
                surface, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, w * cols, h * rows
            )

        sdl2.SDL_SetRenderTarget(surface, self.current)

        for stream in self.streams:
            cols, rows = stream.shape
            sx, sy = stream.sx, stream.sy

            for _data in stream:
                x, y = _data.position

                while x > cols:
                    x = x - (cols + 1)
                    y += 1

                if isinstance(_data, kurses.stream.CharacterAttribute):
                    texture = self.font.present_chr(surface, _data)

                    d_rect = sdl2.SDL_Rect(x * (w * sx), y * (h * sy), w * sx, h * sy)
                    sdl2.SDL_RenderCopy(surface, texture, None, d_rect)

                elif isinstance(_data, kurses.stream.RectangleAttribute):
                    d_rect = sdl2.SDL_Rect(x, y, (_data.w * w) * sx, (_data.h * h) * sy)

                    sdl2.SDL_SetRenderDrawColor(surface, *_data.color, 255)
                    sdl2.SDL_RenderFillRect(surface, d_rect)

        sdl2.SDL_SetRenderTarget(surface, None)

        return self.current

    def clear(self, surface: sdl2.SDL_Renderer) -> None:
        if self.current is not None:
            sdl2.SDL_SetRenderTarget(surface, self.current)
            sdl2.SDL_SetRenderDrawColor(surface, 0, 0, 0, 0)
            sdl2.SDL_RenderClear(surface)

    @property
    def current(self) -> typing.Union[sdl2.SDL_Texture, None]:
        return self.__dst_texture

    @property
    def size(self):
        cols, rows = self.stream.shape
        w, h = self.font.size

        return w * rows, h * cols
