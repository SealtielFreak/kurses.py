import ctypes
import functools
import typing

import sdl2
import sdl2.sdlttf

import kurses.buffer
import kurses.colors
import kurses.virtual_console
import kurses.font_resources

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


def get_size_textures_from_font(font, renderer, render_method):
    empty_texture = create_texture_chr_sdl2(font, render_method, renderer, ' ')
    w, h = get_size_texture_sdl2(empty_texture)

    sdl2.SDL_DestroyTexture(empty_texture)

    return w, h


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


def get_render_font_method_sdl2(encoding: kurses.font_resources.EncodingFont, quality: kurses.font_resources.QualityFont) -> RenderMethodSDL2:
    _render_f = {
        kurses.font_resources.EncodingFont.ASCII: {
            kurses.font_resources.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderText_Solid),
            kurses.font_resources.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderText_Shaded,
            kurses.font_resources.QualityFont.LCD: sdl2.sdlttf.TTF_RenderText_LCD,
            kurses.font_resources.QualityFont.BLENDED: cast_render_method(sdl2.sdlttf.TTF_RenderText_Blended)
        },
        kurses.font_resources.EncodingFont.UTF_8: {
            kurses.font_resources.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderUTF8_Solid),
            kurses.font_resources.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderUTF8_Shaded,
            kurses.font_resources.QualityFont.LCD: sdl2.sdlttf.TTF_RenderUTF8_LCD,
            kurses.font_resources.QualityFont.BLENDED: cast_render_method(sdl2.sdlttf.TTF_RenderUTF8_Blended)
        },
        kurses.font_resources.EncodingFont.UNICODE: {
            kurses.font_resources.QualityFont.SOLID: cast_render_method(sdl2.sdlttf.TTF_RenderUNICODE_Solid),
            kurses.font_resources.QualityFont.SHADED: sdl2.sdlttf.TTF_RenderUNICODE_Shaded,
            kurses.font_resources.QualityFont.LCD: sdl2.sdlttf.TTF_RenderUNICODE_LCD,
            kurses.font_resources.QualityFont.BLENDED: cast_render_method(sdl2.sdlttf.TTF_RenderUNICODE_Blended)
        },
    }[encoding][quality]

    def render_method(font, _chr, fg, bg):
        _chr = _chr.encode()

        return _render_f(font, _chr, fg, bg)

    return render_method


class SDL2FontResources(kurses.font_resources.FontResources):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__c_font = sdl2.sdlttf.TTF_OpenFont(self.filename.encode(), ptsize=self.ptsize)

        if self.__c_font is None:
            raise FileNotFoundError("Font no found")

        _render_method = get_render_font_method_sdl2(self.encoding, self.quality)
        _surface = _render_method(self.font, ' ', color_sdl2((0, 0, 0)), color_sdl2((0, 0, 0)))

        self.__size = (
            _surface.contents.w,
            _surface.contents.h
        )

        sdl2.SDL_FreeSurface(_surface)

    def __del__(self):
        pass

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self.__size

    @property
    def font(self) -> sdl2.sdlttf.TTF_Font:
        return self.__c_font

    def clean_cache(self):
        pass

    def present_chr(self, surface: sdl2.SDL_Renderer, _chr: kurses.buffer.CharacterAttribute) -> sdl2.SDL_Renderer:
        _cast_depth_colors = functools.partial(kurses.colors.cast_depth_colors, bits=self.depth_colors)
        _render_method = get_render_font_method_sdl2(self.encoding, self.quality)

        if _chr not in self.allocate_textures:
            self.allocate_textures[_chr] = create_texture_chr_sdl2(
                self.font, _render_method, surface, _chr.code,
                _cast_depth_colors(_chr.foreign),
                _cast_depth_colors(_chr.background),
                get_style_sdl2(_chr)
            )

        return self.allocate_textures[_chr]

