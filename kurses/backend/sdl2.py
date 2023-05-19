import collections
import ctypes
import functools
import typing
import time

import sdl2
import sdl2.sdlttf

import kurses.buffer
import kurses.colors
import kurses.virtual_console


DEFAULT_WINDOW_POSITION = sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED
DEFAULT_WINDOW_SIZE = 640, 480

RenderMethodSDL2 = typing.Callable[[sdl2.sdlttf.TTF_Font, str, sdl2.SDL_Color, sdl2.SDL_Color], typing.Any]


def color_sdl2(color=(0, 0, 0)) -> sdl2.SDL_Color:
    return sdl2.SDL_Color(*color)


def create_texture_chr_sdl2(font: sdl2.sdlttf.TTF_Font, render_method: RenderMethodSDL2, renderer: sdl2.SDL_Renderer,
                            _chr: str, fg=(0, 0, 0), bg=(0, 0, 0), style: int = 0):
    sdl2.sdlttf.TTF_SetFontStyle(font, style)

    _surface = render_method(font, _chr, color_sdl2(fg), color_sdl2(bg))
    _texture = sdl2.SDL_CreateTextureFromSurface(renderer, _surface)

    sdl2.SDL_FreeSurface(_surface)

    return _texture


def get_size_texture_sdl2(texture: sdl2.SDL_Texture):
    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(texture, None, None, ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value


def get_style_sdl2(chr_attr: kurses.buffer.CharacterAttribute) -> int:
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
        r, g, b, a = 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000
        _surface_font = _render_method(font, _chr, fg)

        _surface = sdl2.SDL_CreateRGBSurface(
            0, _surface_font.contents.w, _surface_font.contents.h, 32, r, g, b, a)
        _color_bg = sdl2.SDL_MapRGB(_surface.contents.format.contents, bg.r, bg.g, bg.b)
        sdl2.SDL_FillRect(_surface, None, _color_bg)

        sdl2.SDL_BlitSurface(_surface_font, None, _surface, None)

        return _surface

    return inner


def get_render_font_method_sdl2(encoding: kurses.virtual_console.EncodingFont, quality: kurses.virtual_console.QualityFont) -> RenderMethodSDL2:
    _render_f = {
        kurses.virtual_console.EncodingFont.ASCII: {
            kurses.virtual_console.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderText_Solid),
            kurses.virtual_console.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderText_Shaded,
            kurses.virtual_console.QualityFont.LCD: sdl2.sdlttf.TTF_RenderText_LCD,
            kurses.virtual_console.QualityFont.BLENDED: cast_render_method(sdl2.sdlttf.TTF_RenderText_Blended)
        },
        kurses.virtual_console.EncodingFont.UTF_8: {
            kurses.virtual_console.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderUTF8_Solid),
            kurses.virtual_console.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderUTF8_Shaded,
            kurses.virtual_console.QualityFont.LCD: sdl2.sdlttf.TTF_RenderUTF8_LCD,
            kurses.virtual_console.QualityFont.BLENDED: cast_render_method(sdl2.sdlttf.TTF_RenderUTF8_Blended)
        },
        kurses.virtual_console.EncodingFont.UNICODE: {
            kurses.virtual_console.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderUNICODE_Solid),
            kurses.virtual_console.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderUNICODE_Shaded,
            kurses.virtual_console.QualityFont.LCD: sdl2.sdlttf.TTF_RenderUNICODE_LCD,
            kurses.virtual_console.QualityFont.BLENDED: cast_render_method(sdl2.sdlttf.TTF_RenderUNICODE_Blended)
        },
    }[encoding][quality]

    def render_method(font, _chr, fg, bg):
        _chr = _chr.encode()

        return _render_f(font, _chr, fg, bg)

    return render_method


