try:
    import sdl2
    from pyrogue.backend.sdl2 import SDL2VirtualConsole

    Console = SDL2VirtualConsole

except ImportError as e:
    import pygame
    from pyrogue.backend.pygame import PygameVirtualConsole

    Console = PygameVirtualConsole

__all__ = ["Console"]
