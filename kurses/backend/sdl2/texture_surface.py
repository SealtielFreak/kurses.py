import sdl2


import kurses.buffer
import kurses.font_resources
import kurses.texture_surface


class SDL2TextureSurface(kurses.texture_surface.TextureSurface):
    def __init__(self, renderer: sdl2.SDL_Renderer, font: kurses.font_resources.FontResources, buffer: kurses.buffer.VirtualBuffer):
        super().__init__(renderer, font, buffer)

    def present(self):
        pass
    