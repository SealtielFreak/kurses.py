import collections
import ctypes
import functools
import time
import typing

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


def get_size_texture_sdl2(texture: sdl2.SDL_Texture):
    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_QueryTexture(texture, None, None, ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value


def create_texture_chr_sdl2(font: sdl2.sdlttf.TTF_Font, render_method: RenderMethodSDL2, renderer: sdl2.SDL_Renderer,
                            _chr: str, fg=(0, 0, 0), bg=(0, 0, 0), style=0):
    sdl2.sdlttf.TTF_SetFontStyle(font, style)

    _surface = render_method(font, _chr, color_sdl2(fg), color_sdl2(bg))
    _texture = sdl2.SDL_CreateTextureFromSurface(renderer, _surface)

    sdl2.SDL_FreeSurface(_surface)

    return _texture


def get_size_textures_from_font(font, renderer, render_method):
    empty_texture = create_texture_chr_sdl2(font, render_method, renderer, ' ')
    w, h = get_size_texture_sdl2(empty_texture)
    sdl2.SDL_DestroyTexture(empty_texture)

    return w, h


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


def get_render_font_method_sdl2(encoding: kurses.virtual_console.EncodingFont,
                                quality: kurses.virtual_console.QualityFont) -> RenderMethodSDL2:
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


def get_cursor(_type: kurses.buffer.TypeCursor):
    _cursor = {
        kurses.buffer.TypeCursor.LINE: lambda x, y, w, h: sdl2.SDL_Rect(x, y + ((h // 4) * 3), w, (h // 4)),
        kurses.buffer.TypeCursor.RECT: lambda x, y, w, h: sdl2.SDL_Rect(x, y, w, h),
        kurses.buffer.TypeCursor.SOLID_RECT: lambda x, y, w, h: sdl2.SDL_Rect(x, y, w, h),
        kurses.buffer.TypeCursor.VERTICAL: lambda x, y, w, h: sdl2.SDL_Rect(x, y, w // 6, h),
        kurses.buffer.TypeCursor.UNDERSCORE: lambda x, y, w, h: sdl2.SDL_Rect(x, y + ((h // 8) * 7), w, (h // 8)),
        kurses.buffer.TypeCursor.EMPTY: lambda *args: sdl2.SDL_Rect(0, 0, 0, 0)
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
        self.__buffers = [kurses.buffer.VirtualBuffer(80, 30)]
        self.__target = None
        self.__textures_allocate = {}
        self.__chr_format_key = lambda _str: _str.decode().lower()

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

    @property
    def buffers(self):
        return self.__buffers

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
                [buffer.clrscr() for buffer in self.buffers]

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
        if event.type == sdl2.SDL_QUIT:
            self.quit()

        elif event.type == sdl2.SDL_WINDOWEVENT:
            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                width, height = event.window.data1, event.window.data2

                if self._resizable:
                    for _buffer in self.buffers:
                        sx, sy = _buffer.sx, _buffer.sy
                        render_method = get_render_font_method_sdl2(self.encoding, self.quality_font)
                        w, h = get_size_textures_from_font(self.font, self.surface, render_method)

                        _buffer.resize(width // w, height // h)

    def present(self):
        render_method = get_render_font_method_sdl2(self.encoding, self.quality_font)
        _cast_depth_colors = functools.partial(kurses.colors.cast_depth_colors, bits=self.depth_colors)

        for _buffer in self.buffers:
            rows, cols = _buffer.buffersize
            x_offset, y_offset = _buffer.x, _buffer.y
            x_scale, y_scale = _buffer.sx, _buffer.sy
            texture_width, texture_height = get_size_textures_from_font(self.font, self.surface, render_method)

            scale_texture_height, scale_texture_width = texture_width * x_scale, texture_height * y_scale

            for _obj in _buffer:
                x, y = _obj.x + x_offset, _obj.y + y_offset

                while x > cols:
                    x = x - (cols + 1)
                    y += 1

                if isinstance(_obj, kurses.buffer.CharacterAttribute):
                    d_rect = sdl2.SDL_Rect(
                        x * scale_texture_height, y * scale_texture_width, scale_texture_height, scale_texture_width
                    )

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
                    d_rect = sdl2.SDL_Rect(x, y, _obj.w * texture_width, _obj.h * texture_height)

                    sdl2.SDL_SetRenderDrawColor(self.surface, *_obj.color, 255)
                    sdl2.SDL_RenderFillRect(self.surface, d_rect)

                if _buffer.blink_cursor > _buffer.time_blink_cursor:
                    _cursor_type = get_cursor(_buffer.type_cursor)
                    x_cursor, y_cursor = _buffer.wherex() * scale_texture_height, _buffer.wherey() * scale_texture_width

                    sdl2.SDL_SetRenderDrawColor(self.surface, *_buffer.cursor_color, 255)
                    sdl2.SDL_RenderFillRect(
                        self.surface,
                        _cursor_type(x_cursor, y_cursor, scale_texture_height, scale_texture_width)
                    )

                if _buffer.blink_cursor > _buffer.time_blink_cursor * 2:
                    _buffer.blink_cursor = 0

                _buffer.blink_cursor += _buffer.time_wait_blink_cursor * self.dt

    def quit(self):
        self.running = False
