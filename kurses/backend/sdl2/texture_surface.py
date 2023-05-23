import typing

import sdl2

import kurses.font_resources
import kurses.texture_surface
import kurses.stream


class SDL2TextureSurface(kurses.texture_surface.TextureSurface):
    def __init__(self, surface: sdl2.SDL_Renderer, font: kurses.font_resources.FontResources, stream: kurses.stream.StreamBuffer):
        super().__init__(surface, font, stream)

        w, h = self.size
        self.__dst_texture = sdl2.SDL_CreateTexture(
            self.surface, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, w, h
        )

    def __del__(self):
        sdl2.SDL_DestroyTexture(self.current)

    def present(self) -> sdl2.SDL_Texture:
        sdl2.SDL_SetRenderTarget(self.surface, self.current)
        w, h = self.font.size

        for _data in self.stream:
            if isinstance(_data, kurses.stream.CharacterAttribute):
                x, y = _data.position
                texture = self.font.present_chr(self.surface, _data)

                sdl2.SDL_RenderCopy(self.surface, texture, None, sdl2.SDL_Rect(x * w, y * h, w, h))

            elif isinstance(_data, kurses.stream.RectangleAttribute):
                pass

        sdl2.SDL_SetRenderTarget(self.surface, None)

        return self.current

    def clear(self) -> None:
        sdl2.SDL_SetRenderTarget(self.surface, self.current)
        sdl2.SDL_SetRenderDrawColor(self.surface, 0, 0, 0, 0)
        sdl2.SDL_RenderClear(self.surface)

    @property
    def current(self) -> sdl2.SDL_Texture:
        return self.__dst_texture

    @property
    def size(self):
        cols, rows = self.stream.shape
        w, h = self.font.size

        return w * rows, h * cols