def get_cursor(_type: kurses.virtual_console.TypeCursor):
    _cursor = {
        kurses.virtual_console.TypeCursor.LINE: lambda x, y, w, h: sdl2.SDL_Rect(x, y + ((h // 4) * 3), w, (h // 4)),
        kurses.virtual_console.TypeCursor.RECT: lambda x, y, w, h: sdl2.SDL_Rect(x, y, w, h),
        kurses.virtual_console.TypeCursor.SOLID_RECT: lambda x, y, w, h: sdl2.SDL_Rect(x, y, w, h),
        kurses.virtual_console.TypeCursor.VERTICAL: lambda x, y, w, h: sdl2.SDL_Rect(x, y, w // 6, h),
        kurses.virtual_console.TypeCursor.UNDERSCORE: lambda x, y, w, h: sdl2.SDL_Rect(x, y + ((h // 8) * 7), w, (h // 8)),
    }

    return _cursor[_type]


class SDL2VirtualConsole(kurses.virtual_console.VirtualConsole):
    def __init_sdl2(self):
        _type_render = {
            kurses.virtual_console.Rendering.HARDWARE: sdl2.SDL_RENDERER_ACCELERATED,
            kurses.virtual_console.Rendering.SOFTWARE: sdl2.SDL_RENDERER_SOFTWARE,
        }

        if not sdl2.SDL_WasInit(sdl2.SDL_INIT_EVERYTHING):
            sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

        if not sdl2.sdlttf.TTF_WasInit():
            sdl2.sdlttf.TTF_Init()

        self.__c_window = sdl2.SDL_CreateWindow(
            kurses.virtual_console.DEFAULT_WINDOW_TITLE.encode(),
            *DEFAULT_WINDOW_POSITION,
            *DEFAULT_WINDOW_SIZE,
            sdl2.SDL_WINDOW_SHOWN)
        self.__c_renderer = sdl2.SDL_CreateRenderer(self.__c_window, -1, _type_render[self.render])

        self.set_resizable(self.resizable)

    def __del_sdl2(self):
        sdl2.sdlttf.TTF_CloseFont(self.font)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__init_sdl2()

        self.__c_font = None
        self.__background_color = 0, 0, 0
        self.__buffer = kurses.buffer.VirtualBuffer(80, 30)
        self.__target = None
        self.__textures_allocate = {}
        self.__chr_format_key = lambda _str: _str.decode().lower()
        self.__size_texture = None
        self.__blink_cursor = 0

    def __del__(self):
        self.__del_sdl2()

    def set_resizable(self, _bool: bool):
        self._resizable = _bool
        sdl2.SDL_SetWindowResizable(self.window, _bool)

    def set_font(self, filename: str, ptsize=None):
        if ptsize is None:
            ptsize = kurses.buffer.DEFAULT_PTSIZE

        self.__c_font = sdl2.sdlttf.TTF_OpenFont(filename.encode(), ptsize=ptsize)

        if self.__c_font is None:
            raise FileNotFoundError("Font no found")

        render_method = get_render_font_method_sdl2(self.encoding, self.quality_font)
        empty_texture = create_texture_chr_sdl2(self.font, render_method, self.surface, ' ')

        self.__size_texture = get_size_texture_sdl2(empty_texture)

        sdl2.SDL_DestroyTexture(empty_texture)

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
        if self.font is None:
            raise RuntimeError("You need load a font source")

        while self.running:
            frame_time = 1.0 / self.fps
            frame_start = time.time()

            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                self.push_events(event)

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

            if self.auto_clean_cache:
                self.clear_cache()

            self._dt = time.time() - frame_start
            wait_time = max(0, frame_time - self._dt)

            sdl2.SDL_Delay(int(wait_time * 1000))

            if self.auto_clean_buffer:
                self.buffer.clrscr()

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

    def push_events(self, event: sdl2.SDL_Event):
        w, h = self.__size_texture

        if event.type == sdl2.SDL_QUIT:
            self.quit()

        elif event.type == sdl2.SDL_WINDOWEVENT:
            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                width, height = event.window.data1, event.window.data2

                if self._resizable:
                    self.buffer.resize(width // w, height // h)

    def present(self):
        w, h = self.__size_texture
        render_method = get_render_font_method_sdl2(self.encoding, self.quality_font)
        _cast_depth_colors = functools.partial(kurses.colors.cast_depth_colors, bits=self.depth_colors)

        for _obj in self.buffer:
            x, y = _obj.x, _obj.y
            limit_h, limit_w = self.buffer.buffersize

            while x > limit_w:
                x = x - (limit_w + 1)
                y += 1

            if isinstance(_obj, kurses.buffer.CharacterAttribute):
                d_rect = sdl2.SDL_Rect(x * w, y * h, w, h)

                if _obj not in self.__textures_allocate.keys():
                    self.__textures_allocate[_obj] = create_texture_chr_sdl2(
                        self.font, render_method, self.surface, _obj.code,
                        _cast_depth_colors(_obj.foreign),
                        _cast_depth_colors(_obj.background),
                        get_style_sdl2(_obj)
                    )

                sdl2.SDL_SetRenderDrawColor(self.surface, *_obj.background, 255)
                sdl2.SDL_RenderCopy(self.surface, self.__textures_allocate[_obj], None, d_rect)
            elif isinstance(_obj, kurses.buffer.RectangleAttribute):
                d_rect = sdl2.SDL_Rect(x, y, _obj.w * w, _obj.h * h)

                sdl2.SDL_SetRenderDrawColor(self.surface, *_obj.color, 255)
                sdl2.SDL_RenderFillRect(self.surface, d_rect)

        if self.__blink_cursor > self.time_blink_cursor:
            _cursor_type = get_cursor(self.type_cursor)
            x, y = self.buffer.wherex() * w, self.buffer.wherey() * h

            sdl2.SDL_SetRenderDrawColor(self.surface, *self.cursor_color, 255)
            sdl2.SDL_RenderFillRect(self.surface, _cursor_type(x, y, w, h))

        if self.__blink_cursor > self.time_blink_cursor * 2:
            self.__blink_cursor = 0

        self.__blink_cursor += self.time_wait_blink_cursor * self.dt

    def quit(self):
        self.running = False
