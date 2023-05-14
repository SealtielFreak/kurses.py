import collections
import ctypes
import string
import typing

import sdl2
import sdl2.sdlttf

import pyrogue.buffer_term
import pyrogue.colors
import pyrogue.virtual_console

DEFAULT_FONT = "ModernDOS8x16.ttf"
DEFAULT_PTSIZE = 16
DEFAULT_ALL_ASCII = string.printable
DEFAULT_ALL_STYLES = (
    sdl2.sdlttf.TTF_STYLE_NORMAL,
    sdl2.sdlttf.TTF_STYLE_ITALIC,
    sdl2.sdlttf.TTF_STYLE_BOLD,
    sdl2.sdlttf.TTF_STYLE_UNDERLINE,
    sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH
)

WINDOW_DEFAULT_TITLE = "SDL2"
WINDOW_DEFAULT_POSITION = sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED
WINDOW_DEFAULT_SIZE = 640, 480


def create_texture_chr(font: sdl2.sdlttf.TTF_Font, renderer: sdl2.SDL_Renderer, _chr: chr, foreign_color=(0, 0, 0),
                       style: int = 0):
    sdl2.sdlttf.TTF_SetFontStyle(font, style)

    chr_surface = sdl2.sdlttf.TTF_RenderText_Blended(font, _chr.encode(), sdl2.SDL_Color(*foreign_color))
    chr_texture = sdl2.SDL_CreateTextureFromSurface(renderer, chr_surface)

    sdl2.SDL_FreeSurface(chr_surface)

    return chr_texture


def get_size_texture(texture: sdl2.SDL_Texture):
    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(texture, None, None, ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value


def get_style(chr_attr: pyrogue.buffer_term.CharacterAttribute) -> int:
    style = 0

    if chr_attr.bold:
        style |= sdl2.sdlttf.TTF_STYLE_BOLD

    if chr_attr.italic:
        style |= sdl2.sdlttf.TTF_STYLE_ITALIC

    if chr_attr.underline:
        style |= sdl2.sdlttf.TTF_STYLE_UNDERLINE

    if chr_attr.strikethrough:
        style |= sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH

    return style


class SDL2VirtualConsole(pyrogue.virtual_console.VirtualConsole):
    def __instance_all_service(self):
        if not sdl2.SDL_WasInit(sdl2.SDL_INIT_EVERYTHING):
            sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        if not sdl2.sdlttf.TTF_WasInit():
            sdl2.sdlttf.TTF_Init()

        self.__c_window = sdl2.SDL_CreateWindow(
            WINDOW_DEFAULT_TITLE.encode(),
            *WINDOW_DEFAULT_POSITION,
            *WINDOW_DEFAULT_SIZE,
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE
        )
        self.__c_renderer = sdl2.SDL_CreateRenderer(self.__c_window, -1, sdl2.SDL_RENDERER_ACCELERATED)
        self.__c_font = sdl2.sdlttf.TTF_OpenFont(DEFAULT_FONT.encode(), ptsize=DEFAULT_PTSIZE)

    def __init__(self):
        self.__instance_all_service()

        empty_texture = create_texture_chr(self.font, self.surface, ' ')

        self.__buffer = pyrogue.buffer_term.BufferTerm(80, 30)
        self.__target = None
        self.__running = True
        self.__textures_allocate = {}
        self.__chr_format_key = lambda _str: _str.decode().lower()
        self.__size_texture = get_size_texture(empty_texture)

        sdl2.SDL_DestroyTexture(empty_texture)

    def __del__(self):
        self.quit()

    @property
    def buffer(self) -> pyrogue.buffer_term.BufferTerm:
        return self.__buffer

    def set_target(self, target: typing.Callable[[None], None]):
        self.__target = target

    def main_loop(self):

        while self.__running:
            self.events()

            if self.__target:
                try:
                    self.__target()
                except Exception as e:
                    self.__running = False
                    raise e

            sdl2.SDL_SetRenderDrawColor(self.surface, 0, 0, 0, 255)
            sdl2.SDL_RenderClear(self.surface)

            self.draw()

            sdl2.SDL_RenderPresent(self.surface)

        self.clear_cache()

        sdl2.sdlttf.TTF_CloseFont(self.font)
        sdl2.SDL_DestroyWindow(self.__c_window)
        sdl2.SDL_Quit()

    def set_title(self, _str: str):
        sdl2.SDL_SetWindowTitle(self.__c_window, _str.encode())

    def keyspressed(self):
        pressed_keys = collections.deque()

        keyboard_state = sdl2.SDL_GetKeyboardState(None)

        for key_code in range(sdl2.SDL_NUM_SCANCODES):
            if keyboard_state[key_code] == 1:
                pressed_keys.append(self.__chr_format_key(sdl2.SDL_GetScancodeName(key_code)))

        return pressed_keys

    @property
    def window(self) -> sdl2.SDL_Window:
        return self.__c_window

    @property
    def surface(self) -> sdl2.SDL_Renderer:
        return self.__c_renderer

    @property
    def font(self) -> sdl2.sdlttf.TTF_Font:
        return self.__c_font

    def clear_cache(self):
        if len(self.__textures_allocate) != 0:
            [sdl2.SDL_DestroyTexture(texture) for texture in self.__textures_allocate.values()]

        self.__textures_allocate.clear()

    def draw(self):
        w, h = self.__size_texture

        for chr_attr in self.__buffer:
            x, y = chr_attr.x, chr_attr.y
            d_rect = sdl2.SDL_Rect(x * w, y * h, w, h)

            if chr_attr not in self.__textures_allocate.keys():
                self.__textures_allocate[chr_attr] = create_texture_chr(
                    self.font, self.surface, chr_attr.code, chr_attr.foreign, get_style(chr_attr)
                )

            sdl2.SDL_SetRenderDrawColor(self.surface, *chr_attr.background, 255)
            sdl2.SDL_RenderFillRect(self.surface, d_rect)
            sdl2.SDL_RenderCopy(self.surface, self.__textures_allocate[chr_attr], None, d_rect)

    def events(self):
        events = sdl2.SDL_Event()
        w, h = self.__size_texture

        while sdl2.SDL_PollEvent(ctypes.byref(events)) != 0:
            if events.type == sdl2.SDL_QUIT:
                self.__running = False

            elif events.type == sdl2.SDL_WINDOWEVENT:
                if events.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    width, height = events.window.data1, events.window.data2
                    self.__buffer.resize(width // w, height // h)

    def quit(self):
        sdl2.sdlttf.TTF_CloseFont(self.font)
        sdl2.SDL_DestroyWindow(self.__c_window)
        sdl2.SDL_Quit()
