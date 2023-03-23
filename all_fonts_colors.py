import ctypes
import string

import sdl2
import sdl2.sdlttf as sdlttf

from pyrogue.character_attr import CharacterAttribute

DEFAULT_FONT = "ModernDOS8x16.ttf"
DEFAULT_PTSIZE = 16
DEFAULT_ALL_ASCII = string.printable


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


def rgb_to_hex(rgb):
    return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]


DEFAULT_BIT_COLORS = get_1bit_colors


def main():
    WINDOW_DEFAULT_TITLE = "SDL2"
    WINDOW_DEFAULT_POSITION = sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED
    WINDOW_DEFAULT_SIZE = 640, 480

    if sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING):
        return

    running = True
    window = sdl2.SDL_CreateWindow(
        WINDOW_DEFAULT_TITLE.encode(),
        *WINDOW_DEFAULT_POSITION,
        *WINDOW_DEFAULT_SIZE,
        sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE
    )
    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

    sdlttf.TTF_Init()

    font = sdlttf.TTF_OpenFont(DEFAULT_FONT.encode(), ptsize=DEFAULT_PTSIZE)
    if font is None:
        return

    ascii_texture = {}

    for c in DEFAULT_ALL_ASCII:
        for rgb_foreign in DEFAULT_BIT_COLORS():
            surface_c = sdlttf.TTF_RenderText_Blended(font, c.encode(), sdl2.SDL_Color(*rgb_foreign))
            ascii_texture[
                CharacterAttribute(c, rgb_to_hex(rgb_foreign))
            ] = sdl2.SDL_CreateTextureFromSurface(renderer, surface_c)
            sdl2.SDL_FreeSurface(surface_c)

    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(next(iter(ascii_texture.values())), None, None, ctypes.byref(w), ctypes.byref(h))
    w, h = w.value, h.value

    while running:
        events = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(events)) != 0:
            if events.type == sdl2.SDL_QUIT:
                running = False

        sdl2.SDL_RenderClear(renderer)

        window_width, window_height = ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GetWindowSize(window, ctypes.byref(window_width), ctypes.byref(window_height))
        window_width, window_height = window_width.value, window_height.value

        x, y = 0, 0
        for texture in ascii_texture.values():
            for rgb in DEFAULT_BIT_COLORS():
                dest = sdl2.SDL_Rect(x * w, y * h, w, h)
                sdl2.SDL_SetRenderDrawColor(renderer, *rgb, 255)
                sdl2.SDL_RenderFillRect(renderer, dest)
                sdl2.SDL_RenderCopy(renderer, texture, None, dest)

                x += 1

                if x * w > window_width:
                    y += 1
                    x = 0

        sdl2.SDL_RenderPresent(renderer)

    [sdl2.SDL_DestroyTexture(texture) for texture in ascii_texture.values()]
    ascii_texture.clear()

    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()


if __name__ == '__main__':
    main()
