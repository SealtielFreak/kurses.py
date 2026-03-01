# So, I need work her
from kurses.backend.sdl2.resources import SDL2AudioSystem

try:
    import sdl2

    from kurses.backend.sdl2.font_resources import SDL2FontResources
    from kurses.backend.sdl2.texture_surface import SDL2TextureSurface
    from kurses.backend.sdl2 import SDL2VirtualTerminal
    from kurses.backend.sdl2.bitmap_surface import SDL2BitmapSurface
    from kurses.backend.sdl2.interface.joystick import SDL2JoystickInterface
    from kurses.backend.sdl2.resources.mixer import SDL2Effect, SDL2Music, SDL2Buzzer

    VirtualTerminal = SDL2VirtualTerminal
    FontResources = SDL2FontResources
    TextureSurface = SDL2TextureSurface
    BitmapSurface = SDL2BitmapSurface
    JoystickInterface = SDL2JoystickInterface
    AudioSystem = SDL2AudioSystem
    Effect = SDL2Effect
    Music = SDL2Music

except ImportError:
    try:
        raise ImportError("The module for Pygame has not been implemented yet.")
    except ImportError:
        raise ImportError("You need install pySDL2 for this module work!")

__all__ = ["VirtualTerminal", "AudioSystem", "Effect", "Music"]
