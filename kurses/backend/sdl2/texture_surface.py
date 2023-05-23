import typing

import sdl2

import kurses.font_resources
import kurses.texture_surface
import kurses.stream


class SDL2TextureSurface(kurses.texture_surface.TextureSurface):
    def __init__(self, font: kurses.font_resources.FontResources, stream: kurses.stream.StreamBuffer):
        super().__init__(font, stream)

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

        for _data in self.stream:
            x, y = _data.position
            if isinstance(_data, kurses.stream.CharacterAttribute):
                texture = self.font.present_chr(surface, _data)

                sdl2.SDL_RenderCopy(surface, texture, None, sdl2.SDL_Rect(x * w, y * h, w, h))

            elif isinstance(_data, kurses.stream.RectangleAttribute):
                d_rect = sdl2.SDL_Rect(x, y, _data.w * w, _data.h * h)

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
