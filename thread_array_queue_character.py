import collections
import ctypes
import string
import threading
import time

import sdl2
import sdl2.sdlttf as sdlttf

from pyrlkit.character_value import CharacterValue

DEFAULT_SHAPE = [80, 30]

DEFAULT_FONT = "ModernDOS8x16.ttf"
DEFAULT_PTSIZE = 16
DEFAULT_ALL_ASCII = string.printable
DEFAULT_ALL_STYLES = (
    sdlttf.TTF_STYLE_NORMAL,
    sdlttf.TTF_STYLE_ITALIC,
    sdlttf.TTF_STYLE_BOLD,
    sdlttf.TTF_STYLE_UNDERLINE,
    sdlttf.TTF_STYLE_STRIKETHROUGH
)


def get_true_colors():
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                yield r, g, b


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


def hex_to_rgb(hex_color):
    hex_str = hex(hex_color)[2:]

    hex_str = hex_str.rjust(6, '0')

    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)

    return r, g, b


def create_shape(shape):
    rows, cols = shape
    return [[CharacterValue() for _ in range(rows)] for _ in range(cols)]


chr_matrix = create_shape(DEFAULT_SHAPE)


def resize(row, col):
    global chr_matrix
    DEFAULT_SHAPE[0] = row
    DEFAULT_SHAPE[1] = col
    chr_matrix = create_shape((row, col))


def clrs():
    global chr_matrix
    chr_matrix = create_shape(DEFAULT_SHAPE)


def putchxy(x: int, y: int, c: chr):
    global chr_matrix

    try:
        chr_matrix[y][x] = CharacterValue(code=c, x=x, y=y)
    except IndexError:
        pass


def cputsxy(x: int, y: int, _str: str) -> None:
    for c in _str:
        putchxy(x, y, c)
        x += 1


DEFAULT_BIT_COLORS = get_1bit_colors


def main_loop(target):
    global chr_matrix

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

    for _chr in DEFAULT_ALL_ASCII:
        for rgb_foreign in DEFAULT_BIT_COLORS():
            for style in DEFAULT_ALL_STYLES:
                sdlttf.TTF_SetFontStyle(font, style)
                surface_c = sdlttf.TTF_RenderText_Blended(font, _chr.encode(), sdl2.SDL_Color(*rgb_foreign))
                ascii_texture[
                    CharacterValue(_chr, rgb_to_hex(rgb_foreign), style=style)
                ] = sdl2.SDL_CreateTextureFromSurface(renderer, surface_c)
                sdl2.SDL_FreeSurface(surface_c)

    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(next(iter(ascii_texture.values())), None, None, ctypes.byref(w), ctypes.byref(h))
    w, h = w.value, h.value

    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

    while running:
        events = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(events)) != 0:
            if events.type == sdl2.SDL_QUIT:
                running = False

            elif events.type == sdl2.SDL_WINDOWEVENT:
                if events.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    width, height = events.window.data1, events.window.data2
                    resize(width // w, height // h)
                    print(len(chr_matrix), len(chr_matrix[0]))

        sdl2.SDL_RenderClear(renderer)

        chr_queue = collections.deque()
        for row in chr_matrix:
            for _chr in row:
                if _chr.code == '':
                    continue

                chr_queue.append(_chr)

        while len(chr_queue) != 0:
            _chr = chr_queue.pop()
            x, y = _chr.x, _chr.y
            dest = sdl2.SDL_Rect(x * w, y * h, w, h)

            sdl2.SDL_SetRenderDrawColor(renderer, *hex_to_rgb(_chr.bg), 255)
            sdl2.SDL_RenderFillRect(renderer, dest)
            sdl2.SDL_RenderCopy(renderer, ascii_texture[_chr], None, dest)

        sdl2.SDL_RenderPresent(renderer)


    [sdl2.SDL_DestroyTexture(texture) for texture in ascii_texture.values()]
    ascii_texture.clear()

    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()


if __name__ == '__main__':

    def main():
        x, y = 0, 0

        while True:
            clrs()
            cputsxy(x, y, "Hello world")
            time.sleep(0.25)
            x += 1
            y += 1


    main_loop(target=main)
