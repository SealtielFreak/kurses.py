# So, I need work her
from kurses.backend.sdl2.bitmap_surface import SDL2BitmapSurface

try:
    import sdl2

    from kurses.backend.sdl2.font_resources import SDL2FontResources
    from kurses.backend.sdl2.texture_surface import SDL2TextureSurface
    from kurses.backend.sdl2 import SDL2VirtualTerminal

    VirtualTerminal = SDL2VirtualTerminal
    FontResources = SDL2FontResources
    TextureSurface = SDL2TextureSurface
    BitmapSurface = SDL2BitmapSurface

except ImportError:
    try:
        raise ImportError("The module for Pygame has not been implemented yet.")
    except ImportError:
        raise ImportError("You need install pySDL2 for this module work!")

__all__ = ["VirtualTerminal"]
