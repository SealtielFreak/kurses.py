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
        pass

    def present(self, surface: sdl2.SDL_Renderer) -> sdl2.SDL_Texture:
        w, h = self.font.size
        cols, rows = self.stream.shape

        if self.current is None:
            self.__dst_texture = sdl2.SDL_CreateTexture(
                surface, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, w * cols, h * rows
            )

        sdl2.SDL_SetRenderTarget(surface, self.current)

        for _data in self.stream:
            if isinstance(_data, kurses.stream.CharacterAttribute):
                x, y = _data.position
                texture = self.font.present_chr(surface, _data)

                sdl2.SDL_RenderCopy(surface, texture, None, sdl2.SDL_Rect(x * w, y * h, w, h))

            elif isinstance(_data, kurses.stream.RectangleAttribute):
                pass

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
