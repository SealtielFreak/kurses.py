import ctypes
import string

import sdl2
import sdl2.sdlttf as sdlttf

DEFAULT_FONT = "ModernDOS8x16.ttf"
DEFAULT_PTSIZE = 16
DEFAULT_ALL_ASCII = string.printable


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
        surface_c = sdlttf.TTF_RenderText_Blended(font, c.encode(), sdl2.SDL_Color())
        ascii_texture[c] = sdl2.SDL_CreateTextureFromSurface(renderer, surface_c)
        sdl2.SDL_FreeSurface(surface_c)

    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(ascii_texture[' '], None, None, ctypes.byref(w), ctypes.byref(h))
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
            sdl2.SDL_RenderCopy(renderer, texture, None, sdl2.SDL_Rect(x * w, y * h, w, h))

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
