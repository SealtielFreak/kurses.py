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

RenderMethod = typing.Callable[[sdl2.sdlttf.TTF_Font, chr, sdl2.SDL_Color, sdl2.SDL_Color], typing.Any]


def color_sdl2(color=(0, 0, 0)) -> sdl2.SDL_Color:
    return sdl2.SDL_Color(*color)


def create_texture_chr_sdl2(font: sdl2.sdlttf.TTF_Font, render_method: RenderMethod, renderer: sdl2.SDL_Renderer,
                            _chr: chr, fg=(0, 0, 0), bg=(0, 0, 0), style: int = 0):
    sdl2.sdlttf.TTF_SetFontStyle(font, style)

    _surface = render_method(font, _chr, color_sdl2(fg), color_sdl2(bg))
    _texture = sdl2.SDL_CreateTextureFromSurface(renderer, _surface)

    sdl2.SDL_FreeSurface(_surface)

    return _texture


def get_size_texture_sdl2(texture: sdl2.SDL_Texture):
    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(texture, None, None, ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value


def get_style_sdl2(chr_attr: pyrogue.buffer_term.CharacterAttribute) -> int:
    all_styles = {
        "bold": sdl2.sdlttf.TTF_STYLE_BOLD,
        "italic": sdl2.sdlttf.TTF_STYLE_ITALIC,
        "underline": sdl2.sdlttf.TTF_STYLE_UNDERLINE,
        "strikethrough": sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH,
    }

    style = 0

    for _s in all_styles.keys():
        if getattr(chr_attr, _s):
            style |= all_styles[_s]

    return style


def cast_render_method(_render_method):
    def inner(font, _chr, fg, bg):
        _surface_font = _render_method(font, _chr, fg)

        _surface_bg = sdl2.SDL_CreateRGBSurface(0, _surface_font.contents.w, _surface_font.contents.h, 32, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        _color_bg = sdl2.SDL_MapRGB(_surface_bg.contents.format.contents, bg.r, bg.g, bg.b)
        sdl2.SDL_FillRect(_surface_bg, None, _color_bg)

        sdl2.SDL_BlitSurface(_surface_font, None, _surface_bg, None)

        return _surface_bg

    return inner


def get_render_font_method_sdl2(encoding: pyrogue.virtual_console.EncodingFont, quality: pyrogue.virtual_console.QualityFont) -> RenderMethod:
    _render_f = {
        pyrogue.virtual_console.EncodingFont.ASCII: {
            pyrogue.virtual_console.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderText_Solid),
            pyrogue.virtual_console.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderText_Shaded,
            pyrogue.virtual_console.QualityFont.LCD: sdl2.sdlttf.TTF_RenderText_LCD,
            pyrogue.virtual_console.QualityFont.BLENDED: sdl2.sdlttf.TTF_RenderText_Blended
        },
        pyrogue.virtual_console.EncodingFont.UTF_8: {
            pyrogue.virtual_console.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderUTF8_Solid),
            pyrogue.virtual_console.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderUTF8_Shaded,
            pyrogue.virtual_console.QualityFont.LCD: sdl2.sdlttf.TTF_RenderUTF8_LCD,
            pyrogue.virtual_console.QualityFont.BLENDED: sdl2.sdlttf.TTF_RenderUTF8_Blended
        },
        pyrogue.virtual_console.EncodingFont.UNICODE: {
            pyrogue.virtual_console.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderUNICODE_Solid),
            pyrogue.virtual_console.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderUNICODE_Shaded,
            pyrogue.virtual_console.QualityFont.LCD: sdl2.sdlttf.TTF_RenderUNICODE_LCD,
            pyrogue.virtual_console.QualityFont.BLENDED: sdl2.sdlttf.TTF_RenderUNICODE_Blended
        },
    }[encoding][quality]

    _arg_count = _render_f.__code__.co_argcount

    def render_method(font, _chr, fg, bg):
        _chr = _chr.encode()

        return _render_f(font, _chr, fg, bg)

    return render_method


