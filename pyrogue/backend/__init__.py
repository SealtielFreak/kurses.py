try:
    import sdl2
    from pyrogue.backend.sdl2 import SDL2VirtualConsole as Console

except ImportError as e:
    import pygame
    from pyrogue.backend.pygame import PygameVirtualConsole as Console

__all__ = ["Console"]