class SDL2VirtualConsole(pyrogue.virtual_console.VirtualConsole):
    def __init_sdl2(self):
        _type_render = {
            pyrogue.virtual_console.Rendering.HARDWARE: sdl2.SDL_RENDERER_ACCELERATED,
            pyrogue.virtual_console.Rendering.SOFTWARE: sdl2.SDL_RENDERER_SOFTWARE,
        }

        if not sdl2.SDL_WasInit(sdl2.SDL_INIT_EVERYTHING):
            sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        if not sdl2.sdlttf.TTF_WasInit():
            sdl2.sdlttf.TTF_Init()

        self.__c_window = sdl2.SDL_CreateWindow(
            WINDOW_DEFAULT_TITLE.encode(),
            *WINDOW_DEFAULT_POSITION,
            *WINDOW_DEFAULT_SIZE,
            sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE)
        self.__c_renderer = sdl2.SDL_CreateRenderer(self.__c_window, -1, _type_render[self.render])
        self.__c_font = sdl2.sdlttf.TTF_OpenFont(DEFAULT_FONT.encode(), ptsize=DEFAULT_PTSIZE)

    def __del_sdl2(self):
        sdl2.sdlttf.TTF_CloseFont(self.font)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def __init__(self):
        super().__init__()

        self.__init_sdl2()

        render_method = get_render_font_method_sdl2(self.encoding, self.quality_font)
        empty_texture = create_texture_chr_sdl2(self.font, render_method, self.surface, ' ')

        self.__background_color = 0, 0, 0
        self.__buffer = pyrogue.buffer_term.BufferTerm(80, 30)
        self.__target = None
        self.__textures_allocate = {}
        self.__chr_format_key = lambda _str: _str.decode().lower()
        self.__size_texture = get_size_texture_sdl2(empty_texture)

        sdl2.SDL_DestroyTexture(empty_texture)

    def __del__(self):
        self.__del_sdl2()

    @property
    def buffer(self):
        return self.__buffer

    def set_target(self, target):
        self.__target = target

    @property
    def background(self):
        return self.__background_color

    @background.setter
    def background(self, background):
        self.__background_color = background

    def main_loop(self):
        while self.running:
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                self.events(event)

            if self.__target:
                try:
                    self.__target()
                except Exception as e:
                    self.running = False
                    raise e

            if self.surface is not None:
                sdl2.SDL_SetRenderDrawColor(self.surface, *self.background, 255)
                sdl2.SDL_RenderClear(self.surface)

                self.present()

                sdl2.SDL_RenderPresent(self.surface)

        self.clear_cache()

        self.quit()

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

    def events(self, event: sdl2.SDL_Event):
        w, h = self.__size_texture

        if event.type == sdl2.SDL_QUIT:
            self.quit()

        elif event.type == sdl2.SDL_WINDOWEVENT:
            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                width, height = event.window.data1, event.window.data2
                self.__buffer.resize(width // w, height // h)

    def present(self):
        w, h = self.__size_texture
        render_method = get_render_font_method_sdl2(self.encoding, self.quality_font)

        for _obj in self.__buffer:
            x, y = _obj.x, _obj.y

            if isinstance(_obj, pyrogue.buffer_term.CharacterAttribute):
                d_rect = sdl2.SDL_Rect(x * w, y * h, w, h)

                if _obj not in self.__textures_allocate.keys():
                    self.__textures_allocate[_obj] = create_texture_chr_sdl2(
                        self.font, render_method, self.surface, _obj.code,
                        pyrogue.colors.cast_depth_colors(_obj.foreign, self.depth_colors),
                        pyrogue.colors.cast_depth_colors(_obj.background, self.depth_colors),
                        get_style_sdl2(_obj)
                    )

                sdl2.SDL_SetRenderDrawColor(self.surface, *_obj.background, 255)
                sdl2.SDL_RenderCopy(self.surface, self.__textures_allocate[_obj], None, d_rect)
            elif isinstance(_obj, pyrogue.buffer_term.RectangleAttribute):
                d_rect = sdl2.SDL_Rect(x, y, _obj.w * w, _obj.h * h)

                sdl2.SDL_SetRenderDrawColor(self.surface, *_obj.color, 255)
                sdl2.SDL_RenderFillRect(self.surface, d_rect)

    def quit(self):
        self.running = False
